import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Paramètres de simulation
n_projects = 5
n_years = 10
np.random.seed(42)  # Pour la reproductibilité

# Paramètres pour la simulation de Monte Carlo
S0 = 100  # Prix initial de l'actif
mu = 0.05  # Taux de rendement attendu
sigma = 0.2  # Volatilité
n = 10  # Nombre d'années
dt = 1/252  # Pas quotidien, en supposant 252 jours de trading par an
n_steps = int(n / dt)  # Nombre total de pas
n_simulations = 100  # Définir le nombre de simulations de Monte Carlo

# Génération des flux de trésorerie en millions
cash_flows = {}
volatility = {}
npv_values = {}  # Pour stocker la NPV de chaque projet

r = 0.03  # Taux d'actualisation

for i in range(n_projects):
    mean = np.random.randint(1, 5) * 1e6
    std_dev = np.random.randint(1, 2) * 1e5
    cf = np.random.normal(loc=mean, scale=std_dev, size=n_years)
    cash_flows[f"Project {i+1}"] = cf
    # Calcul de la volatilité des rendements plutôt que des valeurs monétaires
    returns = np.diff(cf) / cf[:-1]
    volatility[f"Project {i+1}"] = np.std(returns)
    npv_values[f"Project {i+1}"] = np.sum(cf / (1 + r)**np.arange(1, n_years+1))

# Affichage de la volatilité des rendements pour chaque projet
print("Volatility (Standard Deviation) of Returns for Each Project:")
for name, vol in volatility.items():
    print(f"{name}: {vol:.2%}")  # Affichage en pourcentage

# Simulation de Monte Carlo pour le prix de l'actif
price_paths = np.zeros((n_steps + 1, n_simulations))
price_paths[0] = S0

for t in range(1, n_steps + 1):
    Z = np.random.standard_normal(n_simulations)  # Générer des variations aléatoires
    price_paths[t] = price_paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

def black_scholes_call(S, K, T, r, sigma):
    """
    Calcule la valeur d'une option d'achat européenne avec le modèle de Black-Scholes
    
    :param S: Prix actuel de l'actif sous-jacent
    :param K: Prix d'exercice de l'option
    :param T: Temps restant jusqu'à l'expiration de l'option (en années)
    :param r: Taux d'intérêt sans risque
    :param sigma: Volatilité de l'actif sous-jacent
    :return: Valeur de l'option d'achat
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    return call_price

waiting_option_values = {}

for project, npv in npv_values.items():
    # Utilisons la NPV comme prix d'exercice de l'option d'attendre
    S = npv  # Prix actuel, en utilisant NPV comme approximation
    K = npv  # Prix d'exercice, NPV du projet
    sigma = volatility[project]  # Volatilité du projet
    time_to_decision = 1
    T = time_to_decision

    
    
    # Calcul de la valeur de l'option d'attendre
    option_value = black_scholes_call(S, K, T, r, sigma)
    waiting_option_values[project] = option_value /1e6

# Affichage de la valeur de l'option d'attente pour chaque projet
for project, value in waiting_option_values.items():
    print(f"Waiting option value for {project}: $M{value:.2f}")

# Visualisation des trajectoires de prix
plt.figure(figsize=(14, 8))
for i in range(n_simulations):
    plt.plot(np.linspace(0, n, n_steps + 1), price_paths[:, i], lw=1, alpha=0.2)
plt.title("Monte Carlo Simulation for Asset Price Evolution")
plt.xlabel("Years")
plt.ylabel("Asset Price")
plt.grid(True)
plt.show()

# Example decision based on NPV of a specific project
# Replace 'Project 1' with the specific project you're analyzing
if npv_values['Project 1'] > option_value:
    print("Investing immediately is more advantageous.")
else:
    print("Waiting is more advantageous.")
# Supposons que vous avez un dictionnaire `cash_flows` où la clé est le nom du projet
# et la valeur est un array des flux de trésorerie futurs pour chaque année.

# Boucle sur chaque projet pour calculer la NPV
for project, flows in cash_flows.items():
    npv = sum(cf / (1 + r)**t for t, cf in enumerate(flows, start=1))
    npv_values[project] = npv /1e6

# Affichage de la NPV pour chaque projet
for project, npv in npv_values.items():
    print(f"NPV for {project}: {npv:.2f}")