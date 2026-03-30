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
    print(f"\n--- Incarcarea datelor din '{file_name}' ---")
    try:
        df = pd.read_csv(file_name)
        print(f"Setul de date a fost incarcat cu succes. Randuri initiale: {df.shape[0]}")
        return df
    except FileNotFoundError:
        print(f"\nEROARE: Fisierul '{file_name}' nu a fost gasit.")
        return None
    except Exception as e:
        print(f"\nEROARE la incarcarea fisierului: {e}")
        return None


def extract_rating_value(rating_str):
    """
    Extrage valoarea numerica a ratingului dintr-un sir de caractere.
    Exemplu: "8.75 out of 10" devine 8.75.
    Trateaza valorile lipsa (NaN) sau 'no value'.
    """
    if pd.isna(rating_str) or rating_str == 'no value':
        return np.nan
    try:
        return float(str(rating_str).split(' ')[0])
    except:
        return np.nan

def preprocess_data(df):
    """
    Efectueaza toti pasii de preprocesare, curatare si transformare a datelor.
    1. Conversia tipurilor de date
    2. Extragerea rating-ului
    3. Eliminarea valorilor lipsa
    4. Eliminarea duplicatelor
    """
    print("\n--- 1. Transformarea si Curatarea Datelor ---")

    print("   1.1. Conversia tipurilor de coloane...")
    
    # Coloane catre int
    integer_cols = ['quantity_sold', 'num_of_ratings', 'quantity_in_stock']
    for col in integer_cols:
        # Folosim pd.to_numeric si errors='coerce' pentru a trata valorile non-numerice
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int32')

    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    print("   1.1. Conversie finalizata.")
    
    print("   1.2. Extragerea valorilor numerice din coloana 'rating'...")
    df['rating'] = df['rating'].apply(extract_rating_value)
    print("   1.2. Extragere rating finalizata.")

    initial_rows = df.shape[0]
    
    df.dropna(subset=['product_name'], inplace=True)
    print(f"   1.3.1. Randuri eliminate din cauza 'product_name' lipsa. Randuri ramase: {df.shape[0]}")
    
    num_cols = df.shape[1]
    threshold = num_cols - 4
    df.dropna(thresh=threshold, inplace=True)
    print(f"   1.3.2. Randuri eliminate din cauza prea multor valori lipsa (>4). Randuri ramase: {df.shape[0]}")
    
    df.drop_duplicates(keep='first', inplace=True)
    print(f"   1.4. Randuri duplicate complete eliminate. Randuri ramase: {df.shape[0]}")
    print(f"\n   TOTAL randuri eliminate in etapa de curatare: {initial_rows - df.shape[0]}")

    return df


def feature_engineering(df):
    """
    Genereaza o noua caracteristica: 'revenue' (venit).
    """
    print("\n--- 2. Ingineria Caracteristicilor ---")
    
    df['revenue'] = df['price'] * df['quantity_sold']
    
    print("   Noua coloana 'revenue' (pret * unitati vandute) a fost generata.")
        
    return df


def perform_analysis(df):
    """
    Efectueaza cele doua analize solicitate: top 10 Keyboards dupa venit si top 10 TVs dupa cel mai mic venit.
    """
    print("\n--- 3. Analiza Datelor ---")

    # Gaseste cele 10 produse din categoria 'Keyboards' cu cel mai mare venit
    keyboards_df = df[df['category'] == 'Keyboards'].copy()
    
    top_10_keyboards = keyboards_df.sort_values(
        by='revenue', 
        ascending=False
    ).head(10)

    print("\n====================================================")
    print("3.1. Top 10 produse (Keyboards) dupa cel mai MARE venit:")
    
    if not top_10_keyboards.empty:
        print(top_10_keyboards[['product_name', 'revenue']].to_string(
            index=False, 
            float_format=lambda x: f"{x:,.2f}"
        ))
    else:
        print("   Nu s-au gasit date valide pentru categoria 'Keyboards'.")


    # Gaseste cele 10 produse din categoria 'TVs' cu cel mai mic venit
    tvs_df = df[df['category'] == 'TVs'].copy()
    
    bottom_10_tvs = tvs_df.sort_values(
        by='revenue', 
        ascending=True
    ).head(10)

    print("\n====================================================")
    print("3.2. Top 10 produse (TVs) dupa cel mai MIC venit:")

    if not bottom_10_tvs.empty:
        print(bottom_10_tvs[['product_name', 'revenue']].to_string(
            index=False, 
            float_format=lambda x: f"{x:,.2f}"
        ))
    else:
        print("   Nu s-au gasit date valide pentru categoria 'TVs'.")


if __name__ == "__main__":
    
    data = load_data(FILE_NAME)

    if data is not None:
        df_cleaned = preprocess_data(data.copy())
        
        df_final = feature_engineering(df_cleaned.copy())
        
        perform_analysis(df_final)

    print("\n--- Analiza si Preprocesarea Datelor Finalizata ---")