import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Charger les données nécessaires pour le plot
final_data_cleaned = pd.read_excel('Cash_Flows_Entreprises_with_NPV.xlsx')

def update_plot(selected_companies, final_data_cleaned):
    fig, ax = plt.subplots()
    for company in selected_companies:
        company_data = final_data_cleaned[final_data_cleaned['conm'] == company]
        ax.errorbar(company_data['npv_mean'], company_data['npv_sd'], fmt='o', label=company)

    ax.set_title('Mean NPV with Standard Deviation from Monte Carlo Simulation')
    ax.set_xlabel('Company')
    ax.set_ylabel('Net Present Value (NPV)')
    ax.legend()
    plt.show()

# Exemple d'utilisation (Vous devrez adapter cela en fonction de la manière dont vous souhaitez sélectionner les entreprises)
if __name__ == "__main__":
    # Créer une liste de noms d'entreprises à partir du DataFrame pour l'exemple
    selected_companies = final_data_cleaned['conm'].unique().tolist()
    # Mettre à jour le plot avec toutes les entreprises (pour l'exemple)
    update_plot(selected_companies, final_data_cleaned)
