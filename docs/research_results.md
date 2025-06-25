# Research Results - Stochastic Models and Real Options in Corporate Valuation

**Author:** Romain Bastiani  
**Institution:** NEOMA Business School  
**Supervisor:** Pierre SIX  
**Date:** June 18, 2024

---

## Executive Summary

This document presents the detailed research results from the master's thesis analyzing the integration of stochastic models and real options theory in corporate valuation. The study examined 3,951 companies across 11 sectors using Monte Carlo simulations and the Black-Scholes model to evaluate investment decisions under uncertainty.

---

## Sample Characteristics

### Dataset Overview
- **Total Companies**: 3,951 companies
- **Analysis Period**: Q1 2015 to Q4 2023 (36 quarters)
- **Rows Analyzed**: 100,000 (optimized for computational efficiency)
- **Sectors**: 11 GICS sectors (codes 10-60)
- **Economic Scenarios**: Boom, Normal, and Recession

### Descriptive Statistics
- **Average Return**: -0.007458 (-0.75%)
- **Median Profitability**: -0.006965 (-0.70%)
- **Average Cumulative NPV (2015-2023)**: $7,918.88 million
- **Median Cumulative NPV**: $371.32 million
- **Average Quarterly NPV**: $417.73 million
- **Stochastic NPV Average per Quarter**: $379.70 million

---

## Sector Analysis

### Beta Values by Sector (Market Risk Sensitivity)

| Sector | GICS Code | Beta | Risk Level |
|--------|-----------|------|------------|
| Energy | 10 | 1.726 | Highest |
| Consumer Discretionary | 25 | 1.410 | High |
| Industrials | 20 | 1.313 | High |
| Materials | 15 | 1.277 | Moderate-High |
| Information Technology | 45 | 1.275 | Moderate-High |
| Healthcare | 35 | 1.269 | Moderate-High |
| Real Estate | 60 | 1.123 | Moderate |
| Financials | 40 | 1.016 | Moderate |
| Consumer Staples | 30 | 0.827 | Low |
| Utilities | 55 | 0.591 | Lowest |

### Option Value Performance by Sector

#### Expansion Options (% Difference from Deterministic NPV)

| Sector | Mean % Diff | Median % Diff | Growth Potential |
|--------|-------------|---------------|------------------|
| Information Technology | 14.39% | 7.75% | Excellent |
| Industrials | 8.53% | 8.70% | Very Good |
| Financials | 6.32% | 8.62% | Good |
| Materials | 3.70% | 9.47% | Good |
| Real Estate | 3.69% | 7.43% | Good |
| Consumer Staples | 3.12% | 6.88% | Moderate |
| Energy | 3.04% | -8.37% | Volatile |
| Utilities | 2.74% | -6.69% | Variable |
| Healthcare | -3.64% | -5.31% | Limited |
| Consumer Discretionary | -9.10% | 8.53% | Highly Variable |

---

## Hypothesis Testing Results

### H1: Interest Rate Impact on NPV ✅ **CONFIRMED**
- **Finding**: Non-linear relationship with diminishing returns
- **Normal Conditions**: Coefficient = -235.17 (t-stat = -0.860)
- **Recession Conditions**: Coefficient = -358.01 (stronger negative impact)
- **Interpretation**: Initial rate decreases significantly boost NPV, but further reductions show diminishing returns

### H2: Volatility and Option Values ❌ **REJECTED**
- **Finding**: Negative relationship between volatility and NPV
- **Coefficient**: -0.113 (t-stat = -3.911)
- **Interpretation**: Higher volatility decreases NPV, contrary to initial hypothesis
- **Revised Understanding**: Uncertainty reduces valuations rather than enhancing option values

### H3: Cash Flows and NPV ✅ **CONFIRMED**
- **Finding**: Strong positive correlation (0.999) between operating cash flows and NPV
- **Coefficient**: 1.9999 (t-stat = 475.457)
- **Economic Downturns**: Relationship weakens during recessions
- **Interpretation**: Cash flow management is critical for value creation

### H4: Interest Rates and Abandonment Options ✅ **CONFIRMED**
- **Finding**: Higher interest rates increase abandonment likelihood
- **Mechanism**: Rising rates reduce NPV, making abandonment more attractive
- **Strategic Implication**: Companies should monitor rate environments for exit decisions

### H5: Market Returns and Beta ✅ **CONFIRMED**
- **Finding**: Higher market returns correlate with higher betas
- **Coefficient**: 2.2922 (t-stat = 0.681)
- **Recession Effect**: Relationship more pronounced during economic downturns
- **Risk Management**: High-beta companies need enhanced risk strategies

### H6: Option Maturity and Value ✅ **CONFIRMED**
- **Finding**: Longer maturity options have higher values
- **Expansion Options**: Coefficients increase with maturity (2.379 to 3.597)
- **Abandonment Options**: Positive but decreasing coefficients (1.998 to 1.490)
- **Strategic Planning**: Long-term flexibility creates value

### H7: Stationary Cash Flows ✅ **CONFIRMED**
- **Statistical Test**: Augmented Dickey-Fuller Test
- **ADF Statistic**: -10.084426
- **P-value**: < 0.001 (highly significant)
- **Interpretation**: Stationary cash flows enable reliable NPV predictions

---

## Regression Analysis Results

### Model Performance
- **Multiple R**: 0.89 (strong positive correlation)
- **Adjusted R²**: 0.88 (88% variance explained)
- **Standard Error**: 1,730 (acceptable for financial data scale)
- **F-Significance**: p < 0.05 (statistically significant model)

