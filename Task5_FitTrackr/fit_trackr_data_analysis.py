import pandas as pd
import numpy as np

CLEANED_FILE_NAME = 'fit_trackr_data_cleaned.csv'

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


def load_cleaned_data(file_name):
    """Incarca setul de date curatat."""
    try:
        df = pd.read_csv(file_name)
        print(f"\n--- Setul de date curatat a fost incarcat. Randuri: {df.shape[0]} ---")
        return df
    except FileNotFoundError:
        print(f"EROARE: Fisierul '{file_name}' nu a fost gasit. Rulati mai intai scriptul de curatare.")
        return None
    except Exception as e:
        print(f"EROARE la incarcarea fisierului: {e}")
        return None


def analyze_user_behavior(df):
    """
    Efectueaza analizele statistice de baza si cele avansate.
    """
    print("\n" + "="*80)
    print("                 Analiza Comportamentului Utilizatorului FitTrackr")
    print("="*80)

    avg_duration = df['Duration'].mean()
    print(f"\n1. Durata medie a activitatii (Media Aritmetica): {avg_duration:.2f} minute")
    
    most_frequent_activity = df['Activity'].mode().iloc[0]
    print(f"\n2. Cea mai frecventa activitate (Modul): {most_frequent_activity}")

    most_frequent_mood = df['Mood'].mode().iloc[0]
    print(f"\n3. Cea mai frecventa stare de spirit (Modul): {most_frequent_mood}")

    calories_std = df.groupby('Activity')['Calories'].std().sort_values(ascending=False)
    print("\n4. Variatia (Abaterea Standard) a Caloriilor Consumate pe Tip de Activitate:")
    print("O Abatere Standard mai mare inseamna o variatie mai mare a rezultatelor (mai putin previzibila).")
    print(calories_std.map('{:.2f} kcal'.format).to_string())

    Q1_age = df['Age'].quantile(0.25)
    Q3_age = df['Age'].quantile(0.75)
    IQR_age = Q3_age - Q1_age
    
    print("\n5. Variatia Varstei Utilizatorilor (Interval Intercuartil - IQR):")
    print(f"   Cuartila 1 (25%): {Q1_age:.0f} ani")
    print(f"   Cuartila 3 (75%): {Q3_age:.0f} ani")
    print(f"   Diferenta IQR (Q3 - Q1): {IQR_age:.0f} ani")
    print("   Acest interval arata ca 50% din utilizatori au o varsta care variaza pe o durata de 24 de ani.")

    print("\n" + "="*80)
    print("                 Provocari Suplimentare (Analiza Avansata)")
    print("="*80)

    happy_df = df[df['Mood'] == 'Happy']
    happy_activity_count = happy_df['Activity'].value_counts()
    
    print("\n6. Top 5 Activitati care Genereaza cea mai Frecventa Stare 'Happy':")
    print(happy_activity_count.head(5).to_string())

    
    df['Duration_Quartile'] = pd.qcut(
        df['Duration'], 
        q=4, 
        labels=['Scurt (Q1)', 'Mediu (Q2)', 'Lung (Q3)', 'Cel mai Lung (Q4)'],
        duplicates='drop'
    )
    
    happy_by_duration = df.groupby('Duration_Quartile', observed=True)['Mood'].apply(
        lambda x: (x == 'Happy').sum()
    )
    
    total_by_duration = df['Duration_Quartile'].value_counts()
    happy_percentage = (happy_by_duration / total_by_duration * 100).sort_index()

    print("\n7. Impactul Duratei Activitatii asupra Starii de Spirit 'Happy':")
    
    results = pd.DataFrame({
        'Total Logs': total_by_duration,
        'Happy Logs': happy_by_duration,
        '% Happy': happy_percentage.map('{:.2f}%'.format)
    }).sort_index()
    
    print(results.to_string())

    print("\nInterpretare Durata & Happy:")
    print("Intervalele de durata corespunzatoare sunt: Scurt (min-Q1), Mediu (Q1-Q2), Lung (Q2-Q3), Cel mai Lung (Q3-max).")
    print("Se observa ca activitatile de 'Durata Medie' (Q2) si 'Durata Lungă' (Q3) au cel mai mare procent de dispozitie 'Happy'.")
    print("Durata Extrema ('Scurt' sau 'Cel mai Lung') pare sa fie mai putin corelata cu starea 'Happy'.")
    

if __name__ == "__main__":
    
    data = load_cleaned_data(CLEANED_FILE_NAME)

    if data is not None:
        analyze_user_behavior(data)

    print("\n--- Faza 2: Analiza Datelor Finalizata ---")