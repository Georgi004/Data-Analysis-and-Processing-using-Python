import pandas as pd
import numpy as np

FILE_NAME = 'fit_trackr_data.csv'
CLEANED_FILE_NAME = 'fit_trackr_data_cleaned.csv'

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


def load_data(file_name):
    """Incarca setul de date."""
    try:
        df = pd.read_csv(file_name)
        print(f"\n--- 1. Incarcarea Datelor ---")
        print(f"Setul de date '{file_name}' a fost incarcat. Randuri initiale: {df.shape[0]}")
        return df
    except FileNotFoundError:
        print(f"EROARE: Fisierul '{file_name}' nu a fost gasit.")
        return None


def clean_duration_calories(df):
    """
    Transforma coloanele 'Duration' si 'Calories' in valori numerice (float).
    Elimina unitatile de masura (min, kcal) si trateaza valorile lipsa.
    """
    print("--- 2.1. Curatarea si Conversia Duratei si Caloriilor ---")

    df['Duration'] = df['Duration'].astype(str).str.replace(r' min', '', regex=False).str.strip()
    df['Duration'] = pd.to_numeric(df['Duration'], errors='coerce')
    
    df['Calories'] = df['Calories'].astype(str).str.replace(r' kcal', '', regex=False).str.strip()
    df['Calories'] = pd.to_numeric(df['Calories'], errors='coerce')

    print("Conversie Durata/Calorii finalizata.")
    return df


def standardize_text_data(df):
    """
    Standardizeaza valorile in coloanele 'Activity' si 'Mood' (trateaza majuscule/minuscule, greseli comune).
    """
    print("--- 2.2. Standardizarea Datelor Textuale (Activity & Mood) ---")

    df['Activity'] = df['Activity'].astype(str).str.lower().str.strip()
    df['Activity'] = df['Activity'].replace({'swimm': 'swimming', 'swim': 'swimming', 'walk': 'walking', 'yoga': 'Yoga', 'run': 'running'})
    
    df['Mood'] = df['Mood'].astype(str).str.strip()
    
    print("Standardizare Activity & Mood finalizata.")
    return df


def handle_missing_duplicates(df):
    """
    Trateaza valorile lipsa si elimina randurile duplicate.
    """
    print("--- 2.3. Eliminarea Duplicatelor si a Randurilor Incomplete ---")
    
    initial_rows = df.shape[0]
    
    df.drop_duplicates(inplace=True)
    duplicates_removed = initial_rows - df.shape[0]
    print(f"  > Duplicate complete eliminate: {duplicates_removed}")
    
    cols_to_check = ['Activity', 'Duration', 'Calories', 'Mood']
    df.dropna(subset=cols_to_check, inplace=True)
    
    missing_removed = initial_rows - duplicates_removed - df.shape[0]
    print(f"  > Randuri incomplete eliminate: {missing_removed}")
    
    df.dropna(subset=['Username'], inplace=True)
    
    final_rows = df.shape[0]
    print(f"Randuri ramase dupa curatare: {final_rows}")
    
    return df


def save_cleaned_data(df, file_name):
    """Salveaza setul de date curatat intr-un fisier CSV."""
    df.to_csv(file_name, index=False)
    print(f"\n--- Setul de date curatat a fost salvat ca '{file_name}' ---")


if __name__ == "__main__":
    
    data = load_data(FILE_NAME)

    if data is not None:
        df_cleaned = clean_duration_calories(data.copy())
        df_cleaned = standardize_text_data(df_cleaned)
        df_cleaned = handle_missing_duplicates(df_cleaned)
        
        save_cleaned_data(df_cleaned, CLEANED_FILE_NAME)

    print("\n--- Faza 1: Preprocesarea Datelor Finalizata ---")

    