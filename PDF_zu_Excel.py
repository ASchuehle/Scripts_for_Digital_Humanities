import PyPDF2
import ezodf

# Quelldatei abfragen
source_file = input("Bitte geben Sie den Pfad zur Quelldatei ein: ")

# PDF öffnen und Text extrahieren
with open(source_file, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    pages_text = []
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        pages_text.append(page.extract_text())

# Neue Tabelle erstellen
spreadsheet = ezodf.newdoc(doctype='ods')
sheet = ezodf.Sheet('Blatt1', size=(len(pages_text), 1))

# Text in die Tabelle schreiben
for i, text in enumerate(pages_text):
    sheet[i, 0].set_value(text)

# Tabelle zum Dokument hinzufügen
spreadsheet.sheets.append(sheet)

# Zieldatei speichern
output_file = source_file.replace('.pdf', '.ods')
spreadsheet.saveas(output_file)

print(f"Die Daten wurden in {output_file} gespeichert.")
