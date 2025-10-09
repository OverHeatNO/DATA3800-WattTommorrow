# DATA3800-WattTomorrow
Semester project for DATA3800 - Data Science with Scripting

## What is left to do:
- Make script for getting energy_makeup
- Make script for getting energy_price
- Make script for getting natural resource price
- Make script for getting weather data
- (Wish) We want it to be so that you can get the newest data somehow. Like get only the data for for example yesterday in all the categories
- Data exploration
- Data feature selection
- Model training
- Model evaluation
- "Fast API" for access of our trained prediction model
- Make Rag/GPT. Use "gradio api" for interface
- Making report on our findings



## Package instalation with pip in venv
| Library        | Purpose                                                                               |
| -------------- | ------------------------------------------------------------------------------------- |
| **meteostat**  | For accessing historical weather and climate data (e.g., temperature, precipitation). |
| **pandas**     | Data manipulation and analysis.                                                       |
| **numpy**      | Numerical operations on arrays and matrices.                                          |
| **yfinance**   | Fetch financial and stock market data from Yahoo Finance.                             |
| **seaborn**    | Statistical data visualization (works with Matplotlib).                               |
| **matplotlib** | Core plotting and graphing library.                                                   |
| **kagglehub**  | For downloading datasets from Kaggle programmatically.                                |
| **entsoe-py**  | Access to ENTSO-E (European electricity market) data.                                 |


```
pip install meteostat pandas numpy yfinance seaborn matplotlib kagglehub entsoe-py
```