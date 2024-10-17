import pandas as pd
from fuzzywuzzy import process

# 1. Citirea fișierelor CSV
print("Citirea fișierelor CSV...")
facebook_df = pd.read_csv("facebook_dataset.csv", on_bad_lines="skip")
google_df = pd.read_csv("google_dataset.csv", on_bad_lines="skip", low_memory=False)
website_df = pd.read_csv("website_dataset.csv", sep=";", on_bad_lines="skip")
print("Fișierele au fost citite cu succes.")

# 2. Verificarea primelor rânduri din fiecare set de date
print("Facebook Dataset:")
print(facebook_df.head())

print("\nGoogle Dataset:")
print(google_df.head())

print("\nWebsite Dataset:")
print(website_df.head())

# 3. Informatii suplimentare despre datele din fiecare set de date
print("\nInformatii Facebook Dataset:")
print(facebook_df.info())

print("\nInformatii Google Dataset:")
print(google_df.info())

print("\nInformatii Website Dataset:")
print(website_df.info())

# 4. Functie pentru curatarea si standardizarea numelui companiilor
def clean_company_name(df, column_name):
    df[column_name] = df[column_name].str.lower().str.strip()
    return df

# 5. Aplicarea functiei de curatare pe fiecare set de date
facebook_df = clean_company_name(facebook_df, 'name')
google_df = clean_company_name(google_df, 'name')
website_df = clean_company_name(website_df, 'site_name')

# 6. Functie pentru potrivirea fuzzy a numelui companiilor
def fuzzy_match_names(df1, df2, column1, column2, threshold=80):
    matched_names = []
    for name in df1[column1]:
        match = process.extractOne(name, df2[column2], score_cutoff=threshold)
        matched_names.append(match[0] if match else None)
    return matched_names

# 7. Aplicarea potrivirii fuzzy pentru a gasi nume similare in seturile de date
facebook_df['matched_name_google'] = fuzzy_match_names(facebook_df, google_df, 'name', 'name')
website_df['matched_name_facebook'] = fuzzy_match_names(website_df, facebook_df, 'site_name', 'name')

# 8. Imbinarea seturilor de date pe baza numelui potrivit fuzzy
merged_df = pd.merge(facebook_df, google_df, left_on="matched_name_google", right_on="name", how="outer", suffixes=('_fb', '_google'))
merged_df = pd.merge(merged_df, website_df, left_on="matched_name_google", right_on="matched_name_facebook", how="outer")

# 9. Functie pentru rezolvarea conflictelor de date in coloana 'phone'
def resolve_conflict(val1, val2, val3):
    values = [val1, val2, val3]
    valid_values = [val for val in values if pd.notnull(val)]
    return max(set(valid_values), key=valid_values.count) if valid_values else None

# 10. Aplic functia de rezolvare a conflictelor pentru coloana 'phone'
merged_df['phone'] = merged_df.apply(lambda row: resolve_conflict(row.get('phone_fb'), row.get('phone_google'), row.get('phone')), axis=1)

# 11. Verific coloanele din setul de date final
print("\nColoanele din setul de date final:")
print(merged_df.columns)

# 12. Eliminarea coloanelor care nu mai sunt necesare
cols_to_drop = ['phone_fb', 'phone_google', 'site_name', 'domain_fb', 'address_fb', 'categories', 'city_fb', 
                'country_code_fb', 'country_name_fb', 'description']
final_df = merged_df.drop(columns=[col for col in cols_to_drop if col in merged_df.columns])

# 13. Salvarea rezultatelor în fișiere CSV
final_df.to_csv("final_merged_dataset.csv", index=False, sep=',')
final_df.to_csv("final_merged_cleaned_dataset.csv", index=False, sep=',')

# 14. Afișarea rezultatelor
print("\nFinal Dataset:")
print(final_df.head())

print("\nNumăr de valori lipsă în fiecare coloană după îmbinare:")
print(final_df.isnull().sum())

