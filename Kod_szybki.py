import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path1 = "C:/Users/olgas/OneDrive/Pulpit/studia/Praca dyplomowa/Dane/GPW day colse adj USD.xlsx"
file_path2 = "C:/Users/olgas/OneDrive/Pulpit/studia/Praca dyplomowa/Dane/GPW day turnover USD.xlsx"

## FUNKCJE ##
def clean_data(df, determinant) :
    missing_values = df[df[determinant].isna()]['Date'].tolist() #Stworzenie listy gdzie np. KGHM nie ma odczytów z giełdy
    prices_cl = prices[~prices['Date'].isin(missing_values)]
    turnovers_cl = turnovers[~turnovers['Date'].isin(missing_values)]
    return prices_cl, turnovers_cl


def max_turnover(df, window):
    result = pd.DataFrame(columns=df.columns) # Pusty df do wypełnienia
       
    for col in df.columns:
        if col == 'Date':
            result['Date'] = df['Date'][window-1:].reset_index(drop=True)
        else:
            
            max_values = [] # Pusta lista którą póżniej wypełnimy maksymalnymi wartościami
            for i in range(len(df) - window + 1): # Indeksowanie od 0 dlatego +1
                window_data = df[col][i:i+window] # Wybieram dane np. od 0 do 19 
                if window_data.isna().any():
                    max_values.append(np.nan) # Jeżeli w tych 20 danych jest NA to dodaje NA
                else:
                    max_values.append(window_data.max()) # W przeciwnym przypadku dodaje maksymalną wartośc z tych np. 20 dni
            
            result[col] = pd.Series(max_values)# Zapisujemy obliczone wartości do nowej kolumny
    
    return result


def date_max_turnovers(df, turn, window): # argimenty to : pierwotna tabela/ taleba z maxami / okres referencyjny
    result = pd.DataFrame(columns=df.columns) # Pusty df do wypełnienia
    
   
    
    for col in df.columns:
        if col == 'Date':
            result['Date'] = df['Date'][window:].reset_index(drop=True)
        else:
            max_values = [] # max values na początku każdej iteracji po kolumnach powinna być pusta
            for i in range(len(df)- window):
                if df[col].iloc[i + window] > turn[col].iloc[i]:
                    max_values.append(df[col].iloc[i + window]/turn[col].iloc[i])
                else :
                    max_values.append(np.nan)
            result[col] = pd.Series(max_values).reset_index(drop=True)
  
    return result



## RAMKI ##

prices = pd.read_excel(file_path1)
turnovers = pd.read_excel(file_path2)
prices_cleaned, turnovers_cleaned = clean_data(prices, 'KGH:PL') # Zapisane wyników ( ubyło 209 wierszy )
turnovers_20 = max_turnover(turnovers_cleaned, 20)
turnovers_10 = max_turnover(turnovers_cleaned, 10)
turnovers_50 = max_turnover(turnovers_cleaned, 50)
result_20 = date_max_turnovers(turnovers_cleaned, turnovers_20, 20)
result_10 = date_max_turnovers(turnovers_cleaned, turnovers_10, 10)
result_50 = date_max_turnovers(turnovers_cleaned, turnovers_50, 50)
