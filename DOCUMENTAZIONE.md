# Documentazione del Progetto - Gen_Pax_Dts da un idea di Davide Cardella.

**Versione:** 1.4
**Data:** Aggiornamento Corrente

## 1. Scopo del Progetto

Lo scopo di questo progetto è fornire un'applicazione desktop con interfaccia grafica (GUI) per gestire e generare dati anagrafici di passeggeri fittizi (nome, cognome, data di nascita, sesso, nazionalità, categoria d'età). I dati generati vengono salvati cumulativamente in un file locale `database.csv`.

## 2. Funzionalità Principali

- **Modalità di Input Unificata (Auto-Fill):** Permette di generare in blocco X passeggeri completamente casuali. Se l'utente compila solo parzialmente il modulo (es. imposta solo il nome), il programma compilerà autonomamente e casualmente tutti i campi restanti mantenendo la coerenza del genere.
- **Campo Manuale Esclusivo:** È stato aggiunto il campo "Voyagerclub No." che viene salvato solo se inserito manualmente, rimanendo vuoto nella generazione casuale.
- **Generazione Mirata per Età (Spinbox):** Tramite comode frecce direzionali è possibile decidere il numero totale dei record da generare e specificare quanti di essi devono essere minorenni (Junior/Infant).
- **Generazione Dati Estesa:** Il sistema ora genera un set completo di dati anagrafici, includendo:
  - **Info Documento:** Numero, data di rilascio/scadenza, paese di rilascio.
  - **Info Residenza:** Nazionalità completa (da una lista di tutte le nazioni), luogo di nascita, indirizzo, città, CAP e paese di residenza.
  - **Info Contatto:** Prefisso, numero di cellulare ed email (con default fisso).
  - **Info Emergenza:** Prefisso, numero e nome di un contatto. Il nome del contatto di emergenza è garantito essere unico all'interno di una singola generazione di gruppo.
- **Supporto Multi-Nazionalità:** Attualmente supporta Italia (IT) e Stati Uniti (US).
- **Formattazione Data Dinamica:** L'indicatore della data si adatta in tempo reale basandosi sulla nazionalità scelta: `GG/MM/AAAA` per IT e `MM/DD/YYYY` per US.
- **Categorizzazione Età:** Calcola l'età automaticamente dalla data di nascita assegnando una Categoria: Infant (`I` <= 2 anni), Junior (`J` < 18 anni), Adult (`A` >= 18 anni).
- **Visualizzazione Divisa:** Schermo diviso tra operazioni recenti (Dati appena generati/inseriti) e lo storico totale (Database locale).
- **Filtro di Ricerca:** Possibilità di cercare tra i vecchi clienti all'interno del database per Nome, Cognome, Sesso e Nazionalità.
- **Eliminazione Record:** È stato aggiunto un pulsante per eliminare in modo permanente un record selezionato dal database, con richiesta di conferma.
- **Copia Rapida Silenziosa:** Cliccando col tasto destro del mouse su un record è possibile copiare la riga direttamente negli appunti del PC senza subire l'interruzione di popup e avvisi.
- **Salvataggio Intelligente:** I dati vengono aggiunti al file `database.csv`. L'app migra automaticamente vecchi database sprovvisti della colonna 'Categoria' aggiornandoli silenziosamente.
- **Tema Scuro Nativo di Default:** L'applicazione si avvia in modalità Dark Mode ad Alto Contrasto, per alleggerire lo stress oculare dell'utilizzatore. È presente un pulsante per passare alla versione chiara tradizionale.
- **Guida Estensione Chrome:** È stato aggiunto un file `CHROME_EXTENSION_GUIDE.md` che spiega come creare un'estensione per l'autofill dei moduli web.
## 3. Struttura del Progetto

Il progetto è composto dai seguenti file:

- **`gui_app.py`**:
  - Contiene il codice per l'interfaccia grafica creata con `tkinter`.
  - Gestisce il Layout (incluso il nuovo campo `Voyagerclub No.`) e gli stili (inclusi i font bold per le etichette).
  - Aggiunge e gestisce le scrollbar orizzontali per le tabelle.
  - Popola dinamicamente le tabelle con tutti i nuovi campi.
  - Gestisce la funzione del menu contestuale per copiare i dati col mouse.
  - Gestisce la logica di eliminazione del record selezionato.
  - Filtra il database chiamando i dati in sola-lettura.

- **`home.py`**:
  - Contiene la logica di business del programma.
  - `get_category_from_date()`: Metodo che deduce matematicamente I/J/A da un oggetto `datetime`.
  - `generate_passenger_data()`: Logica estesa per creare tutti i nuovi campi (documento, residenza, contatti) e per garantire l'unicità dei contatti di emergenza.
  - `read_from_csv()`: Legge l'intero database.
  - `save_to_csv()`: Aggiunge nuovi record al database.
  - `delete_record_by_doc_num()`: Rimuove un record specifico dal database e lo riscrive.

- **`database.csv`**:
  - File generato automaticamente al primo avvio.
  - Contiene i dati in formato CSV (Comma-Separated Values).

- **`INSTALLAZIONE.md`**: Guida per l'installazione e l'avvio.
- **`CHROME_EXTENSION_GUIDE.md`**: Guida per la creazione di un'estensione per l'autofill.
- **`DOCUMENTAZIONE.md`**: Questo file.

## 4. Come Aggiornare la Documentazione

Questa documentazione dovrebbe essere mantenuta aggiornata ad ogni modifica significativa del codice.

- **Nuova Funzionalità?** Aggiungila alla sezione "Funzionalità Principali".
- **Modifica a un file?** Aggiorna la sua descrizione nella "Struttura del Progetto".
- **Cambiamento importante?** Potrebbe essere utile aggiornare la versione e la data all'inizio del documento.