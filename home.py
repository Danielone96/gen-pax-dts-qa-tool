import random
from datetime import datetime, timedelta
import csv
import string

# --- Dati per la generazione ---
first_names_m_it = ["Mario", "Giuseppe", "Luca", "Alessandro", "Roberto", "Francesco", "Giovanni", "Stefano", "Andrea", "Lorenzo", "Matteo", "Marco", "Antonio", "Davide", "Filippo"]
first_names_f_it = ["Maria", "Anna", "Giulia", "Francesca", "Elena", "Chiara", "Silvia", "Federica", "Alice", "Roberta", "Martina", "Sara", "Laura", "Valentina", "Paola"]
last_names_it = ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marini", "Greco", "Barbieri", "Lombardi", "Moretti", "Fontana", "Conti"]

first_names_m_us = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Mark"]
first_names_f_us = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret", "Sandra"]
last_names_us = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]

# Liste estese per nuovi campi
countries = ["USA", "Canada", "Mexico", "Brazil", "Argentina", "UK", "France", "Germany", "Spain", "Italy", "Russia", "China", "Japan", "India", "Australia", "South Africa", "Egypt", "Nigeria"]
cities = ["New York", "Los Angeles", "Toronto", "Mexico City", "Sao Paulo", "London", "Paris", "Berlin", "Rome", "Moscow", "Beijing", "Tokyo", "New Delhi", "Sydney", "Cairo"]
phone_prefixes = ["+1", "+44", "+33", "+49", "+39", "+7", "+86", "+81", "+91", "+61", "+55"]

def get_category_from_date(birth_date_obj):
    """Calcola la categoria: Infant (I) <= 2, Junior (J) < 18, Adult (A) >= 18"""
    # Usa 365.2425 per gestire in modo preciso gli anni bisestili
    age_years = (datetime.now() - birth_date_obj).days / 365.2425
    if age_years <= 2:
        return 'I'
    elif age_years < 18:
        return 'J'
    else:
        return 'A'

def generate_passenger_data(num_passengers=1, nationality='IT', age_category=None):
    """
    Genera una lista di dati passeggeri randomici.
    """

    passengers = []
    shared_residence_country = None # Per garantire che tutti i passeggeri del batch abbiano lo stesso paese di residenza

    emergency_contacts_pool = []
    if num_passengers > 1:
        # Genera un pool di nomi unici per i contatti di emergenza per evitare duplicati nel batch
        temp_names = first_names_m_it + first_names_f_it + first_names_m_us + first_names_f_us
        temp_last_names = last_names_it + last_names_us
        # Assicura di avere abbastanza nomi unici
        while len(emergency_contacts_pool) < num_passengers:
            name = f"{random.choice(temp_names)} {random.choice(temp_last_names)}"
            if name not in emergency_contacts_pool:
                emergency_contacts_pool.append(name)

    for _ in range(num_passengers):
        gender = random.choice(['M', 'F'])

        # Seleziona i dati in base alla nazionalità
        if nationality == 'IT':
            first_names_m = first_names_m_it
            first_names_f = first_names_f_it
            last_names = last_names_it
            date_format = "%d/%m/%Y"
        elif nationality == 'US':
            first_names_m = first_names_m_us
            first_names_f = first_names_f_us
            last_names = last_names_us
            date_format = "%m/%d/%Y"
        else:  # Fallback su IT
            nationality = 'IT'
            first_names_m = first_names_m_it
            first_names_f = first_names_f_it
            last_names = last_names_it
            date_format = "%d/%m/%Y"

        if gender == 'M':
            first_name = random.choice(first_names_m)
        else:
            first_name = random.choice(first_names_f)

        last_name = random.choice(last_names)

        # Generazione data di nascita controllata per Junior o Adult
        if age_category == 'minor':
            start_date = datetime.now() - timedelta(days=17*365)
            end_date = datetime.now()
        elif age_category == 'adult':
            start_date = datetime.now() - timedelta(days=80*365)
            end_date = datetime.now() - timedelta(days=18*365)
        else:
            start_date = datetime.now() - timedelta(days=80*365)
            end_date = datetime.now()
            
        random_days = random.randint(0, (end_date - start_date).days)
        birth_date_obj = start_date + timedelta(days=random_days)
        birth_date_str = birth_date_obj.strftime(date_format)

        # --- Generazione Nuovi Campi ---
        # Info Documento
        doc_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        issue_date = datetime.now() - timedelta(days=random.randint(365*2, 365*5))
        exp_date = datetime.now() + timedelta(days=random.randint(365*2, 365*10))
        doc_nationality = random.choice(countries)

        # Info Residenza
        address_city = random.choice(cities)
        if shared_residence_country is None:
            shared_residence_country = random.choice(countries)
        residence_country = shared_residence_country

        # Info Contatto
        mobile_prefix = random.choice(phone_prefixes)
        mobile_number = str(random.randint(100000000, 999999999))

        # Info Emergenza
        emergency_prefix = random.choice(phone_prefixes)
        emergency_number = str(random.randint(100000000, 999999999))
        if num_passengers > 1:
            emergency_name = emergency_contacts_pool.pop()
        else:
            emergency_name = f"{random.choice(first_names_m_it + first_names_f_it)} {random.choice(last_names_it)}"

        passengers.append({
            "nome": first_name,
            "cognome": last_name,
            "data_nascita": birth_date_str,
            "sesso": gender,
            "nazionalita": nationality, # IT/US per generazione
            "categoria": get_category_from_date(birth_date_obj),
            "voyagerclub_no": "", # Default vuoto, da inserire solo a mano
            "membership": "", # Default vuoto
            "nationality_full": doc_nationality,
            "place_of_birth": random.choice(cities),
            "document_number": doc_number,
            "date_of_issue": issue_date.strftime("%d/%m/%Y"),
            "date_of_expiration": exp_date.strftime("%d/%m/%Y"),
            "country_of_issue": doc_nationality,
            "address_1": f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple'])} St.",
            "city": address_city,
            "country_of_residence": residence_country,
            "zip_code": str(random.randint(10000, 99999)),
            "prefix": mobile_prefix,
            "mobile_number": mobile_number,
            "email_address": "d.dicastro@nexsoft.it",
            "emergency_prefix": emergency_prefix,
            "emergency_phone": emergency_number,
            "emergency_contact_name": emergency_name
        })

    return passengers

