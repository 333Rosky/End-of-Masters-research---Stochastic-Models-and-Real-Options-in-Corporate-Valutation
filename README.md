# Stochastic Models and Real Options in Corporate Valuation

## Master's Thesis - Corporate Finance and International Banking

**Author:** Romain Bastiani  
**Institution:** NEOMA Business School  
**Supervisor:** Pierre SIX  
**Date:** June 18, 2024

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Research Objectives](#research-objectives)
3. [Methodology](#methodology)
4. [Project Structure](#project-structure)
5. [Installation & Setup](#installation--setup)
6. [Usage](#usage)
7. [Data Sources](#data-sources)
8. [Key Features](#key-features)
9. [Results](#results)
10. [Academic References](#academic-references)
11. [License](#license)

---

## Project Overview

This research investigates the integration of **stochastic and deterministic aspects** in financial simulations for company valuation using real options theory. Monte Carlo simulations are employed to construct underlying processes for calculating net present value (NPV), considering both predictable and unpredictable factors. The study emphasizes the use of real options theory to evaluate investment possibilities and divestment choices, underlining the importance of flexibility and adaptability in corporate finance.

### Primary Research Question
**"How do stochastic and deterministic methods, along with the integration of real options, influence the net present value (NPV) of a company, and what are the implications of these methods for corporate investment decisions?"**

### Key Findings
- Interest rates have a greater negative influence on NPV during recessions, increasing abandonment likelihood
- Volatility negatively impacts NPV, showing that greater uncertainty results in lower valuations
- Organizations with higher market risk exhibit greater responsiveness to market conditions
- Options with longer maturities generally hold higher values
- Stochastic NPV is lower than deterministic NPV on average, highlighting uncertainty's importance

---

## Research Objectives

### Primary Objectives
1. **Combine stochastic models, deterministic approaches, and real options theory** to create a comprehensive investment evaluation framework
2. **Implement Monte Carlo simulations** to model cash flow uncertainty and provide probabilistic insights
3. **Apply Black-Scholes model** to evaluate real options for expansion and abandonment decisions
4. **Analyze performance across three economic scenarios**: boom, normal, and recession conditions

### Research Hypotheses Tested
- H1: Interest rate reductions have non-linear effects on NPV with diminishing returns
- H2: High NPV volatility correlates positively with expansion option values
- H3: Higher operating cash flows consistently show higher NPVs (weakens during downturns)
- H4: Higher interest rates increase abandonment option exercise likelihood
- H5: Companies with higher market returns have higher betas (more pronounced during recessions)
- H6: Options with longer maturities consistently have higher values
- H7: Companies with stationary cash flows enable more reliable NPV predictions

---

## Methodology

### Theoretical Framework
- **Real Options Theory**: Valuing flexibility and strategic decisions
- **Stochastic Processes**: Modeling uncertain cash flows and interest rates
- **Monte Carlo Simulation**: Generating multiple scenarios for risk assessment
- **Net Present Value (NPV)**: Traditional and risk-adjusted approaches

### Data Analysis Approach
1. **Data Collection**: Historical financial data from WRDS (Compustat/CRSP)
2. **Interest Rate Analysis**: US Treasury rates as risk-free benchmarks
3. **Statistical Modeling**: Stochastic cash flow simulation
4. **Comparative Analysis**: Traditional vs. stochastic valuation methods

---

## Project Structure

```
End-of-Masters-research---Stochastic-Models-and-Real-Options-in-Corporate-Valutation/
│
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
│
├── src/                              # Source code
│   ├── main.py                       # Main analysis script
│   ├── plotting.py                   # Visualization functions
│   ├── data_processing.py            # Data cleaning and processing
│   └── monte_carlo.py                # Monte Carlo simulation engine
│
├── data/                             # Data files
│   ├── raw/                          # Original data files
│   │   └── US_Interest_Rate.xlsx     # US Treasury rates
│   ├── processed/                    # Cleaned and processed data
│   │   ├── Cash_Flows_Entreprises_with_NPV.xlsx
│   │   └── Cash_Flows_with_NPV_and_Rates.xlsx
│   └── external/                     # External data sources
│
├── results/                          # Analysis results
│   ├── figures/                      # Generated plots and charts
│   ├── tables/                       # Summary statistics and tables
│   └── models/                       # Saved model outputs
│
├── docs/                             # Documentation
│   ├── methodology.md                # Detailed methodology
│   ├── data_description.md           # Data dictionary
│   └── technical_notes.md            # Technical implementation notes
│
├── logs/                             # Log files
│   └── monte_carlo_simulations.log   # Simulation logs
│
└── thesis/                           # Thesis-related documents
    ├── chapters/                     # Thesis chapters
    ├── references/                   # Bibliography and references
    └── appendices/                   # Additional materials
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- WRDS account (for data access)
- Excel for data visualization (optional)

### Required Python Packages
```bash
pip install -r requirements.txt
```

### WRDS Configuration
1. Create a WRDS account at [wrds-www.wharton.upenn.edu](https://wrds-www.wharton.upenn.edu)
2. Configure your credentials in the script or environment variables
3. Ensure access to Compustat and CRSP databases

---

## Usage

### Basic Analysis
```bash
# Run the main analysis
python src/main.py

# Generate visualizations
python src/plotting.py
```

### Advanced Options
```bash
# Run with custom parameters
python src/main.py --simulations 5000 --periods 10

# Generate specific company analysis
python src/main.py --company "AAPL" --detailed-output
```

### Jupyter Notebooks
Interactive analysis notebooks are available in the `notebooks/` directory for detailed exploration.

---

## Data Sources

### Primary Data Sources
1. **WRDS (Wharton Research Data Services)**
   - Compustat Fundamentals: Financial statement data
   - CRSP: Stock price and market data
   - Coverage: 2015-2023

2. **Federal Reserve Economic Data (FRED)**
   - US Treasury Bill Rates (3-month)
   - Risk-free rate proxies

### Data Quality and Limitations
- Data filtered for consistency and completeness
- Missing values handled through interpolation where appropriate
- Sample bias considerations documented in methodology

---

## Key Features

### 🔄 Stochastic Modeling
- Monte Carlo simulation engine with customizable parameters
- Multiple probability distributions for cash flow modeling
- Sensitivity analysis capabilities

### 📊 Comprehensive Analysis
- Traditional NPV calculations with deterministic cash flows
- Risk-adjusted NPV with stochastic components
- Comparative analysis framework

### 📈 Advanced Visualizations
- Interactive plots for scenario analysis
- Statistical distribution visualizations
- Time-series analysis of financial metrics

### 🔧 Robust Data Processing
- Automated data cleaning and validation
- Integration with major financial databases
- Scalable processing for large datasets

---

## Results

### Key Research Findings

1. **Stochastic vs. Deterministic Valuation**
   - Stochastic NPV is generally lower than deterministic NPV
   - Strong positive correlation (0.999) between operating cash flows and NPV
   - Regression model explains 88% of NPV variance (Adjusted R² = 0.88)

2. **Interest Rate Impact Analysis**
   - Negative correlation (-0.187) between interest rates and NPV
   - Stronger negative impact during economic recessions (-358.01 coefficient)
   - Non-linear relationship with diminishing returns at lower rates

3. **Sector-Specific Analysis (Beta Values)**
   - Energy: 1.726 (highest market sensitivity)
   - Utilities: 0.591 (lowest market sensitivity)
   - Information Technology: Strong expansion potential (14.39% avg difference)
   - Healthcare: Limited expansion benefits (-3.64% avg difference)

4. **Real Options Valuation**
   - Expansion options: Higher values with longer maturities
   - Abandonment options: Positive but diminished effect during downturns
   - Strong correlation (>0.92) between option values and deterministic NPV

5. **Risk and Volatility**
   - Negative relationship between volatility and NPV (-0.113 coefficient)
   - Higher beta companies more responsive to market conditions
   - Stationary cash flows enable more reliable NPV predictions (ADF test p-value < 0.001)

### Statistical Summary
- **Sample Size**: 3,951 companies (analyzed first 100,000 rows for computational efficiency)
- **Time Period**: Q1 2015 to Q4 2023 (36 quarters)
- **Sectors Covered**: 11 GICS sectors (codes 10-60)
- **Simulation Runs**: 1,000+ Monte Carlo iterations per company
- **Data Sources**: WRDS (Compustat/CRSP) and FRED
- **Adjusted R²**: 88% variance explained by the regression model
- **Option Maturities**: 3 months, 1 year, 2 years, 5 years, 10 years, 15 years

---

## Academic References

### Core Literature
1. **Berk, J., & DeMarzo, P. (2023).** *Corporate Finance, 6th Global Edition.* Pearson Education.
2. **Hull, J. (2023).** *Options, Futures, and Other Derivatives.* Pearson Education.
3. **Lautier, D. (2001).** *Les Options Réelles: Une idée séduisante - Un concept utile et multiforme - Un instrument facile à créer mais difficile à valoriser.* CEREG, Université Paris IX.
4. **Dixit, A. K., & Pindyck, R. S. (1994).** *Investment Under Uncertainty.* Princeton University Press.
5. **Black, F., & Scholes, M. (1973).** *The Pricing of Options and Corporate Liabilities*
6. **Merton, R. C. (1973).** *Theory of Rational Option Pricing*

### Specialized Research
- **Amram, M., & Kulatilaka, N. (2000).** *Strategy and Shareholder Value Creation: The Real Options Frontier.* Journal of Applied Corporate Finance
- **Tadeu, H. F. B., & Silva, J. T. M. (2014).** *Real Options Theory: An Alternative Methodology Applicable to Investment Analyses in R & D Projects.* Australian Journal of Basic and Applied Sciences
- **Li X., & Johnson, J.D. (2002).** *Evaluate IT Investment Opportunities Using Real Options Theory*
- **Aderibigbe, A. (2014).** *A Term Paper on Monte Carlo Analysis/Simulation.* University of Ibadan.

---

## Technical Implementation

### Software Architecture
- **Object-oriented design** for maintainable code
- **Modular structure** for easy testing and extension
- **Error handling** and logging for robust execution

### Performance Optimization
- Vectorized operations using NumPy
- Parallel processing for Monte Carlo simulations
- Memory-efficient data handling for large datasets

---

## Future Research Directions

1. **Machine Learning Integration**
   - Neural networks for cash flow prediction
   - Deep learning approaches to option pricing

2. **Real-time Analysis**
   - Live data feeds and dynamic updating
   - Real-time risk monitoring dashboards

3. **Extended Market Coverage**
   - International markets and currencies
   - Emerging market applications

---

## Contributing

This project is part of a master's thesis research. For academic collaboration or questions:

- **Author**: Romain Bastiani
- **Institution**: NEOMA Business School - MSc Corporate Finance
- **GitHub**: https://github.com/333Rosky
- **Repository**: https://github.com/333Rosky/End-of-Masters-research---Stochastic-Models-and-Real-Options-in-Corporate-Valutation

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Academic Use**: Please cite this work in academic publications:
```
Bastiani, R. (2024). Stochastic Models and Real Options in Corporate Valuation. 
Master's Thesis, NEOMA Business School, Rouen, France.
Available at: https://github.com/333Rosky/stochastic-real-options
```

---

## Acknowledgments

- **Thesis Supervisor**: Pierre SIX (Associate Professor, NEOMA Business School) for invaluable guidance, support, and expertise in corporate finance
- **Academic Institution**: NEOMA Business School for providing an exceptional educational environment and research facilities
- **Data Providers**: WRDS (Wharton Research Data Services) for access to Compustat and CRSP databases, and FRED for interest rate data
- **Family**: For continuous love, encouragement, and support throughout the academic journey
- **Python Community**: For excellent open-source tools enabling advanced financial modeling

---

*Last Updated: June 18, 2024* 
