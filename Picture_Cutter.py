import requests
import pandas as pd

# WordPress-Zugangsdaten
benutzername = 'dein_benutzername'
passwort = 'dein_passwort'

# URL zur WordPress REST API für Medienelemente
api_url = 'https://deine-wordpress-website.de/wp-json/wp/v2/media/'

# Lese die Excel-Tabelle mit IDs und neuen Beschreibungen
excel_datei = 'Alle_Mitglieder.xlsx'
df = pd.read_excel(excel_datei)

# Durchlaufe die Zeilen der Tabelle
for index, row in df.iterrows():
    media_id = row['ID']
    neue_beschreibung = row['HTML-Link']

    # URL zur REST API für das spezifische Medienelement
    media_url = f'{api_url}{media_id}'

    # Header für die Authentifizierung
    headers = {
        'Content-Type': 'application/json',
    }

    # Daten für die Aktualisierung der Beschreibung
    data = {
        'description': neue_beschreibung,
    }

    # Authentifiziere dich und sende die Anfrage
    auth = (benutzername, passwort)
    response = requests.post(media_url, headers=headers, json=data, auth=auth)

    # Überprüfe die Antwort
    if response.status_code == 200:
        print(f'Beschreibung für Medienelement mit ID {media_id} wurde aktualisiert.')
    else:
        print(f'Fehler beim Aktualisieren der Beschreibung für Medienelement mit ID {media_id}: {response.status_code}')

