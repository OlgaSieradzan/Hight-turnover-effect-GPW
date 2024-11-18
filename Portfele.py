
### BIBLIOTEKI ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### ŚCIEŻKI ##
file_path1 = "C:/Users/olgas/OneDrive/Documents/GitHub/Hight-turnover-effect-GPW/rates_data/rates_data.xlsx"

## FUNKCJE ##

def daily_returns(df):
    result = pd.DataFrame(columns=df.columns)  # Nowa ramka danych do przechowywania wyników

    for col in df.columns:
        if col == 'Date':
            
            result['Date'] = df['Date'][1:].reset_index(drop=True)
        else:
            # Oblicz dzienne stopy zwrotu
            rates_values = []  # Pusta lista na dzienne stopy zwrotu
            for i in range(len(df) - 1):
                rate = (df[col].iloc[i + 1] - df[col].iloc[i]) / df[col].iloc[i]
                rates_values.append(rate)  # Dodaj wynik do listy

            result[col] = pd.Series(rates_values).reset_index(drop=True)

    return result