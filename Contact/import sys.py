import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit
import sqlite3

class ContactenApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.conn = None
        self.cursor = None
        self.db_name = "contactenlijst.db"
        
    def open(self):
        self.conn = sqlite3.connect("contactenlijst.db")
        self.cursor = self.conn.cursor()

    def initUI(self):
        self.setWindowTitle('Contactenbeheer')
        self.setGeometry(100, 100, 600, 400)

        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(300)
        self.list_widget.itemClicked.connect(self.on_contact_selected)

        self.label_naam = QLabel('Naam:')
        self.input_naam = QLineEdit()
        self.label_adres = QLabel('Adres:')
        self.input_adres = QLineEdit()
        self.label_telefoon = QLabel('Telefoonnummer:')
        self.input_telefoon = QLineEdit()
        self.label_geboortedatum = QLabel('Geboortedatum:')
        self.input_geboortedatum = QLineEdit()

        self.button_toevoegen = QPushButton('Toevoegen')
        self.button_toevoegen.clicked.connect(self.voeg_contact_toe)

        self.button_verwijderen = QPushButton('Verwijderen')
        self.button_verwijderen.clicked.connect(self.verwijder_contact)

        self.label_zoeken = QLabel('Zoeken:')
        self.input_zoeken = QLineEdit()
        self.button_zoeken = QPushButton('Zoeken')
        self.button_zoeken.clicked.connect(self.zoek_contact)

        vbox = QVBoxLayout()
        hbox_add = QHBoxLayout()
        hbox_add.addWidget(self.label_naam)
        hbox_add.addWidget(self.input_naam)
        hbox_add.addWidget(self.label_adres)
        hbox_add.addWidget(self.input_adres)
        hbox_add.addWidget(self.label_telefoon)
        hbox_add.addWidget(self.input_telefoon)
        hbox_add.addWidget(self.label_geboortedatum)
        hbox_add.addWidget(self.input_geboortedatum)
        hbox_add.addWidget(self.button_toevoegen)
        hbox_add.addWidget(self.button_verwijderen)

        hbox_search = QHBoxLayout()
        hbox_search.addWidget(self.label_zoeken)
        hbox_search.addWidget(self.input_zoeken)
        hbox_search.addWidget(self.button_zoeken)

        vbox.addLayout(hbox_add)
        vbox.addWidget(self.list_widget)
        vbox.addLayout(hbox_search)

        self.setLayout(vbox)

        self.toon_contacten()

    def toon_contacten(self):
        self.list_widget.clear()
        connection = sqlite3.connect("contactenlijst.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM contacten")
        resultaten = cursor.fetchall()
        for resultaat in resultaten:
            self.list_widget.addItem(f"{resultaat[0]} - {resultaat[1]} - {resultaat[2]} - {resultaat[3]}")
        connection.close()

    def voeg_contact_toe(self):
        naam = self.input_naam.text()
        adres = self.input_adres.text()
        telefoon = self.input_telefoon.text()
        geboortedatum = self.input_geboortedatum.text()

        connection = sqlite3.connect("contactenlijst.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contacten (naam, adres, telefoonnummer, geboortedatum) VALUES (?, ?, ?, ?)",
                       (naam, adres, telefoon, geboortedatum))
        connection.commit()
        connection.close()

        self.toon_contacten()

    def verwijder_contact(self):
        selected_item = self.list_widget.currentItem()
        if selected_item is None:
            return
        
        selected_text = selected_item.text()
        # Extracting naam, adres, telefoonnummer, and geboortedatum from the selected item
        naam, adres, telefoon, geboortedatum = selected_text.split(" - ")

        connection = sqlite3.connect("contactenlijst.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM contacten WHERE naam=? AND adres=? AND telefoonnummer=? AND geboortedatum=?",
                       (naam.strip(), adres.strip(), telefoon.strip(), geboortedatum.strip()))
        connection.commit()
        connection.close()

        self.toon_contacten()

    def zoek_contact(self):
        zoekterm = self.input_zoeken.text()
        self.list_widget.clear()
        connection = sqlite3.connect("contactenlijst.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM contacten WHERE naam LIKE ? OR adres LIKE ? OR telefoonnummer LIKE ? OR geboortedatum LIKE ?",
                       ('%' + zoekterm + '%', '%' + zoekterm + '%', '%' + zoekterm + '%', '%' + zoekterm + '%'))
        resultaten = cursor.fetchall()
        for resultaat in resultaten:
            self.list_widget.addItem(f"{resultaat[0]} - {resultaat[1]} - {resultaat[2]} - {resultaat[3]}")
        connection.close()

    def on_contact_selected(self):
        selected_item = self.list_widget.currentItem()
        if selected_item is None:
            return
        
        selected_text = selected_item.text()
        # Extracting naam, adres, telefoonnummer, and geboortedatum from the selected item
        naam, adres, telefoon, geboortedatum = selected_text.split(" - ")
        self.input_naam.setText(naam.strip())
        self.input_adres.setText(adres.strip())
        self.input_telefoon.setText(telefoon.strip())
        self.input_geboortedatum.setText(geboortedatum.strip())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ContactenApp()
    window.show()
    sys.exit(app.exec_())
