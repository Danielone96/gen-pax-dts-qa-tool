# Gen_Pax_Dts - QA Test Data Generator & Autofill Tool 🚀

![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)
![Testing](https://img.shields.io/badge/QA-Test%20Automation-success.svg)

**Gen_Pax_Dts** è uno strumento ibrido (App Desktop Python + Estensione Chrome) sviluppato per ottimizzare le fasi di *Software Testing* e *Data Entry*. 

Nasce dall'esigenza di velocizzare i test esplorativi ed end-to-end su sistemi di prenotazione e form complessi, eliminando il collo di bottiglia della generazione e dell'inserimento manuale di dati anagrafici realistici.

## 🎯 Funzionalità Principali

1. **Test Data Management (Python GUI):**
   - Generazione automatica e massiva di passeggeri fittizi completi (Nomi, Documenti, Indirizzi, Contatti di emergenza).
   - Gestione intelligente di *Edge Cases*: calcolo automatico della fascia d'età (Infant, Junior, Adult), formati data internazionali (IT/US), e coerenza dei generi.
   - Salvataggio cumulativo in un database locale (`database.csv`) per garantire la riproducibilità dei test.

2. **Data Injection (Estensione Google Chrome):**
   - Interfaccia integrata nel browser per l'inserimento istantaneo (Autofill) dei dati generati all'interno della DOM dell'applicazione web in test.
   - Capacità di isolare chirurgicamente i blocchi HTML per compilare form multipli (es. Passeggero 1 e Passeggero 2) nella stessa pagina senza sovrascrivere dati errati.
   - Supporto alla generazione casuale *"On the fly"* direttamente dal browser, riempiendo solo i campi lasciati vuoti per velocizzare i flussi.

## 🛠️ Stack Tecnologico
* **Core Logic & GUI:** Python 3, Tkinter, CSV
* **Browser Extension:** JavaScript (ES6+), HTML, CSS, Chrome Extensions API (Manifest V3)

## 🚀 Installazione e Utilizzo
Consulta i file di documentazione dedicati per i dettagli su come eseguire lo strumento:
* Guida all'installazione dell'App Python
* Documentazione dell'Estensione Chrome
* Documentazione Architetturale Completa

---
*Progetto concepito e sviluppato da Davide Cardella come Custom QA Tool.*