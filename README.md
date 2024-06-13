# Volatility Aries GUI


1. General information
2. Requirements
3. Volatuition architecture
4. Getting started
5. Quick start guide
6. Plugins
7. Error handling
8. Kodestandarder for GUI-utvikling i Python

# General information

This application - Volatuition - is a graphical user interface (GUI) used for extracting digital artifacts from volatile memory (RAM) samples. Volatility is the most widely used framework for these types of tasks, but it is commonly executed from within a terminal. 
That's why we made Volatuition - the number one solution for using Volatility 3 in the most user-friendly way possible. 

# Requirements
---

Volatuition is compatible with Windows, Linux and Mac and requires Python 3.7.0 or later.
There are no requirements for running this software.

Admin?
Internett?
Dependencies? - Blir vel en EXE fil og trenger ikke dependencies?

```
pip3 install requirements-minimal.txt
```

#### Windows
8gb RAM
#### Linux
8gb RAM
#### Mac
8gb RAM

# Volatuition architecture
---

* Uses <a href="https://github.com/volatilityfoundation/volatility3">Volatility 3</a>: the most used framework for extracting digital artifacts from volatile memory (RAM) samples.
* Written in <a href="https://github.com/volatilityfoundation/volatility3">Python 3.12</a> with libraries such as
	* <a href="https://github.com/volatilityfoundation/volatility3">PyQt5</a> - Python library for GUI design
* Supported memory dump file types:
	* *.dmp,
	* *.mem,
	* *.vmem,
	* *.raw,
	* *.bin,
	* *.img,
	* *.hpak,
	* *.lime, 
	* *.elf,
	* *.json

# Getting started
---
### Installation

In CMD/terminal, navigate to the desired folder for placing Volatuition
```
1. 	cd C:/desired_path/desktop

2.	git clone https://github.com/StaffanPedersen/Volatilit3-Aries.git

3.	cd Volatilit3-Aries/

4.	pip3 install -r requirements.txt
```

##### Download manually

###### Windows
<a href="google.com">Download URL</a>

###### Linux
<a href="google.com">Download URL</a>

###### Macs
<a href="google.com">Download URL</a>


# Quick start guide
---

1. Open Volatuition. Run as administrator if needed.
2. Press "Start" to open the program.
3. Upload a memory dump file by clicking "Select file" in the top left corner. Supported files is listed in "Volatuition architecture".
4. When you see metadata appearing on the left, the program is ready to continue.
5. Press "Select Plugin" to open a window listing all plugins currently installed. Hover over each plugin to see a short description of the plugins function. NB: The plugins is sorted in an ascending order by OS. So if you're on Linux, the Linux plugins will appear on top.
6. Select a plugin for your OS and click save. 
	1. If you want to add a custom plugin, press the "+" button and find your desired plugin. This plugin will be added at the top.
7. When plugin is selected you can press "Run" to start a scan.
8. You can now see the result in the output field in the middle of the screen.
9. Press "Export" to export this scan to a .pdf, .csv, .xls, .txt, .doc or .json file


# Plugins



# Error handling





Kodestandarder for GUI-utvikling i Python
1. Generelle retningslinjer
•	Lesbarhet: Koden skal være lett å lese og forstå.
•	Konsistens: Bruk konsekvent navngivning og struktur.
•	Kommentarer: Kommenter koden der det er nødvendig for å forklare komplekse logikk eller viktige beslutninger.
2. Navngivningskonvensjoner
•	Moduler: Bruk små bokstaver og understrek (_) for å separere ord. Eksempel: my_module.py
•	Klasser: Bruk CamelCase for klassenavn. Eksempel: MyClass
•	Funksjoner og variabler: Bruk små bokstaver med understrek for å separere ord. Eksempel: my_function, my_variable
•	Konstanter: Bruk store bokstaver med understrek for å separere ord. Eksempel: MY_CONSTANT
3. Struktur og organisering
•	Importering: Alle import-setninger skal plasseres øverst i filen.
•	Standardbiblioteker først.
•	Tredjepartsbiblioteker deretter.
•	Egendefinerte moduler til slutt.
•	Funksjonsdefinisjoner: Plasser funksjonsdefinisjoner etter import-setningene, men før hovedkodeblokken.
•	Klasser: Hvis klasser brukes, plasser dem etter funksjonsdefinisjonene.
4. Funksjoner og metoder
•	Lengde: Funksjoner og metoder skal være korte og konsise. En funksjon skal utføre en oppgave eller beregning.
•	Dokumentasjonsstrenger: Alle funksjoner og metoder skal ha dokumentasjonsstrenger som forklarer deres formål.
5. GUI-spesifikke retningslinjer
Layout: Bruk et konsistent layoutsystem (for eksempel tkinter, PyQt, etc.).
Event-håndtering: Skill logikk for event-håndtering fra GUI-kode. Bruk separate funksjoner for å håndtere events.
Modularisering: Del GUI-komponenter inn i separate moduler eller klasser for å gjøre koden mer håndterbar og gjenbrukbar.
Feilhåndtering: Implementer grundig feilhåndtering, spesielt for brukerinput.

7. Testing og validering
•	Enhetstesting: Skriv enhetstester for å validere funksjonaliteten til koden din.
•	GUI-testing: Bruk verktøy som unittest eller pytest sammen med GUI-testing bibliotek som pytest-qt for å teste GUI-komponentene.
8. Dokumentasjon
•	Kommentarer: Kommenter kritiske deler av koden, men ikke overflødig.
