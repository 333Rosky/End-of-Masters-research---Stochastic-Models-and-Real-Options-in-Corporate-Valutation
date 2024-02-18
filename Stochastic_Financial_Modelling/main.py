import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import wrds
import pandas as pd
import warnings
import numpy_financial as npf

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
        SELECT gvkey, datadate, fyear, oancf
        FROM comp.funda
        WHERE gvkey IN ('{gvkeys_str}')
        AND fyear BETWEEN 2015 AND 2023
        AND indfmt = 'INDL'
        AND datafmt = 'STD'
        AND popsrc = 'D'
        AND consol = 'C'
        ORDER BY gvkey, fyear
    """
# Exécutez la requête pour obtenir les données de cash flow
cash_flows_data = db.raw_sql(cash_flows_query)

print(cash_flows_data)

# Supposons que compustat_data contient 'conm' (nom de l'entreprise) et 'tic' (ticker) en plus de 'gvkey'
# Joindre les données de cash flow avec les informations des entreprises
final_data = pd.merge(cash_flows_data, compustat_data[['gvkey', 'conm']], on='gvkey', how='left')
final_data_cleaned = final_data.dropna(subset=['oancf'])
# Vérifier les premières lignes pour confirmer que la fusion est correcte
print(final_data.head())

cash_flows_dict = cash_flows_data.groupby('gvkey')['oancf'].apply(list).to_dict()

# Save the updated DataFrame to an Excel file
final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)
print("Excel file with NPVs created successfully.")

final_data_cleaned = pd.read_excel('Cash_Flows_Entreprises_with_NPV.xlsx')

# Set the discount rate to a fixed value of 0.05
discount_rate = 0.05

npv_dict = {}
for gvkey, group in final_data_cleaned.groupby('gvkey'):
    cash_flows = group['oancf'].tolist()
    # Assuming the first cash flow is an initial outlay and should be negative
    cash_flows[0] = -abs(cash_flows[0])
    npv = npf.npv(discount_rate, cash_flows)
    npv_dict[gvkey] = npv

# Add the NPV values to your final DataFrame
final_data_cleaned['npv'] = final_data_cleaned['gvkey'].map(npv_dict)

# Save the updated DataFrame to an Excel file
final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)
print("Excel file with NPVs created successfully.")

# Define the number of simulations and the number of periods
num_simulations = 1000
num_periods = len(cash_flows)  # Replace with the actual number of periods you have

# Define the mean and standard deviation for the cash flows
mean = np.mean(cash_flows)
std_dev = np.std(cash_flows)

# Replace 'your_excel_file.xlsx' with the path to your actual Excel file
df = pd.read_excel('Cash_Flows_Entreprises_with_NPV.xlsx')

# Calculate mean and standard deviation for each company's cash flows
stats_df = df.groupby('gvkey')['oancf'].agg(['mean', 'std']).reset_index()

# Calculate mean and standard deviation for each company's cash flows
grouped = final_data_cleaned.groupby('gvkey')['oancf']
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


