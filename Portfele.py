
### BIBLIOTEKI ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

### ŚCIEŻKI ##
file_path1 = "C:/Users/olgas/OneDrive/Documents/GitHub/Hight-turnover-effect-GPW/rates_data_PKO.xlsx"
file_path2 = "C:/Users/olgas/OneDrive/Documents/GitHub/Hight-turnover-effect-GPW/prices_cleaned.xlsx"
file_path3 = "C:/Users/olgas/OneDrive/Documents/GitHub/Hight-turnover-effect-GPW/GPW capitalization USD mies.xlsx"
file_path4 = "C:/Users/olgas/OneDrive/Documents/GitHub/Hight-turnover-effect-GPW/zestawienie nazw.xlsx"

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


def one_day(sygnal_df, prices_df, price, kap_min, kap_df, daily_returns):

    
    # Upewnij się, że wszystkie daty są w formacie datetime
    sygnal_df['Year'] = pd.to_datetime(sygnal_df['Date']).dt.year
    sygnal_df['Month'] = pd.to_datetime(sygnal_df['Date']).dt.month
    kap_df['Year'] = pd.to_datetime(kap_df['Date']).dt.year
    kap_df['Month'] = pd.to_datetime(kap_df['Date']).dt.month

    # Dołącz kapitalizację na podstawie roku i miesiąca
    kap_df = kap_df.drop(columns=['Date'])  # Usuń oryginalną kolumnę Date, aby uniknąć konfliktów
    merged_df = pd.merge(
        sygnal_df,
        kap_df,
        on=['Year', 'Month'],
        how='left'
    )

    sygnal_df = sygnal_df.drop(columns=['Year', 'Month'])

    # Filtrowanie ramek
    filtered_kap = [col for col in merged_df.columns if col.endswith('_y')]
    filtered_kap = merged_df[filtered_kap]
    filtered_prices = prices_df.loc[sygnal_df.index]

    # Pusta ramka na wyniki
    result = pd.DataFrame(columns=['Date', 'Mean', 'Count'])


    # Iteracja po wierszach
    for i in range(len(sygnal_df)):
        row_sum = 0
        count = 0

        for col in sygnal_df.columns:
            if col == 'Date':
                result.loc[i, 'Date'] = sygnal_df.loc[i, 'Date']
            else:
                if not pd.isna(sygnal_df[col].iloc[i]):

                    # Sprawdzamy, czy kolumna istnieje w filtered_prices
                    if col in filtered_prices.columns:
                        # Pobieramy odpowiednią wartość kapitalizacji dla konkretnego wiersza
                        kap_value = filtered_kap.loc[i, col + '_y']

                        # Sprawdzamy warunki ceny i kapitalizacji
                        if (filtered_prices[col].iloc[i] > price and
                                kap_min <= kap_value and pd.notna(kap_value)):
                            row_sum += daily_returns[col].iloc[i]
                            count += 1
                    else:
                        print(f"Kolumna {col} nie istnieje w filtered_prices, pomijam wiersz {i}")

        # Obliczanie średniej i zapis wyników
        mean = row_sum / count if count > 0 else 0
        result.loc[i, 'Mean'] = mean
        result.loc[i, 'Count'] = count

    return result



def calculate_results(sygnal_df, prices_df, price, kap_min, kap_max,  kap_df, daily_returns, length):

    
    sygnal_df['Year'] = pd.to_datetime(sygnal_df['Date']).dt.year
    sygnal_df['Month'] = pd.to_datetime(sygnal_df['Date']).dt.month
    kap_df['Year'] = pd.to_datetime(kap_df['Date']).dt.year
    kap_df['Month'] = pd.to_datetime(kap_df['Date']).dt.month

    
    kap_df = kap_df.drop(columns=['Date'])  
    merged_df = pd.merge(
        sygnal_df,
        kap_df,
        on=['Year', 'Month'],
        how='left'
    )

    sygnal_df = sygnal_df.drop(columns=['Year', 'Month'])

    # Filtrowanie ramek
    filtered_kap = [col for col in merged_df.columns if col.endswith('_y')]
    filtered_kap = merged_df[filtered_kap]
    filtered_prices = prices_df.loc[sygnal_df.index]

    # Przygotowanie ramki wyników
    result_columns = [f's{i+1}' for i in range(length)] + [f's{i+1}_c' for i in range(length)] # tworze tyle kolumn jaki będzie okres sprzedaży 
    mid_results = pd.DataFrame(columns=['Date'] + result_columns)
    mid_results['Date'] = sygnal_df.loc[1:, 'Date']

    # Iteracja po wierszach
    for i in range(length):
        j = i  # Startujemy od `i`
        while j < len(sygnal_df): # Zeby samemu kontrolowac j trzeba uzyć pętlui while 
            count = 0
            cols = []  # Lista na nazwy kolumn (nowa w każdej iteracji)

            for col in sygnal_df.columns:
                if col != 'Date' and not pd.isna(sygnal_df[col].iloc[j]):
                    if col in filtered_prices.columns:
                        kap_value = filtered_kap.loc[j, col + '_y']
                        if (filtered_prices[col].iloc[j] > price and kap_min <= kap_value <= kap_max and pd.notna(kap_value)):
                            cols.append(col)
                            count += 1

            column_name = f's{i+1}'
            counter_column = f's{i+1}_c'
            print(j)
            for k in range(length):
                if j + k < len(daily_returns):  # Upewnij się, że indeksy nie wychodzą poza zakres
                    mean = daily_returns.loc[j + k, cols].sum() / count if count > 0 else 0
                    mid_results.loc[j + k, column_name] = mean
                    mid_results.loc[j + k, counter_column] = count

            # Przechodzimy do kolejnego kroku co `length`
            j += length

    # Tworzenie ostatecznej ramki wyników
    print(mid_results)
    result = pd.DataFrame(columns=['Date', 'Mean', 'Count'])
    result['Date'] = mid_results['Date']
    mean_columns = [f's{i+1}' for i in range(length)]
    count_columns = [f's{i+1}_c' for i in range(length)]
    result['Mean'] = mid_results[mean_columns].mean(axis=1, skipna=True)
    result['Count'] = mid_results[count_columns].sum(axis=1, skipna=True)

    return result
