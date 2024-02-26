import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import wrds
import pandas as pd
import numpy_financial as npf
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def retrieve_data() :
    db = wrds.Connection(wrds_username='romainbastiani')
    # Retrieve S&P 500 index membership from CRSP
    # You would replace 'your_username' and 'your_password' with your actual WRDS credentials
    mse = db.raw_sql("""
                        select comnam, ncusip, namedt, nameendt, 
                        permno, shrcd, exchcd, hsiccd, ticker
                        from crsp.msenames
                        """, date_cols=['namedt', 'nameendt'])
    # Créez une liste des tickers uniques
    ticker_list = mse['ticker'].dropna().unique().tolist()
    # Élimination des doublons en convertissant la liste en un ensemble, puis reconvertir en liste
    ticker_list = list(set(ticker_list))
    # Convertissez la liste des tickers en une chaîne pour la requête SQL
    tickers_str = "', '".join(ticker_list)
    # Exécutez votre requête pour obtenir les gvkeys des entreprises
    compustat_data = db.raw_sql("""
                        SELECT gvkey, conm
                        FROM comp.company
                        """)
    # Créez une liste des gvkeys uniques
    gvkey_list = compustat_data['gvkey'].unique().tolist()
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

    return tickers_str, final_data_cleaned

tickers_str, final_data_cleaned = retrieve_data()

def process_interest_rate():
    # Charger les données des taux d'intérêt
    interest_rate_df = pd.read_excel('US_Interest_Rate.xlsx')
    # Vérifiez et convertissez 'DTB3' en float si nécessaire
    if interest_rate_df['DTB3'].dtype == object:
        interest_rate_df['DTB3'] = interest_rate_df['DTB3'].str.replace(',', '.').astype(float)
    # Convertir les taux d'intérêt de pourcentages en décimaux sans répéter la conversion
    interest_rate_df['DTB3'] = interest_rate_df['DTB3'] / 100
    # Convertir 'observation_date' en format datetime
    interest_rate_df['observation_date'] = pd.to_datetime(interest_rate_df['observation_date'])
    # Ajouter une colonne pour les trimestres
    interest_rate_df['Quarter'] = interest_rate_df['observation_date'].dt.to_period('Q')
    # Calculer la moyenne des taux d'intérêt par trimestre
    quarterly_interest_rates = interest_rate_df.groupby('Quarter')['DTB3'].mean()
    # Convertir en dictionnaire
    interest_rate_dict = quarterly_interest_rates.to_dict()
    return interest_rate_dict


# Exemple de fonction pour calculer la NPV pour chaque ligne
def calculate_npv(row, interest_rate_dict):
    # Obtenir le taux d'intérêt pour le trimestre correspondant de la ligne
    rate = row['interest_rate']
    # Assurez-vous que le taux n'est pas déjà un taux décimal. S'il est exprimé en pourcentage, divisez par 100.
    if rate > 1:
        rate = rate / 100
    # Calculer la NPV en utilisant numpy_financial.npv
    # La ligne suivante est ajustée pour utiliser 'oancfy' comme nom de colonne de cash flow selon votre DataFrame
    npv = npf.npv(rate, [0, row['oancfy']])
    return npv

def main():
    
    interest_rate_dict = process_interest_rate()
    print("Dictionnaire des taux d'intérêt trimestriels :")
    print(interest_rate_dict)

    # Supposons que final_data_cleaned est votre DataFrame avec les données nécessaires
    # Assurez-vous que 'datadate' est au format datetime et créez une colonne 'Quarter'
    final_data_cleaned['datadate'] = pd.to_datetime(final_data_cleaned['datadate'], errors='coerce')
    final_data_cleaned['Quarter'] = final_data_cleaned['datadate'].dt.to_period('Q').astype(str)
    
    # Ajoutez une colonne pour les taux d'intérêt en mappant avec le dictionnaire
    final_data_cleaned['interest_rate'] = final_data_cleaned['Quarter'].map(interest_rate_dict)
    
    # Calcul de la NPV pour chaque ligne en utilisant le taux d'intérêt et le cash flow
    final_data_cleaned['npv'] = final_data_cleaned.apply(lambda row: calculate_npv(row, interest_rate_dict), axis=1)
    
    # Sauvegarder le DataFrame avec les calculs de NPV dans un fichier Excel
    final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)

    print(final_data_cleaned[['gvkey', 'Quarter', 'interest_rate', 'npv']].head())

# Exécutez la fonction principale
if __name__ == "__main__":
    main()

# Define the number of simulations and periods, and the discount rate
"""num_simulations = 1000
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
))"""

"""# Save the results to a new Excel file
final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)"""

"""# Function to update the plot based on selected companies
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
root.mainloop()"""