# Thesis - Analysis of the Total Equity PCR in a Factor Model
### Sections
1. Introduction and "State of the Union"
2. Introduction to the PCR
    - PCR as a sentiment indicator
    - Correlation to market returns (Pearson)
    - PCR compared to other FF factors (multicolinearity - is there a test?)
3. Model Creation
    - Multiple linear regression (3 and 5 factor FF)
    - Ridge Regression
    - for t from t and t+1 from t
4. Practical Applications
    - Using the PCR in a trading model (trading indicator)
5. Discussion and Results
6. Conclusion
    - Provides some explainability in returns?
---
- [ ] Model Creation
    - [x] Gather Data
        - [x] Get FF Factors
        - [x] Get PCR data
        - [x] Get list of tickers
            - [x] SP500 Con.
            - [ ] small and mid caps
        - [x] Get data for SP500 con.
        - [x] Get data for benchmark indices (total US and SP500)
        - [x] Save tickers and index closing data to csv file
    - [ ] Multiple Linear Regression t to t
        - [ ] t to t+1
    - [ ] Ridge Regression
        - [ ] t to t+1
- [ ] Backtest/trading strategy results
