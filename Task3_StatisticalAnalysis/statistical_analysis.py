import pandas as pd
import numpy as np

# Numele fisierului de date
FILE_NAME = 'online_store_data.csv'

# Setari pentru afisarea completa a DataFrame-urilor in consola
pd.set_option('display.max_rows', 20)
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
    Extrage valoarea numerica a ratingului dintr-un sir de caractere (ex: "8.75 out of 10" devine 8.75).
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
    print("\n--- Preprocesarea Datelor Necesare ---")
    
    df['rating'] = df['rating'].apply(extract_rating_value)
    
    # 2. Conversia coloanelor numerice cheie la tip intreg, tratand valorile non-numerice ca NaN
    integer_cols = ['quantity_sold', 'quantity_in_stock']
    for col in integer_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int32')
        
    print("Preprocesare finalizata: 'rating' extras, 'quantity_sold' si 'quantity_in_stock' convertite.")
    
    return df


def perform_statistical_analysis(df):
    """
    Efectueaza toate analizele statistice solicitate.
    """
    print("\n--- 1. Evaluarea Medie a Produselor (Masura de Tendinta Centrala) ---")
    
    avg_rating = df['rating'].mean()
    print(f"1. Evaluarea medie a tuturor produselor din magazin: {avg_rating:.2f} (din 10)")
    
    print("\n--- 2. Cel Mai Frecvent Brand (Modul) ---")
    
    most_frequent_brand = df['brand'].mode().iloc[0]
    print(f"2. Cel mai frecvent brand (Modul): {most_frequent_brand}")

    print("\n--- 3. Cel Mai Vândut Brand (Agregare) ---")

    best_selling_brand = df.groupby('brand')['quantity_sold'].sum().sort_values(ascending=False).head(1)
    
    print(f"3. Cel mai vândut brand din magazin (pe baza unităților vândute):")
    print(best_selling_brand.to_string())

    print("\n--- 4. Evaluarea Medie pe Categorii (Grupare și Medie) ---")

    avg_rating_by_category = df.groupby('category')['rating'].mean().sort_values(ascending=False)
    
    print("4. Evaluarea medie a produselor pe categorii:")
    print(avg_rating_by_category.map('{:.2f}'.format).to_string())

    print("\n--- 5. Popularitatea Produselor în Funcție de Culori (Grupare și Sortare) ---")

    sales_by_color = df.groupby('color')['quantity_sold'].sum().sort_values(ascending=False)
    
    print("5. Numărul total de unități vândute în funcție de culoare (Top Culori):")
    print(sales_by_color.to_string())

    print("\n--- 6. Cele Mai Eficiente 5 Branduri (Agregare Multiplă și Inginerie Caracteristici) ---")

    # Agregarea multipla: suma unitatilor vandute si a celor din stoc
    brand_performance = df.groupby('brand').agg(
        total_sold=('quantity_sold', 'sum'),
        total_in_stock=('quantity_in_stock', 'sum')
    )
    
    # Crearea noii caracteristici: Eficiența Vânzărilor (Sales Efficiency)
    brand_performance['sales_efficiency'] = brand_performance['total_sold'] / (
        brand_performance['total_sold'] + brand_performance['total_in_stock']
    )
    
    # Sortarea și selecția top 5
    top_5_efficient_brands = brand_performance.sort_values(
        by='sales_efficiency', 
        ascending=False
    ).head(5)
    
    print("6. Cele mai eficiente 5 branduri din punct de vedere al vânzărilor (Raport Vândut / Total Achiziționat):")
    display_df = top_5_efficient_brands[['total_sold', 'total_in_stock', 'sales_efficiency']].copy()
    display_df['sales_efficiency'] = display_df['sales_efficiency'].map('{:.4f}'.format)
    print(display_df.to_string())

if __name__ == "__main__":
    
    data = load_data(FILE_NAME)

    if data is not None:
        df_processed = preprocess_data(data.copy())
        
        perform_statistical_analysis(df_processed)

    print("\n--- Analiza de bază a datelor magazinului online Finalizată ---")