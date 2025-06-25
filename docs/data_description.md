# Data Dictionary - Stochastic Financial Modeling Project

## Overview
This document provides detailed descriptions of all datasets, variables, and data sources used in the stochastic financial modeling analysis.

---

## Primary Datasets

### 1. Company Financial Data (Compustat via WRDS)

**Source**: Wharton Research Data Services (WRDS) - Compustat Fundamentals Quarterly
**File Location**: `data/processed/Cash_Flows_Entreprises_with_NPV.xlsx`
**Time Period**: 2015 Q1 - 2023 Q4
**Frequency**: Quarterly
**Sample Size**: [X] companies, [Y] observations

#### Variables

| Variable | Description | Data Type | Source | Units |
|----------|-------------|-----------|---------|-------|
| `gvkey` | Global Company Key (unique identifier) | String | Compustat | - |
| `conm` | Company Name | String | Compustat | - |
| `datadate` | Data Date (end of fiscal quarter) | Date | Compustat | YYYY-MM-DD |
| `fqtr` | Fiscal Quarter | Integer | Compustat | 1,2,3,4 |
| `oancfy` | Operating Cash Flow (Annual) | Numeric | Compustat | USD Million |
| `Quarter` | Calendar Quarter | String | Derived | YYYY-QX |

#### Data Quality Notes
- **Missing Values**: Handled via listwise deletion
- **Outliers**: Winsorized at 1st and 99th percentiles
- **Currency**: All amounts in USD millions
- **Fiscal vs Calendar**: Adjusted to calendar quarters for consistency

---

### 2. Interest Rate Data (Federal Reserve)

**Source**: Federal Reserve Economic Data (FRED)
**File Location**: `data/raw/US_Interest_Rate.xlsx`
**Time Period**: 2015-01-01 to 2023-12-31
**Frequency**: Daily (aggregated to quarterly)

#### Variables

| Variable | Description | Data Type | Source | Units |
|----------|-------------|-----------|---------|-------|
| `observation_date` | Date of observation | Date | FRED | YYYY-MM-DD |
| `DTB3` | 3-Month Treasury Bill Rate | Numeric | FRED | Decimal (%) |
| `Quarter` | Calendar Quarter | String | Derived | YYYY-QX |
| `interest_rate` | Quarterly Average Rate | Numeric | Calculated | Decimal |

#### Processing Steps
1. **Daily to Quarterly**: Arithmetic mean of daily rates within each quarter
2. **Percentage Conversion**: Converted from percentage to decimal format
3. **Missing Values**: Linear interpolation for weekends/holidays

---

### 3. Calculated NPV Data

**File Location**: `data/processed/Cash_Flows_with_NPV_and_Rates.xlsx`
**Description**: Enhanced dataset with calculated NPV metrics

#### Additional Variables

| Variable | Description | Formula | Data Type | Units |
|----------|-------------|---------|-----------|-------|
| `npv` | Net Present Value (Traditional) | `Σ(CF_t / (1+r)^t)` | Numeric | USD Million |
| `Mean_NPV` | Average NPV by Company | `mean(npv)` by gvkey | Numeric | USD Million |
| `SD_NPV` | Standard Deviation of NPV | `std(npv)` by gvkey | Numeric | USD Million |
| `Simulated_Mean_NPV` | Monte Carlo Mean NPV | From simulations | Numeric | USD Million |
| `Simulated_SD_NPV` | Monte Carlo SD NPV | From simulations | Numeric | USD Million |

---

## Derived Variables and Calculations

### NPV Calculation Parameters
- **Discount Rate**: Quarterly US 3-Month Treasury Rate
- **Cash Flow Period**: 1 Quarter (t=1)
- **Initial Investment**: Assumed as 0 for operating cash flows

### Monte Carlo Simulation Parameters
- **Simulation Runs**: 1,000 per company
- **Distribution**: Normal distribution of cash flows
- **Parameters**: 
  - Mean: Historical average cash flow per company
  - Standard Deviation: Historical cash flow volatility per company

---

## Data Processing Pipeline

### 1. Raw Data Ingestion
```
WRDS API → Raw Compustat Data
FRED API → Raw Interest Rate Data
```

### 2. Data Cleaning
```python
# Missing value treatment
df = df.dropna(subset=['oancfy'])

# Outlier treatment (example)
Q1 = df['oancfy'].quantile(0.01)
Q3 = df['oancfy'].quantile(0.99)
df = df[(df['oancfy'] >= Q1) & (df['oancfy'] <= Q3)]
```

### 3. Variable Creation
```python
# Quarter creation
df['Quarter'] = df['datadate'].dt.to_period('Q')

# Interest rate mapping
df['interest_rate'] = df['Quarter'].map(interest_rate_dict)

# NPV calculation
df['npv'] = df.apply(lambda row: calculate_npv(row, interest_rate_dict), axis=1)
```

### 4. Aggregation and Statistics
```python
# Company-level statistics
df['Mean_NPV'] = df.groupby('gvkey')['npv'].transform('mean')
df['SD_NPV'] = df.groupby('gvkey')['npv'].transform('std')
```

---

## Data Quality Assessment

### Completeness
- **Financial Data**: 95%+ completeness after cleaning
- **Interest Rate Data**: 100% completeness (interpolated where necessary)
- **Company Names**: 100% availability

### Consistency
- **Time Alignment**: All data aligned to calendar quarters
- **Currency Units**: Standardized to USD millions
- **Date Formats**: ISO 8601 standard (YYYY-MM-DD)

### Accuracy
- **Cross-Validation**: Sample checked against Bloomberg/Yahoo Finance
- **Outlier Detection**: 3-sigma rule applied
- **Range Checks**: Logical bounds verified

---

## Sample Characteristics

### Geographic Distribution
- **Country**: United States only
- **Exchanges**: NYSE, NASDAQ, AMEX
- **Market Cap**: All sizes (micro-cap to mega-cap)

### Temporal Distribution
- **Full Period**: 2015 Q1 - 2023 Q4 (36 quarters)
- **Peak Observations**: 2018-2019 (pre-COVID)
- **Volatility Period**: 2020-2021 (COVID impact)

### Industry Distribution
Based on GICS sector classification:
- Technology: X%
- Healthcare: X%
- Financial Services: X%
- Consumer Discretionary: X%
- [Additional sectors...]

---

## Usage Guidelines

### 1. Data Access
- **File Formats**: Excel (.xlsx), CSV available on request
- **Loading**: Use `pandas.read_excel()` for Python analysis
- **Memory**: Large files may require chunked processing

### 2. Variable Selection
- **Primary Analysis**: Use `oancfy`, `interest_rate`, `npv`
- **Time Series**: Use `datadate` for temporal analysis
- **Cross-Sectional**: Use `gvkey` for company-specific analysis

### 3. Known Limitations
- **Survivorship Bias**: Only includes companies active throughout period
- **Reporting Lag**: Financial data has ~45-90 day reporting delay
- **Currency Effects**: No adjustment for inflation or exchange rates

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | [Date] | Initial data dictionary | [Your Name] |
| 1.1 | [Date] | Added simulation variables | [Your Name] |

---

## Contact Information

For questions about data sources, variable definitions, or access:
- **Primary Contact**: [Your Email]
- **WRDS Support**: wrds-support@wharton.upenn.edu
- **Technical Issues**: [GitHub Issues Link]

---

*Last Updated: [Date]* 