import pandas as pd
import numpy as np

FILE_NAME = 'online_store_data.csv'

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'left')

print("--- Start Analiza Datelor Magazinului Online (Pandas) ---")

try:
    # Incarcarea datelor
    df = pd.read_csv(FILE_NAME)
    print(f"\nSetul de date '{FILE_NAME}' a fost incarcat cu succes.")
    
    # Coloanele reale din fisier: 

    # 1. Cate produse exista in setul de date?
    # Numarul total de randuri din DataFrame (proprietatea .shape[0])
    total_products = df.shape[0]
    print("\n====================================================")
    print(f"1. Numarul total de produse in setul de date: {total_products} randuri.")

    # 2. Care este cel mai bine vandut produs din intregul magazin online?
    # Sortare dupa 'quantity_sold' (descrescator) si selectarea primului rand
    # Coloana folosita - 'quantity_sold'
    best_seller = df.sort_values(by='quantity_sold', ascending=False).iloc[0]

    print("\n====================================================")
    print("2. Cel mai bine vandut produs din intregul magazin online este:")
    print(f"   Produs: {best_seller['product_name']}")
    print(f"   Categorie: {best_seller['category']}")
    print(f"   Unitati Vandute: {int(best_seller['quantity_sold'])}")


    # 3. Care sunt cele mai bine vandute 5 telefoane mobile?
    # Filtrare - Selectam doar produsele din categoria 'Smartphones'
    # Coloana folosita: 'category'
    smartphones_df = df[df['category'] == 'Smartphones'].copy()

    # Sortare - Dupa 'quantity_sold' (descrescator) si selectarea primelor 5
    top_5_smartphones = smartphones_df.sort_values(
        by='quantity_sold', 
        ascending=False
    ).head(5)

    print("\n====================================================")
    print("3. Cele mai bine vandute 5 telefoane mobile (Smartphones):")
    
    if not top_5_smartphones.empty:
        # Coloanele relevante
        print(top_5_smartphones[['product_name', 'quantity_sold', 'price']].to_string(index=False, float_format="%.2f"))
    else:
        print("   Nu s-au gasit produse in categoria 'Smartphones'.")


    # 4. Care este pretul celui mai scump si celui mai ieftin laptop?
    # Filtrare - Selectam doar randurile unde 'category' este 'Laptops'
    laptops_df = df[df['category'] == 'Laptops'].copy()

    # Curatarea datelor - Eliminam randurile unde 'price' este NaN sau mai mic/egal cu 0
    # Sarcina solicita eliminarea valorilor lipsa si preturi mai mari decat zero.
    laptops_df.dropna(subset=['price'], inplace=True)
    laptops_df = laptops_df[laptops_df['price'] > 0]
    
    print("\n====================================================")
    print("4. Pretul celui mai scump si celui mai ieftin laptop:")

    if not laptops_df.empty:
        max_price = laptops_df['price'].max()
        min_price = laptops_df['price'].min()

        most_expensive = laptops_df[laptops_df['price'] == max_price].iloc[0]
        cheapest = laptops_df[laptops_df['price'] == min_price].iloc[0]

        print(f"   Cel mai scump laptop:")
        print(f"      Nume: {most_expensive['product_name']}")
        print(f"      Preț: {max_price:.2f}")

        print(f"\n   Cel mai ieftin laptop:")
        print(f"      Nume: {cheapest['product_name']}")
        print(f"      Pret: {min_price:.2f}")
    else:
        print("   Nu s-au gasit laptopuri valide (cu pret pozitiv) dupa filtrare.")

except FileNotFoundError:
    print(f"\nEROARE: Fisierul '{FILE_NAME}' nu a fost gasit. Asigurati-va ca este in acelasi director cu scriptul.")
except KeyError as e:
    print(f"\nEROARE: Coloana {e} nu a fost gasita in setul de date. Va rugam sa verificati numele coloanelor.")
except Exception as e:
    print(f"\nO eroare neasteptata a aparut: {e}")


print("\n--- Analiza finalizata ---")