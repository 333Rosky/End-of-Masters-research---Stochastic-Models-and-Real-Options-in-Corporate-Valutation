import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import wrds
import pandas as pd
import warnings


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

# Interrogez Compustat pour obtenir les cash flows opérationnels
cash_flows_query = f"""
    select tic, datadate, fyear, oancf, ivncf, fincf
    from comp.funda
    where tic in ('{tickers_str}')
    and datafmt = 'STD'
    and consol = 'C'
    and popsrc = 'D'
    and indfmt = 'INDL'
"""
# Exécutez la requête pour obtenir les données de cash flow
cash_flows_data = db.raw_sql(cash_flows_query)

print(cash_flows_data)

def recuperer_cash_flows_tickers(tickers):
    cash_flows = pd.DataFrame()
    for ticker in tickers:
        query = f"""
        SELECT tic, datadate, fyear, oancf
        FROM comp.funda
        WHERE tic = 'HLN'
        AND indfmt = 'INDL'
        AND datafmt = 'STD'
        AND popsrc = 'D'
        AND consol = 'C'
        ORDER BY fyear
        """
        data = db.raw_sql(query)
        
        # Utilisez warnings.catch_warnings pour ignorer les FutureWarning spécifiques
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=FutureWarning)
            # Vérifiez si 'data' est non vide et ne contient pas uniquement des NA avant de concaténer
            if not data.empty and not data.isna().all().all():
                cash_flows = pd.concat([cash_flows, data], ignore_index=True)
            else:
                print("DataFrame 'data' est vide ou entièrement NA, il sera exclu de la concaténation.")
    
    print(cash_flows)
    return cash_flows

# Récupérer les cash flows pour tous les tickers du S&P 500
cash_flows_sp500 = recuperer_cash_flows_tickers(ticker_list)


# Afficher les cash flows récupérés
print(cash_flows_sp500.head())

# N'oubliez pas de fermer la connexion après avoir fini
db.close()

  
# Affichez les données pour vérification
print(cash_flows_data.head())
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
# Vérification du contenu de cash_flows
print("Keys in cash_flows:", list(cash_flows.keys()))

# Calcul déterministe de la NPV
npv_deterministic = {}
growth_rate = 0.05  # Taux de croissance annuel fixe pour l'exemple

r = 0.03  # Taux d'actualisation

# Définition des scénarios économiques
scenarios = {
    'haute_croissance': {'mu': 0.1, 'sigma': 0.15},
    'récession': {'mu': -0.02, 'sigma': 0.3},
}

# Sélection aléatoire d'un scénario
scenario_choisi = np.random.choice(list(scenarios.keys()))
params = scenarios[scenario_choisi]

# Génération des CF en fonction du scénario
cf = np.random.normal(loc=params['mu'], scale=params['sigma'], size=n_years)

for i in range(n_projects):
    mean = np.random.randint(1, 5) * 1e6
    std_dev = np.random.randint(1, 2) * 1e5
    cf = np.random.normal(loc=mean, scale=std_dev, size=n_years)
    print(f"Filling cash_flows for Project {i+1}")  # Instruction d'impression pour le débogage
    cash_flows[f"Project {i+1}"] = cf

# Affichage de la NPV déterministe pour chaque projet
print("Deterministic NPV Values:")
for project, npv in npv_deterministic.items():
    print(f"{project}: $M{npv:.2f}")

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