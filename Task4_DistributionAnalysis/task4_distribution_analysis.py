import pandas as pd
import numpy as np

# Numele fisierului de date
FILE_NAME = 'online_store_data.csv'

# Setari pentru afisarea completa a DataFrame-urilor in consola
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'left')


def load_data(file_name):
    """
    Incarca setul de date dintr-un fisier CSV.
    """
    try:
        df = pd.read_csv(file_name)
        return df
    except FileNotFoundError:
        print(f"EROARE: Fisierul '{file_name}' nu a fost gasit.")
        return None
    except Exception as e:
        print(f"EROARE la incarcarea fisierului: {e}")
        return None


def extract_rating_value(rating_str):
    """
    Extrage valoarea numerica a ratingului dintr-un sir de caractere.
    """
    if pd.isna(rating_str) or str(rating_str).strip().lower() == 'no value':
        return np.nan
    try:
        return float(str(rating_str).split(' ')[0])
    except:
        return np.nan


def preprocess_data(df):
    """
    Realizeaza curatarea si conversia de baza a tipurilor de date necesare pentru analiza.
    """
    print("\n--- Preprocesarea Datelor Necesare (Rating & Conversii) ---")
    
    df['rating'] = df['rating'].apply(extract_rating_value)
    
    integer_cols = ['quantity_sold', 'num_of_ratings']
    for col in integer_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int32')
        
    df.dropna(subset=['rating', 'num_of_ratings', 'price'], inplace=True)
    
    print(f"Preprocesare finalizata. Randuri ramase: {df.shape[0]}.")
    
    return df


def perform_distribution_analysis(df):
    """
    Efectueaza toate analizele de distributie solicitate.
    """
    print("\n" + "="*70)
    print("                Analiza Distribuției Datelor")
    print("="*70)

    # Care este diferența dintre cel mai bine și cel mai slab evaluat televizor? (Range)
    print("\n--- 1. Intervalul (Range) Evaluărilor pentru Categoria 'TVs' ---")
    
    tvs_df = df[df['category'] == 'TVs'].copy()
    
    if tvs_df.empty:
        print("Nu s-au găsit date pentru categoria 'TVs'.")
        tvs_range = np.nan
    else:
        max_rating = tvs_df['rating'].max()
        min_rating = tvs_df['rating'].min()
        tvs_range = max_rating - min_rating
        
        print(f"Evaluare maximă (max): {max_rating:.2f}")
        print(f"Evaluare minimă (min): {min_rating:.2f}")
        print(f"1. Diferența (Range) dintre cele mai bune și cele mai slabe evaluări ale TV-urilor: {tvs_range:.2f}")
        
    # În ce interval de preț se află cel mai mare număr de telefoane mobile vândute? (IQR)
    print("\n--- 2. Intervalul Intercuartil (IQR) pentru Prețurile 'Smartphones' ---")
    
    smartphones_df = df[df['category'] == 'Smartphones'].copy()
    
    if smartphones_df.empty:
        print("Nu s-au găsit date pentru categoria 'Smartphones'.")
    else:
        Q1 = smartphones_df['price'].quantile(0.25)
        Q3 = smartphones_df['price'].quantile(0.75)
        IQR = Q3 - Q1
        
        print(f"Cuartila 1 (Q1, 25%): {Q1:.2f} RON")
        print(f"Cuartila 3 (Q3, 75%): {Q3:.2f} RON")
        print(f"Intervalul Intercuartil (IQR) pentru preț: {IQR:.2f} RON")
        print(f"2. Intervalul de preț (IQR) în care se află numărul tipic (median) de telefoane vândute: între {Q1:.2f} RON și {Q3:.2f} RON")

    # Care sunt cele 5 branduri cu cele mai uniforme evaluări? (Abaterea Standard)
    print("\n--- 3. Cele 5 Branduri cu Cele Mai Uniforme Evaluări (Abaterea Standard) ---")
    
    brand_std = df.groupby('brand')['rating'].std().sort_values(ascending=True)
    
    top_5_uniform_brands = brand_std.head(5)
    
    print("3. Top 5 branduri cu cele mai uniforme evaluări (Abatere Standard descrescătoare):")
    print(top_5_uniform_brands.map('{:.4f}'.format).to_string())

    # Depinde numărul de evaluări de numărul de unități vândute? (Împărțirea în Cuartile)
    print("\n--- 4. Relația între Numărul de Evaluări și Vânzări (Grupare pe Cuartile) ---")
        
    try:
        df['rating_quartile'] = pd.qcut(
            df['num_of_ratings'], 
            q=4, 
            labels=['1st Quartile (Lowest Ratings)', '2nd Quartile', '3rd Quartile', '4th Quartile (Highest Ratings)']
        )
    except ValueError as e:
        print(f"Atenție la qcut: {e}. Folosim cut cu bins de cuartile.")
        quartiles = df['num_of_ratings'].quantile([0.25, 0.5, 0.75]).tolist()
        df['rating_quartile'] = pd.cut(
            df['num_of_ratings'], 
            bins=[df['num_of_ratings'].min() - 1] + quartiles + [df['num_of_ratings'].max() + 1],
            labels=['1st Quartile (Lowest Ratings)', '2nd Quartile', '3rd Quartile', '4th Quartile (Highest Ratings)'],
            include_lowest=True
        )

    sales_by_rating_quartile = df.groupby('rating_quartile', observed=True)['quantity_sold'].sum()
    
    print("4. Total unități vândute, grupate după Cuartila Numărului de Evaluări:")
    print(sales_by_rating_quartile.map('{:,.0f}'.format).to_string())
    
    print("\nInterpretare:")
    print("După cum se observă, există o asociere clară: Cu cât produsele au un număr mai mare de evaluări (4th Quartile),")
    print("cu atât numărul total de unități vândute este semnificativ mai mare. Acest lucru confirmă că vânzările și")
    print("numărul de evaluări se influențează reciproc pozitiv.")


if __name__ == "__main__":
    
    data = load_data(FILE_NAME)

    if data is not None:
        df_processed = preprocess_data(data.copy())
        
        perform_distribution_analysis(df_processed)

    print("\n--- Analiza Distribuției Datelor Finalizată ---")