## RAMKI DANYCH ## 

prices = pd.read_excel(file_path2)

prices.iloc[:, 1:] = prices.iloc[:, 1:].applymap(lambda x: pd.to_numeric(x, errors='coerce'))

capitalization = pd.read_excel(file_path3)

accuracy = pd.read_excel(file_path4)


sheets_dict = pd.read_excel(file_path1, sheet_name=None)

sygnals = {} # Pusty słownik do zappisywania 
for sheet_name, dataframe in sheets_dict.items():
    sygnals[sheet_name] = dataframe

# Odwoływanie sie do konkretnych ramek danych -> sygnals['rates_10_1']

columns_to_remove = accuracy.loc[accuracy['czy zgodnosc'].isnull(), 'Profesora'].tolist() # Kolumny których nie ma w mojej tabeli do usuniecia 

capitalizationv2 = capitalization.drop(columns=columns_to_remove) # usunięcie wartości których ja u siebie nie mam 

capitalizationv3 = capitalizationv2[prices.columns] # ustawienie w tej samej kolejności kolumny

daily_returns_df = daily_returns(prices)


# Do badania na szczecin wybieram spółki o cenie większej niż 0.5 i kapitalizacji większej niż 1 mln złotych 

## JEDEN ## 

# def one_day(sygnal_df, prices_df, price, kap_min, kap_max,  kap_df)

results_10_1_s = one_day(sygnals['rates_10_1'], prices, 0.5, 0, capitalizationv2, daily_returns_df)
results_20_1_s = one_day(sygnals['rates_20_1'], prices, 0.5, 0, capitalizationv2, daily_returns_df)

results_50_1_s = one_day(sygnals['rates_50_1'], prices, 0.5, 0, capitalizationv2,daily_returns_df)

# def calculate_results(sygnal_df, prices_df, price, kap_min, kap_max,  kap_df, daily_returns, length):
## TRZY ##


results_10_3_l = calculate_results(sygnals['rates_10_3'], prices, 0.5, 0, float('inf'), capitalizationv2, daily_returns_df,3)
results_20_3_l = calculate_results(sygnals['rates_20_3'], prices, 0.5, 0, float('inf'), capitalizationv2, daily_returns_df,3)

results_50_3_l = calculate_results(sygnals['rates_50_3'], prices, 0.5, 0, float('inf'), capitalizationv2, daily_returns_df,3)

## PIĘĆ ## 



results_10_5_l = calculate_results(sygnals['rates_10_5'], prices, 0.5,0, float('inf'), capitalizationv2, daily_returns_df,5)
results_20_5_l = calculate_results(sygnals['rates_20_5'], prices, 0.5, 0, float('inf'), capitalizationv2, daily_returns_df,5)

results_50_5_l = calculate_results(sygnals['rates_50_5'], prices, 0.5, 0, float('inf'), capitalizationv2, daily_returns_df,5)

## DZIESIĘĆ ##

results_10_10_s = calculate_results(sygnals['rates_10_10'], prices, 0.5,  0, float('inf'), capitalizationv2, daily_returns_df,10)
results_20_10_s = calculate_results(sygnals['rates_20_10'], prices, 0.5,  0, float('inf'), capitalizationv2, daily_returns_df, 10)

results_50_10_s = calculate_results(sygnals['rates_50_10'], prices, 0.5,  0, float('inf'), capitalizationv2, daily_returns_df, 10)



results = {
    "results_10_1_s": results_10_1_s,
    "results_20_1_s": results_20_1_s,
    "results_50_1_s": results_50_1_s,
    "results_10_3_l": results_10_3_l,
    "results_20_3_l": results_20_3_l,
    "results_50_3_l": results_50_3_l,
    "results_10_5_l": results_10_5_l,
    "results_20_5_l": results_20_5_l,
    "results_50_5_l": results_50_5_l,
    "results_10_10_s": results_10_10_s,
    "results_20_10_s": results_20_10_s,
    "results_50_10_s": results_50_10_s
}

# Ścieżka do pliku Excel
file_name = "results_Szczecin_PKO.xlsx"

# Zapisujemy dane do Excela
with pd.ExcelWriter(file_name) as writer:
    for sheet_name, df in results.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Wyniki zostały zapisane w pliku {file_name}")


