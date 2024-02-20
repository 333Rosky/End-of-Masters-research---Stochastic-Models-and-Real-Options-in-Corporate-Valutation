import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import wrds
import pandas as pd
import warnings
import numpy_financial as npf
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

db = wrds.Connection(wrds_username='romainbastiani')

# Retrieve S&P 500 index membership from CRSP
# You would replace 'your_username' and 'your_password' with your actual WRDS credentials

# Exécutez votre requête pour obtenir les tickers des entreprises du S&P 500
mse = db.raw_sql("""
                        select comnam, ncusip, namedt, nameendt, 
                        permno, shrcd, exchcd, hsiccd, ticker
                        from crsp.msenames
                        """, date_cols=['namedt', 'nameendt'])
# Créez une liste des tickers uniques
ticker_list = mse['ticker'].dropna().unique().tolist()

# Élimination des doublons en convertissant la liste en un ensemble, puis reconvertir en liste
ticker_list = list(set(ticker_list))

print(ticker_list)

# Convertissez la liste des tickers en une chaîne pour la requête SQL
tickers_str = "', '".join(ticker_list)

# Exécutez votre requête pour obtenir les gvkeys des entreprises
compustat_data = db.raw_sql("""
                        SELECT gvkey, conm
                        FROM comp.company
                        """)
# Créez une liste des gvkeys uniques
gvkey_list = compustat_data['gvkey'].unique().tolist()

print(gvkey_list)

gvkeys_str = "', '".join(gvkey_list)


# Interrogez Compustat pour obtenir les cash flows opérationnels
cash_flows_query = f"""
        SELECT gvkey, datadate, fqtr, oancfy
        FROM comp.fundq
        WHERE gvkey IN ('{gvkeys_str}')
        AND datadate BETWEEN '2015-01-01' AND '2023-12-31'
        AND indfmt = 'INDL'
        AND datafmt = 'STD'
        AND popsrc = 'D'
        AND consol = 'C'
        ORDER BY gvkey, datadate
    """
# Exécutez la requête pour obtenir les données de cash flow
cash_flows_data = db.raw_sql(cash_flows_query)
final_data = pd.merge(cash_flows_data, compustat_data[['gvkey', 'conm']], on='gvkey', how='left')
final_data_cleaned = final_data.dropna(subset=['oancfy'])

# Load interest rate data
interest_rate_df = pd.read_excel('US_Interest_Rate.xlsx', skiprows=10)
# Convert the interest rates from percentages to decimals if they are in string format with commas
if interest_rate_df['DTB3'].dtype == 'object':
    interest_rate_df['DTB3'] = interest_rate_df['DTB3'].str.replace(',', '.').astype(float)
interest_rate_df['DTB3'] = interest_rate_df['DTB3'] / 100

# Convertir 'observation_date' en format datetime si ce n'est pas déjà fait
interest_rate_df['observation_date'] = pd.to_datetime(interest_rate_df['observation_date'])

# Ajouter une colonne pour les trimestres
interest_rate_df['Quarter'] = interest_rate_df['observation_date'].dt.to_period('Q')

# Calculer la moyenne des taux d'intérêt par trimestre
quarterly_interest_rates = interest_rate_df.groupby('Quarter')['DTB3'].mean()

# Convertir le résultat en dictionnaire
interest_rate_dict = quarterly_interest_rates.to_dict()

print("Data type of 'datadate' in final_data_cleaned:", final_data_cleaned['datadate'].dtype)
print("Data type of 'observation_date' in interest_rate_df:", interest_rate_df['observation_date'].dtype)

# Since you've already attempted conversion, these should confirm both are datetime64[ns].

print(final_data_cleaned['datadate'].dtype)
print(interest_rate_df['observation_date'].dtype)

# Make sure 'datadate' is a datetime in both DataFrames to avoid merge conflicts
final_data_cleaned = final_data_cleaned.copy()
final_data_cleaned['datadate'] = pd.to_datetime(final_data_cleaned['datadate'], errors='coerce')
interest_rate_df['observation_date'] = pd.to_datetime(interest_rate_df['observation_date'], errors='coerce')

# Now try to merge again
final_data_with_rates = pd.merge(
    final_data_cleaned,
    interest_rate_df,
    left_on='datadate',
    right_on='observation_date',
    how='left'
)



def make_first_negative(x):
    x.iloc[0] = -abs(x.iloc[0])
    return x

final_data_with_rates['oancfy'] = final_data_with_rates.groupby('gvkey')['oancfy'].transform(make_first_negative)

# Assuming the first cash flow is an outlay and should be negative
final_data_with_rates['oancfy'] = final_data_with_rates.groupby('gvkey')['oancfy'].transform(lambda x: -abs(x.iloc[0]) if x.name == 0 else x)

def calculate_npv(cash_flows, interest_rates):
    npv = 0
    for i, cash_flow in enumerate(cash_flows):
        rate = interest_rates[i] if i < len(interest_rates) else interest_rates[-1]
        npv += cash_flow / (1 + rate) ** (i + 1)
    return npv

# Function to calculate NPV
def calculate_quarterly_npv(cash_flows, cash_flow_quarters, interest_rate_dict):
    npv = 0
    for i, cash_flow in enumerate(cash_flows):
        quarter = cash_flow_quarters[i]
        rate = interest_rate_dict.get(quarter, 0) / 4  # Convertir le taux annuel en taux trimestriel
        npv += cash_flow / (1 + rate) ** (i + 1)
    return npv

# Save the DataFrame with NPV calculations
final_data_with_rates.to_excel('Cash_Flows_with_NPV_and_Rates.xlsx', index=False)
# Vérifier les premières lignes pour confirmer que la fusion est correcte
print(final_data.head())

