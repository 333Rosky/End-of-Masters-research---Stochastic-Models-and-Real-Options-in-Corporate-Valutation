import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import wrds
import pandas as pd
import numpy_financial as npf
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import logging
import yahoo_fin.options as op

logging.basicConfig(filename='monte_carlo_simulations.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

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
    return tickers_str, final_data_cleaned, gvkey_list

tickers_str, final_data_cleaned, gvkey_list = retrieve_data()

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
    logging.info("Starting the main process...")
    logging.info("Processing interest rates...")
    interest_rate_dict = process_interest_rate()
    print("Interest rate dictionary:")
    print(interest_rate_dict)

    logging.info("Preparing data...")
    final_data_cleaned['datadate'] = pd.to_datetime(final_data_cleaned['datadate'], errors='coerce')
    final_data_cleaned['Quarter'] = final_data_cleaned['datadate'].dt.to_period('Q').astype(str)
    final_data_cleaned['interest_rate'] = final_data_cleaned['Quarter'].map(interest_rate_dict)
    final_data_cleaned['npv'] = final_data_cleaned.apply(lambda row: calculate_npv(row, interest_rate_dict), axis=1)
    
    final_data_cleaned['Simulated_Mean_NPV'] = np.nan
    final_data_cleaned['Simulated_SD_NPV'] = np.nan

    logging.info("Retrieving options data...")

    logging.info("Starting Monte Carlo simulations...")
    for gvkey, group in final_data_cleaned.groupby('gvkey'):
        logging.info(f"Processing gvkey: {gvkey}")
        # Pour chaque entreprise, récupérez les taux et cash flows
        rates = group['interest_rate'].tolist()
        cash_flows = group['oancfy'].tolist()
        num_periods = len(cash_flows)
        # Exécutez la simulation de Monte Carlo pour chaque entreprise
        simulated_mean, simulated_std = monte_carlo_simulation(cash_flows, rates, 1000, num_periods)

        # Mettez à jour le DataFrame avec les résultats pour ce gvkey
        final_data_cleaned.loc[final_data_cleaned['gvkey'] == gvkey, 'Simulated_Mean_NPV'] = simulated_mean
        final_data_cleaned.loc[final_data_cleaned['gvkey'] == gvkey, 'Simulated_SD_NPV'] = simulated_std

        logging.info(f"gvkey: {gvkey} - Simulated Mean NPV: {simulated_mean}, Simulated SD NPV: {simulated_std}")

    logging.info("Simulations completed.")
    
    # Ajouter une colonne pour la moyenne des NPV par gvkey
    final_data_cleaned['Mean_NPV'] = final_data_cleaned.groupby('gvkey')['npv'].transform('mean')

    # Ajouter une colonne pour l'écart-type des NPV par gvkey
    final_data_cleaned['SD_NPV'] = final_data_cleaned.groupby('gvkey')['npv'].transform('std')

    logging.info("Saving results to Excel...")
    # Maintenant, sauvegardez le DataFrame avec les nouvelles colonnes dans un fichier Excel
    final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)
    logging.info("Results saved.")

    print("Moyenne des NPV par gvkey: ")
    print(final_data_cleaned['Mean_NPV'])

    print("Écart-type des NPV par gvkey: ")
    print(final_data_cleaned['SD_NPV'])
    
    print(f"Simulated Mean NPV: {simulated_mean}")
    print(f"Simulated SD NPV: {simulated_std}")
     # Sauvegarde des résultats
    final_data_cleaned.to_excel('Cash_Flows_Entreprises_with_NPV.xlsx', index=False)

def simulate_cash_flow(mean, std, num_periods):
    return np.random.normal(mean, std, num_periods)


def calculate_simulated_npv(rates, cash_flows):
    npv = 0
    for i, cash_flow in enumerate(cash_flows):
        npv += cash_flow / ((1 + rates[i]) ** (i + 1))
    return npv

def monte_carlo_simulation(cash_flows, rates, num_simulations, num_periods):
    simulated_npvs = []
    for _ in range(num_simulations):
        # Générer des cash flows simulés pour chaque période
        simulated_cash_flows = np.random.normal(np.mean(cash_flows), np.std(cash_flows), num_periods)
        # Calculer la NPV pour les cash flows simulés avec les taux d'intérêt correspondants
        simulated_npv = calculate_simulated_npv(rates, simulated_cash_flows)
        simulated_npvs.append(simulated_npv)
    
    # Calculer et retourner la moyenne et l'écart-type des NPV simulées
    mean_npv = np.mean(simulated_npvs)
    std_npv = np.std(simulated_npvs)
    return mean_npv, std_npv

# Exécutez la fonction principale
if __name__ == "__main__":
    main()