def _overwrite_db(data_list, filename="database.csv"):
    """
    Funzione interna per sovrascrivere l'intero file CSV con una nuova lista di dati.
    """
    all_keys = [
        "nome", "cognome", "data_nascita", "sesso", "nazionalita", "categoria", "voyagerclub_no",
        "membership", "nationality_full", "place_of_birth", "document_number", "date_of_issue", "date_of_expiration",
        "country_of_issue", "address_1", "city", "country_of_residence", "zip_code", "prefix",
        "mobile_number", "email_address", "emergency_prefix", "emergency_phone", "emergency_contact_name"
    ]
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            if data_list: # Assicura che la lista non sia vuota per evitare errori
                # Filtra le chiavi di ogni riga per corrispondere a all_keys, per sicurezza
                filtered_data = [{k: row.get(k, '') for k in all_keys} for row in data_list]
                writer.writerows(filtered_data)
    except PermissionError:
        raise PermissionError(f"Impossibile salvare su {filename}. Chiudi il file se è aperto in un altro programma.")
    except Exception as e:
        print(f"Errore durante la sovrascrittura del DB: {e}")

def read_from_csv(filename="database.csv"):
    """
    Legge i dati dal file CSV e li restituisce come lista di dizionari.
    """
    passengers = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                passengers.append(row)
    except FileNotFoundError:
        pass
    return passengers

def save_to_csv(passengers, filename="database.csv"):
    """
    Salva e aggiorna il database fondendo vecchi e nuovi dati in modo pulito.
    """
    # Lista completa e ordinata di tutte le colonne possibili per garantire la coerenza del CSV
    all_keys = [
        "nome", "cognome", "data_nascita", "sesso", "nazionalita", "categoria", "voyagerclub_no",
        "membership", "nationality_full", "place_of_birth", "document_number", "date_of_issue", "date_of_expiration",
        "country_of_issue", "address_1", "city", "country_of_residence", "zip_code", "prefix",
        "mobile_number", "email_address", "emergency_prefix", "emergency_phone", "emergency_contact_name"
    ]

    if not passengers:
        return

    existing_data = read_from_csv(filename)
    
    # Retrocompatibilità: Assicura che i vecchi dati ricevano tutte le nuove colonne con valori vuoti
    for row in existing_data:
        # Logica per 'categoria'
        if 'categoria' not in row or not row['categoria']:
            if row.get('data_nascita'):
                fmt = "%m/%d/%Y" if row.get('nazionalita') == 'US' else "%d/%m/%Y"
                try:
                    dt = datetime.strptime(row.get('data_nascita', ''), fmt)
                    row['categoria'] = get_category_from_date(dt)
                except ValueError:
                    row['categoria'] = 'A' # Fallback sicuro
            else:
                row['categoria'] = 'A'
        # Aggiunge le altre chiavi mancanti
        for key in all_keys:
            if key not in row:
                row[key] = ''

    all_data = existing_data + passengers

    _overwrite_db(all_data, filename)

def delete_record(nome, cognome, data_nascita, filename="database.csv"):
    """
    Elimina un record dal file CSV basandosi su nome, cognome e data di nascita.
    """
    all_data = read_from_csv(filename)
    for i, row in enumerate(all_data):
        if row.get('nome') == nome and row.get('cognome') == cognome and row.get('data_nascita') == data_nascita:
            del all_data[i]
            break
            
    _overwrite_db(all_data, filename)

def update_record(old_nome, old_cognome, old_data, new_record_dict, filename="database.csv"):
    """
    Trova il record basato su nome, cognome e data originali, e lo sostituisce interamente
    con il nuovo dizionario fornito. Poi riscrive il file.
    """
    all_data = read_from_csv(filename)
    updated = False
    for i, row in enumerate(all_data):
        if row.get('nome') == old_nome and row.get('cognome') == old_cognome and row.get('data_nascita') == old_data:
            # Unisce o sostituisce con i nuovi dati
            all_data[i].update(new_record_dict)
            updated = True
            break
    
    if updated:
        _overwrite_db(all_data, filename)

if __name__ == "__main__":
    print("--- Generatore Dati Passeggeri (Test CLI) ---")
    try:
        count_input = input("Quanti passeggeri vuoi generare? [default: 2] ")
        count = int(count_input) if count_input else 2
        nationality_choice = input("Nazionalità (IT/US)? [default: IT] ").upper() or 'IT'

        data = generate_passenger_data(count, nationality_choice)
        save_to_csv(data)
        print(f"\n Dati generati e salvati in 'database.csv'")

        print(f"\n{'NOME':<15} | {'COGNOME':<15} | {'DATA NASCITA':<15} | {'SESSO':<5} | {'NAZ.':<5} | {'CAT.':<5}")
        print("-" * 75)
        for p in data:
            print(f"{p['nome']:<15} | {p['cognome']:<15} | {p['data_nascita']:<15} | {p['sesso']:<5} | {p['nazionalita']:<5} | {p['categoria']:<5}")

    except ValueError:
        print("Input non valido. Inserire un numero intero.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")