# Scripts_for_Humanities
Scripts for Data collecting and date wrangling

Language for all scripts will be Python 3

## youtube_list.py

Dieses Skript ermöglicht das Scraping von Videos von einer YouTube-Kanal- oder Playliste-Seite. Es sammelt die Titel und URLs der Videos und speichert sie in einer .ods-Datei (LibreOffice Calc). Das Skript verwendet Selenium, um den Browser zu automatisieren, und Pandas, um die Daten zu verarbeiten und zu speichern.

### Voraussetzungen
Bevor das Skript ausgeführt wird, müssen einige Bibliotheken installiert werden. Die wichtigsten sind:

- **Selenium**: Für die Automatisierung der Browserinteraktion.
- **Webdriver Manager**: Zum automatischen Herunterladen und Verwalten des ChromeDrivers.
- **Pandas**: Zum Verarbeiten und Speichern der Daten in einer .ods-Datei.
- **BeautifulSoup4** (optional): Zum Analysieren von HTML, wird hier aber nicht aktiv verwendet.
- **odfpy**: Zum Exportieren der Daten in das .ods-Format.

### Installation
Die benötigten Bibliotheken können mit den folgenden Befehlen installiert werden:

```bash
pip install selenium
pip install webdriver-manager
pip install pandas
pip install odfpy
```

Stelle außerdem sicher, dass du Google Chrome installiert hast, da das Skript den ChromeDriver verwendet.

## youtube_videos_data.py

Dieses Skript sammelt detaillierte Informationen zu YouTube-Videos, die aus einer vorherigen Liste von Video-URLs stammen. Es verwendet die YouTube Data API, um Daten wie Veröffentlichungsdatum, Aufrufe, Likes, Kommentare und die Videolänge zu extrahieren. Die Ergebnisse werden anschließend in einer neuen ODS-Datei gespeichert.

### Voraussetzungen

Um das Skript auszuführen, müssen einige Bibliotheken installiert sein:

- **pandas**: Zum Lesen und Verarbeiten der .ods-Dateien.
- **google-api-python-client**: Zum Interagieren mit der YouTube Data API.
- **isodate**: Zum Parsen der Videolänge im ISO 8601-Format.
- **odfpy**: Zum Exportieren der Ergebnisse in das ODS-Format.

### Installation

Installiere die benötigten Bibliotheken mit den folgenden Befehlen:

```bash
pip install pandas
pip install google-api-python-client
pip install isodate
pip install odfpy
```