### Key Regression Coefficients

| Variable | Coefficient | t-Statistic | Significance | Interpretation |
|----------|-------------|-------------|--------------|----------------|
| Operating Cash Flow (OANCFY) | 1.9999 | 475.457 | *** | Strong positive driver of NPV |
| Interest Rate | -235.17 | -0.860 | | Negative impact, stronger in recessions |
| Volatility | -0.113 | -3.911 | *** | Reduces NPV contrary to expectations |
| Beta | 2.2922 | 0.681 | | Market-sensitive firms have higher NPVs |

### Option Coefficients by Maturity

#### Expansion Options
- **3 months**: 2.379
- **12 months**: 2.683
- **60 months**: 2.947
- **96 months**: 2.993
- **120 months**: 3.142
- **180 months**: 3.597

#### Abandonment Options
- **3 months**: 1.998
- **12 months**: 2.031
- **60 months**: 1.933
- **96 months**: 1.810
- **120 months**: 1.845
- **180 months**: 1.490

---

## Economic Scenario Analysis

### Normal Economic Conditions
- Standard coefficients apply
- Balanced growth and abandonment option values
- Predictable relationships between variables

### Recession Conditions
- **Interest Rate Impact**: -358.01 (vs -235.17 normal)
- **Volatility Impact**: -0.284 (vs -0.113 normal)
- **Option Values**: Expansion options decline, abandonment options retain value
- **Strategic Implication**: Focus on flexibility and downside protection

### Boom Conditions
- Enhanced expansion option values
- Reduced abandonment option relevance
- Increased emphasis on growth opportunities

---

## Correlation Analysis

### Strong Correlations (>0.9)
- **Operating Cash Flows ↔ Deterministic NPV**: 0.9999
- **Operating Cash Flows ↔ Stochastic NPV**: 0.9986
- **Option Values ↔ Deterministic NPV**: >0.92
- **Cash Flows ↔ Volatility**: 0.9991

### Moderate Correlations (0.4-0.7)
- **Volatility ↔ Deterministic NPV**: 0.562
- **Volatility ↔ Stochastic NPV**: 0.521
- **Beta ↔ Volatility**: 0.413

### Weak Correlations (<0.3)
- **Interest Rate ↔ NPV**: -0.187
- **Beta ↔ NPV**: 0.211

---

## Multicollinearity Assessment

### Variance Inflation Factors (VIF)
- **Interest Rate**: 3.57 (acceptable)
- **Volatility**: 3.46 (acceptable)
- **OANCFY**: 1.46 (low)
- **OANCFY Mean**: 1.23 (low)
- **Beta**: 0.00 (no issues)
- **Option Values**: 8.93-10.23 (moderate, expected due to similar inputs)

### Interpretation
- Most variables show acceptable multicollinearity levels
- Option value correlations expected due to shared underlying factors
- Model reliability confirmed by low VIF values for key variables

---

## Key Insights and Implications

### 1. Stochastic vs. Deterministic NPV
- **Finding**: Stochastic NPV consistently lower than deterministic NPV
- **Implication**: Traditional NPV may overestimate project values
- **Recommendation**: Incorporate uncertainty explicitly in valuations

### 2. Sector-Specific Strategies
- **Technology Sector**: Strong expansion potential, pursue growth options
- **Energy Sector**: High volatility, focus on risk management
- **Utilities**: Low beta, suitable for stable cash flow strategies
- **Healthcare**: Limited expansion benefits, focus on operational efficiency

### 3. Economic Environment Adaptation
- **Recession**: Prioritize abandonment options and cash flow stability
- **Normal**: Balanced approach to growth and risk management
- **Boom**: Emphasize expansion options and growth investments

### 4. Strategic Flexibility Value
- **Long-term Options**: Higher values justify extended planning horizons
- **Real Options Approach**: Superior to traditional NPV for strategic decisions
- **Timing Importance**: Market conditions significantly impact option values

---

## Limitations and Future Research

### Current Limitations
1. **Model Complexity**: Sophisticated models require extensive data and expertise
2. **Assumption Dependency**: Normal distribution assumptions may not hold
3. **Sector Aggregation**: Cross-sector analysis may obscure industry-specific patterns
4. **Market Efficiency**: Assumes liquid markets for real options pricing

### Future Research Directions
1. **Machine Learning Integration**: Neural networks for cash flow prediction
2. **Behavioral Finance**: Incorporate management decision biases
3. **Industry-Specific Models**: Develop sector-tailored approaches
4. **Real-Time Applications**: Dynamic updating with market data

---

## Practical Applications

### For Corporate Managers
1. **Investment Timing**: Use interest rate environment for optimal timing
2. **Portfolio Management**: Balance expansion and abandonment options
3. **Risk Assessment**: Incorporate stochastic modeling in evaluations
4. **Strategic Planning**: Leverage long-term option values

### For Financial Analysts
1. **Valuation Enhancement**: Combine deterministic and stochastic approaches
2. **Sector Analysis**: Apply sector-specific beta and volatility factors
3. **Scenario Planning**: Model different economic conditions
4. **Risk Communication**: Use probabilistic NPV ranges

### For Academic Research
1. **Methodology Validation**: Confirm results across different datasets
2. **Model Extension**: Develop more sophisticated stochastic processes
3. **Empirical Testing**: Validate real options theory in various contexts
4. **Interdisciplinary Applications**: Apply to other business domains

---

*Document Version: 1.0*  
*Last Updated: June 18, 2024*  
*Contact: Romain Bastiani, NEOMA Business School* 