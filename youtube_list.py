from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import html
from webdriver_manager.chrome import ChromeDriverManager

def get_all_videos(channel_url):
    # Konfiguriere den ChromeDriver
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--headless")

    # Verwende den WebDriver-Manager, um den ChromeDriver automatisch herunterzuladen
    service = Service(ChromeDriverManager().install())

    # Starte den Browser
    driver = webdriver.Chrome(service=service, options=options)
    print("Browser gestartet.")

    # Besuche die Kanal-URL
    driver.get(channel_url)
    print(f"Besuche die URL: {channel_url}")

    try:
        # Warte, bis der Zustimmungsbutton auf der Umleitungsseite angezeigt wird
        accept_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[2]/div/div/button/span'))
        )
        accept_button.click()
        print("Cookie-Meldung akzeptiert.")
    except Exception as e:
        print(f"Cookie-Zustimmung konnte nicht geklickt werden: {e}")

    # Warte kurz, damit die Seite korrekt geladen wird
    time.sleep(5)
    try:
        # Warte, bis die Videoelemente sichtbar sind
        WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        print("Videoelemente wurden gefunden.")
    except Exception as e:
        print(f"Die Videos konnten nicht rechtzeitig geladen werden: {e}")
        return [], driver

    # Scrollen, um alle Videos zu laden (Lazy Loading)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3)  # Warte, bis der Inhalt geladen wird
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Versuche, die Videos zu extrahieren (Selenium)
    video_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/watch')]")
    all_videos = []

    for video in video_elements:
        video_title = video.get_attribute("title")
        video_url = video.get_attribute("href")
        if video_title and video_url:
            all_videos.append([video_title, video_url])

    if not all_videos:
        print("Keine Videos gefunden. Möglicherweise wurde die Seite nicht korrekt geladen.")
    else:
        print(f"{len(all_videos)} Videos gefunden.")

    return all_videos, driver

# Frage nach der Channel-URL
channel_url = input("Bitte geben Sie die URL des YouTube-Kanals an: ").strip()
if not channel_url.startswith("http"):
    channel_url = "https://" + channel_url

# Frage nach dem gewünschten Dateinamen
output_filename = input("Bitte geben Sie den Namen der Ausgabedatei (ohne Erweiterung) an: ").strip()
if not output_filename.endswith('.ods'):
    output_filename += '.ods'  # Füge die Endung .ods hinzu, wenn nicht bereits vorhanden

# Videos abrufen und speichern
videos, driver = get_all_videos(channel_url)

if videos:
    df = pd.DataFrame(videos, columns=['Title', 'URL'])
    df.insert(0, 'ID', range(1, 1 + len(df)))  # Fügt eine ID-Spalte am Anfang hinzu
    df['ID'] = df['ID'].apply(lambda x: f"{x:03d}")  # Format der ID als dreistellige Zahl
    df.to_excel(output_filename, index=False, engine='odf')
    print(f"Die Tabelle {output_filename} wurde erstellt und enthält {len(videos)} Videos.")
else:
    print("Keine Videos wurden gefunden und gespeichert.")

# Optional: Den Browser manuell schließen, wenn alle Aufgaben abgeschlossen sind
try:
    print("Beenden des Browsers...")
    driver.quit()
    print("Browser erfolgreich beendet.")
except Exception as e:
    print(f"Fehler beim Beenden des Browsers: {e}")
