

### BIBLIOTEKI ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## ŚCIEŻKI ##

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


def rate_of_return(df, turn, investment, window): # argumenty : ramka z cenami zamknięcia, ramka z obrót/obrót max zwrotami, okres inwestycji, okres referencyjny
    result = pd.DataFrame(columns=df.columns)

    for col in df.columns:
        if col == 'Date':
            result['Date'] = df['Date'][window+investment:].reset_index(drop=True) # przesuwamy daty o okres inwestycji ponieważ wtedy stopy zwrotu zapiszą się w ostatni dzień inwestycji 
        else:
            return_values = []
            for i in range(len(df)- window):
                if pd.isna(turn[col].iloc[i]):
                    return_values.append(np.nan)
                elif not pd.isna(turn[col].iloc[i]) and i + investment <= len(df) and not pd.isna(df[col].iloc[i]) and not pd.isna(df[col].iloc[i + investment]):
                    return_values.append((df[col].iloc[i + investment] - df[col].iloc[i])/df[col].iloc[i]) 
            result[col] = pd.Series(return_values).reset_index(drop=True)
  
    return result



## RAMKI ##



prices = pd.read_excel(file_path1)
turnovers = pd.read_excel(file_path2)

prices_cleaned, turnovers_cleaned = clean_data(prices, 'KGH:PL') # Zapisane wyników ( ubyło 209 wierszy )

prices_cleaned.iloc[:, 1:] = prices_cleaned.iloc[:, 1:].applymap(lambda x: pd.to_numeric(x, errors='coerce'))

turnovers_20 = max_turnover(turnovers_cleaned, 20)
turnovers_10 = max_turnover(turnovers_cleaned, 10)
turnovers_50 = max_turnover(turnovers_cleaned, 50)

result_20 = date_max_turnovers(turnovers_cleaned, turnovers_20, 20)
result_10 = date_max_turnovers(turnovers_cleaned, turnovers_10, 10)
result_50 = date_max_turnovers(turnovers_cleaned, turnovers_50, 50)

rates_10_5 = rate_of_return(prices_cleaned, result_10, 5, 10)
rates_20_5 = rate_of_return(prices_cleaned, result_20, 5, 20)
rates_50_5 = rate_of_return(prices_cleaned, result_50, 5, 50)

rates_10_1 = rate_of_return(prices_cleaned, result_10, 1, 10)
rates_20_1 = rate_of_return(prices_cleaned, result_20, 1, 20)
rates_50_1 = rate_of_return(prices_cleaned, result_50, 1, 50)

rates_10_2 = rate_of_return(prices_cleaned, result_10, 2, 10)
rates_20_2 = rate_of_return(prices_cleaned, result_20, 2, 20)
rates_50_2 = rate_of_return(prices_cleaned, result_50, 2, 50)

rates_10_3 = rate_of_return(prices_cleaned, result_10, 3, 10)
rates_20_3 = rate_of_return(prices_cleaned, result_20, 3, 20)
rates_50_3 = rate_of_return(prices_cleaned, result_50, 3, 50)

rates_10_10 = rate_of_return(prices_cleaned, result_10, 10, 10)
rates_20_10 = rate_of_return(prices_cleaned, result_20, 10, 20)
rates_50_10 = rate_of_return(prices_cleaned, result_50, 10, 50)

dataframes = {
    "rates_10_5": rates_10_5,
    "rates_20_5": rates_20_5,
    "rates_50_5": rates_50_5,
    "rates_10_1": rates_10_1,
    "rates_20_1": rates_20_1,
    "rates_50_1": rates_50_1,
    "rates_10_2": rates_10_2,
    "rates_20_2": rates_20_2,
    "rates_50_2": rates_50_2,
    "rates_10_3": rates_10_3,
    "rates_20_3": rates_20_3,
    "rates_50_3": rates_50_3,
    "rates_10_10": rates_10_10,
    "rates_20_10": rates_20_10,
    "rates_50_10": rates_50_10
}


with pd.ExcelWriter("rates_data.xlsx", engine="openpyxl") as writer:
    for sheet_name, df in dataframes.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print("Plik Excel został zapisany z wieloma arkuszami!")