cash_flows_dict = cash_flows_data.groupby('gvkey')['oancfy'].apply(list).to_dict()

# Save the updated DataFrame to an Excel file
final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)
print("Excel file with NPVs created successfully.")

final_data_cleaned = pd.read_excel('Cash_Flows_Entreprises_with_NPV.xlsx')

npv_dict = {}

discount_rate = 0.05

for gvkey, group in final_data_cleaned.groupby('gvkey'):
    cash_flows = group['oancfy'].tolist()
    # Assuming the first cash flow is an initial outlay and should be negative
    cash_flows[0] = -abs(cash_flows[0])
    npv = npf.npv(discount_rate, cash_flows)
    npv_dict[gvkey] = npv


def calculate_npv(cash_flows, interest_rates):
    # S'assurer qu'il y a au moins un taux d'intérêt
    if not interest_rates:
        raise ValueError("La liste des taux d'intérêt est vide.")
    
    # Étendre la liste des taux d'intérêt pour correspondre à la longueur des flux de trésorerie si nécessaire
    if len(interest_rates) < len(cash_flows):
        last_rate = interest_rates[-1] if interest_rates else 0.05  # Utiliser le dernier taux ou un taux par défaut
        interest_rates += [last_rate] * (len(cash_flows) - len(interest_rates))
    
    npv = 0
    for i, cash_flow in enumerate(cash_flows):
        rate = interest_rates[i]  # Maintenant, il est sûr d'accéder à interest_rates[i]
        npv += cash_flow / (1 + rate) ** (i + 1)  # Assurez-vous que l'exposant est correct
    return npv

# Add the NPV values to your final DataFrame
final_data_cleaned['npv'] = final_data_cleaned['gvkey'].map(npv_dict)

# Save the updated DataFrame to an Excel file
final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)
print("Excel file with NPVs created successfully.")

# Define the mean and standard deviation for the cash flows
mean = np.mean(cash_flows)
std_dev = np.std(cash_flows)

# Replace 'your_excel_file.xlsx' with the path to your actual Excel file
df = pd.read_excel('Cash_Flows_Entreprises_with_NPV.xlsx')

# Calculate mean and standard deviation for each company's cash flows
stats_df = df.groupby('gvkey')['oancfy'].agg(['mean', 'std']).reset_index()

# Calculate mean and standard deviation for each company's cash flows
grouped = final_data_cleaned.groupby('gvkey')['oancfy']
final_data_cleaned['mean'] = grouped.transform('mean')  # Calculate mean cash flow
final_data_cleaned['sd'] = grouped.transform('std')  # Calculate standard deviation of cash flow

final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)
print("Excel file with Mean and SD created successfully.")

# Define the number of simulations and periods, and the discount rate
num_simulations = 1000
num_periods = 10  # Adjust this to match the actual number of periods for your cash flows
discount_rate = 0.05

# Define a function for the Monte Carlo simulation
def monte_carlo_simulation(mean, sd, num_periods, num_simulations, discount_rate):
    npv_list = []
    for i in range(num_simulations):
        # Generate random cash flows for each period based on mean and sd
        simulated_cash_flows = np.random.normal(mean, sd, num_periods)
        # Calculate the NPV of the simulated cash flows
        npv = npf.npv(discount_rate, simulated_cash_flows)
        npv_list.append(npv)
    # Return the mean and standard deviation of the NPVs
    return np.mean(npv_list), np.std(npv_list)

# Run the Monte Carlo simulation for each company and store the results in new columns
final_data_cleaned['npv_mean'], final_data_cleaned['npv_sd'] = zip(*final_data_cleaned.apply(
    lambda x: monte_carlo_simulation(
        x['mean'], x['sd'], num_periods, num_simulations, discount_rate
    ), axis=1
))

# Save the results to a new Excel file
final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)

# Function to update the plot based on selected companies
def update_plot():
    global canvas  # Add this line to use the 'canvas' variable defined outside the function
    selected_indices = list(map(int, lb.curselection()))
    selected_companies = [lb.get(i) for i in selected_indices]
    selected_data = final_data_cleaned[final_data_cleaned['conm'].isin(selected_companies)]

    fig, ax = plt.subplots()
    for company in selected_companies:
        company_data = selected_data[selected_data['conm'] == company]
        ax.errorbar(company_data['npv_mean'], company_data['npv_sd'], fmt='o', label=company)

    ax.set_title('Mean NPV with Standard Deviation from Monte Carlo Simulation')
    ax.set_xlabel('Company')
    ax.set_ylabel('Net Present Value (NPV)')
    ax.legend()

    # Check if 'canvas' exists before trying to pack it away
    if canvas is not None:
        canvas.get_tk_widget().pack_forget()
    
    # Create a new canvas for the new figure
    canvas = FigureCanvasTkAgg(fig, master=root) 
    canvas.get_tk_widget().pack()
    canvas.draw()

# Create the main Tkinter window
root = tk.Tk()
root.title('Monte Carlo Simulation Data Plotter')

# Create a listbox to select companies
lb = tk.Listbox(root, selectmode='multiple', exportselection=0)
for company in final_data_cleaned['conm'].unique():
    lb.insert(tk.END, company)
lb.pack(side='left', fill='y')

# Create a scrollbar for the listbox
scrollbar = ttk.Scrollbar(root, orient='vertical', command=lb.yview)
scrollbar.pack(side='left', fill='y')
lb.config(yscrollcommand=scrollbar.set)

# Create a button to update the plot
plot_button = ttk.Button(root, text='Plot Data', command=update_plot)
plot_button.pack(side='top')

# Placeholder for the matplotlib figure canvas
canvas = None

# Start the Tkinter event loop
root.mainloop()