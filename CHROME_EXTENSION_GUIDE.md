# Guida alla Creazione di un'Estensione Chrome per l'Autofill

Questa guida spiega concettualmente come creare una semplice estensione per Google Chrome che possa prendere i dati di un passeggero copiati da **Gen_Pax_Dts** e usarli per compilare automaticamente i campi di un modulo su un sito web.

**Nota:** Questa è una guida di base. Ogni sito web è diverso, quindi l'estensione dovrà essere personalizzata per funzionare su uno specifico sito di destinazione.

## 1. Struttura dei File dell'Estensione

Un'estensione di Chrome è essenzialmente un insieme di file (HTML, CSS, JavaScript). Crea una nuova cartella (es. `autofill-extension`) e al suo interno crea i seguenti tre file:

### a) `manifest.json`

Questo è il file più importante. Dice a Chrome tutto sulla tua estensione: il suo nome, i permessi di cui ha bisogno, ecc.

```json
{
  "manifest_version": 3,
  "name": "Gen_Pax_Dts Autofill",
  "version": "1.0",
  "description": "Compila i moduli web con i dati copiati da Gen_Pax_Dts.",
  "permissions": [
    "activeTab",
    "scripting",
    "clipboardRead"
  ],
  "action": {
    "default_popup": "popup.html"
  }
}
```
*   **`permissions`**: Chiediamo il permesso di leggere gli appunti (`clipboardRead`), di interagire con la scheda attiva (`activeTab`) e di eseguire script su di essa (`scripting`).
*   **`action`**: Definisce cosa succede quando clicchi sull'icona dell'estensione (apre `popup.html`).
*   **`icons`**: Avrai bisogno di creare delle icone (puoi usare un generatore online) e salvarle nella cartella. Per iniziare, non sono obbligatorie.

### b) `popup.html`

Questa è la piccola finestra che appare quando fai clic sull'icona dell'estensione.

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { width: 220px; text-align: center; font-family: sans-serif; padding: 10px; background-color: #f9f9f9; }
    .button-container { display: flex; justify-content: space-between; gap: 5px; margin-top: 10px; }
    button { width: 100%; padding: 10px; cursor: pointer; border-radius: 5px; font-weight: bold; font-size: 14px;}
    .btn-pax1 { background-color: #4CAF50; color: white; border: 1px solid #3d8b40; }
    .btn-pax1:hover { background-color: #45a049; }
    .btn-pax2 { background-color: #2196F3; color: white; border: 1px solid #1976D2; }
    .btn-pax2:hover { background-color: #0b7dda; }
    p { font-size: 12px; color: #555; margin-bottom: 5px;}
  </style>
</head>
<body>
  <h3>Gen_Pax_Dts Autofill</h3>
  <p>Copia una riga e scegli chi compilare:</p>
  <div class="button-container">
    <button id="btnPax1" class="btn-pax1">Pax 1</button>
    <button id="btnPax2" class="btn-pax2">Pax 2</button>
  </div>
  <script src="popup.js"></script>
</body>
</html>
```

### c) `content_script.js`

Questo script verrà iniettato nella pagina web che stai visitando. Sarà lui a compilare materialmente i campi.

```javascript
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "fill_form") {
    const data = request.data;
    const paxIndex = request.paxIndex; // ECCO LA RIGA CHE MANCAVA!
    
    console.log(`\n--- INIZIO COMPILAZIONE PER PAX ${paxIndex + 1} ---`);
    console.log("Dati ricevuti per la compilazione:", data);

    // Molti siti per il "Gender" vogliono la parola intera al posto di M/F
    let genderFull = data[3];
    if (data[3] === 'M') genderFull = 'Male';
    if (data[3] === 'F') genderFull = 'Female';

    // Funzione 1: Compilazione Diretta tramite Selettore (Infallibile e Sicura)
    function fillFieldBySelector(selector, value, fieldName) {
      if (!value || !value.trim()) return false;
      try {
        // Seleziona tutti gli input con quel nome e usa l'indice del passeggero per saltare al successivo
        const inputElements = document.querySelectorAll(selector);
        const inputElement = inputElements[paxIndex];
        
        if (inputElement) {
          inputElement.focus();
          const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value")?.set;
          if (nativeInputValueSetter) nativeInputValueSetter.call(inputElement, value);
          else inputElement.value = value;
          
          inputElement.dispatchEvent(new KeyboardEvent('keydown', { key: 'a', bubbles: true }));
          inputElement.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
          inputElement.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
          inputElement.dispatchEvent(new KeyboardEvent('keyup', { key: 'a', bubbles: true }));
          inputElement.blur();
          console.log(`🎯 [${fieldName}] compilato -> ${value}`);
          return true;
        }
      } catch (e) {
        console.error(`❌ Errore con selettore ${selector}:`, e);
      }
      return false;
    }

    // Funzione 2: Compilazione tramite Testo Exact Match
    function fillFieldByLabelText(labelText, value, targetIndexWithinPax = 0, totalOccurrencesPerPax = 1, exactMatch = true) {
      if (!value || !value.trim()) return;
      try {
        // Cerca in tutti i tag di testo (non solo label) per trovare campi come "Contact Name"
        const allTextElements = Array.from(document.querySelectorAll('label, span, div, p, strong, b'));
        
        const matchingLabels = allTextElements.filter(el => {
            // Verifica che sia un elemento foglia o quasi (evita di prendere l'intera pagina)
            if (el.children.length > 2) return false;
            
            // Estrae solo il testo "pulito" ignorando gli <span> degli asterischi
            let directText = "";
            for (let i = 0; i < el.childNodes.length; i++) {
                if (el.childNodes[i].nodeType === Node.TEXT_NODE) {
                    directText += el.childNodes[i].nodeValue;
                }
            }
            
            // Normalizza spazi e accapo
            directText = directText.replace(/\s+/g, ' ').trim().toLowerCase();
            const search = labelText.replace(/\s+/g, ' ').trim().toLowerCase();
            
            // Match esatto previene confusioni tra "Phone Number" e "Company Phone Number"
            const isMatch = exactMatch ? (directText === search) : directText.includes(search);
            const isVisible = el.offsetWidth > 0 || el.offsetHeight > 0 || el.getClientRects().length > 0;
            return isMatch && isVisible;
        });
        
        // Rimuove eventuali doppioni causati da div annidati con lo stesso testo
        const uniqueLabels = [];
        matchingLabels.forEach(el => {
           if (!uniqueLabels.some(u => u.contains(el) || el.contains(u))) {
               uniqueLabels.push(el);
           }
        });
        
        // CALCOLO MATEMATICO: Salta le etichette dei passeggeri precedenti
        const absoluteIndex = (paxIndex * totalOccurrencesPerPax) + targetIndexWithinPax;
        const targetLabel = uniqueLabels[absoluteIndex];

        if (targetLabel) {
          let inputElement = null;
          let currentParent = targetLabel.parentElement;
          let searchDepth = 15; 
          
          while (currentParent && searchDepth > 0 && !inputElement) {
            inputElement = currentParent.querySelector('input:not([type="hidden"]), textarea, select');
            currentParent = currentParent.parentElement;
            searchDepth--;
          }

          if (!inputElement) {
            const allElements = Array.from(document.querySelectorAll('*'));
            const labelIndex = allElements.indexOf(targetLabel);
            const limit = Math.min(labelIndex + 50, allElements.length);
            for (let i = labelIndex + 1; i < limit; i++) {
                const el = allElements[i];
                if ((el.tagName === 'INPUT' && el.type !== 'hidden') || el.tagName === 'SELECT' || el.tagName === 'TEXTAREA') {
                    if (el.offsetWidth > 0 || el.offsetHeight > 0) {
                        inputElement = el;
                        break;
                    }
                }
            }
          }

          if (!inputElement) {
            const forId = targetLabel.getAttribute('for');
            if (forId) inputElement = document.getElementById(forId);
          }

          if (inputElement) {
            inputElement.focus();
            let proto = window.HTMLInputElement.prototype;
            if (inputElement.tagName === 'SELECT') {
              proto = window.HTMLSelectElement.prototype;
              const option = Array.from(inputElement.options).find(opt => 
                opt.text.toLowerCase().includes(value.toLowerCase()) || 
                opt.value.toLowerCase() === value.toLowerCase()
              );
              if (option) value = option.value;
            }
            if (inputElement.tagName === 'TEXTAREA') proto = window.HTMLTextAreaElement.prototype;

            // 3. Setter Nativo Corazzato
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(proto, "value")?.set;
            if (nativeInputValueSetter) {
              nativeInputValueSetter.call(inputElement, value);
            } else {
              inputElement.value = value;
            }

            inputElement.dispatchEvent(new KeyboardEvent('keydown', { key: 'a', bubbles: true }));
            inputElement.dispatchEvent(new Event('input', { bubbles: true, composed: true }));
            inputElement.dispatchEvent(new Event('change', { bubbles: true, composed: true }));
            inputElement.dispatchEvent(new KeyboardEvent('keyup', { key: 'a', bubbles: true }));
            inputElement.blur(); 
            console.log(`✅ [${labelText}] compilato -> ${value}`);
          } else {
            console.warn(`⚠️ Trovata l'etichetta "${labelText}", ma NON il campo associato.`);
          }
        } else {
          console.warn(`⚠️ Etichetta "${labelText}" NON trovata per PAX ${paxIndex + 1} (Indice calcolato: ${absoluteIndex}).`);
        }
      } catch (e) {
        console.error(`❌ Errore critico con l'etichetta "${labelText}":`, e);
      }
    }

    fillFieldByLabelText('First Name', data[0]);
    fillFieldByLabelText('Last Name', data[1]);
    fillFieldByLabelText('Gender', genderFull); 
    fillFieldByLabelText('Date of Birth', data[2]);
    fillFieldByLabelText('Nationality', data[7]);
    fillFieldByLabelText('Place of Birth', data[8]);
    
    // Il campo Document Number compare 2 volte per ogni passeggero. Prendiamo il primo (0).
    fillFieldByLabelText('Document Number', data[9], 0, 2);
    
    // Compila la tendina del Tipo Documento impostandola su Passport
    fillFieldByLabelText('Document', 'Passport'); 

    fillFieldByLabelText('Date of Issue', data[10]); 
    
    // Il campo Date of expiration compare 2 volte per ogni passeggero. Prendiamo il primo (0).
    fillFieldByLabelText('Date of expiration', data[11], 0, 2); 
    fillFieldByLabelText('Country of Issue', data[12]); 
    fillFieldByLabelText('Address 1', data[13]);
    fillFieldByLabelText('City', data[14]);
    fillFieldByLabelText('Country of Residence', data[15]);
    fillFieldByLabelText('Zip code', data[16]);

    // Tentativo diretto e sicuro con Cecchino per i due campi ostinati:
    if (!fillFieldBySelector('input[name="mob"]', data[18], 'Mobile Number')) {
        fillFieldByLabelText('Mobile Number', data[18]);
    }
    if (!fillFieldBySelector('input[name="freeEmail"]', data[19], 'Email Address')) {
        fillFieldByLabelText('Email Address', data[19]);
    }

    // Le etichette duplicate vanno gestite specificando il (Totale Volte Per Passeggero)
    fillFieldByLabelText('Prefix', data[17], 0, 3); // Prefix Mobile (1 di 3)
    fillFieldByLabelText('Prefix', data[20], 2, 3); // Prefix Emergenza (3 di 3)
    
    // Grazie al Match Esatto, "Phone Number" compare esattamente 1 volta.
    fillFieldByLabelText('Phone Number', data[21]); 
    
    // Contact Name che ora verrà trovato anche se è un semplice span o div!
    fillFieldByLabelText('Contact Name', data[22]);
    
    console.log(`--- Fine compilazione PAX ${paxIndex + 1} ---`);
  }
});
```

### d) `popup.js`

Questo script gestisce la logica del popup, come la lettura degli appunti e l'invio dei dati al `content_script.js`.

```javascript
// Funzione generale per innescare l'autofill passando l'indice del passeggero (0 o 1)
async function triggerAutofill(paxIndex) {
  try {
    const clipboardText = await navigator.clipboard.readText();
    const passengerData = clipboardText.split(' | ');

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content_script.js']
    }, () => {
        // Inviamo i dati E l'indice (paxIndex)
        chrome.tabs.sendMessage(tab.id, { action: "fill_form", data: passengerData, paxIndex: paxIndex });
    });

  } catch (err) {
    alert("Errore: Impossibile leggere dagli appunti. Assicurati di aver copiato una riga da Gen_Pax_Dts.");
  }
}

// Colleghiamo i due pulsanti alla funzione
document.getElementById('btnPax1').addEventListener('click', () => triggerAutofill(0));
document.getElementById('btnPax2').addEventListener('click', () => triggerAutofill(1));
```

## 2. Come Usare l'Estensione

1.  **Copia i Dati**: In `Gen_Pax_Dts`, fai clic con il tasto destro su un passeggero e seleziona "Copia Dati".
2.  **Apri il Sito Web**: Naviga fino alla pagina web con il modulo che vuoi compilare.
3.  **Attiva l'Estensione**: Fai clic sull'icona della tua estensione nella barra di Chrome.
4.  **Compila**: Fai clic sul pulsante "Compila Modulo". Lo script tenterà di riempire i campi.

## 3. Installare l'Estensione in Chrome

1.  Apri Chrome e vai all'indirizzo `chrome://extensions`.
2.  In alto a destra, attiva la levetta **"Modalità sviluppatore"**.
3.  Appariranno dei nuovi pulsanti. Fai clic su **"Carica estensione non pacchettizzata"**.
4.  Seleziona la cartella che hai creato (`autofill-extension`) dove hai salvato i 4 file.
5.  L'estensione apparirà nella lista e la sua icona sarà visibile nella barra degli strumenti di Chrome.

Ora sei pronto per testarla! Ricorda che la parte più complessa è adattare il `content_script.js` per trovare i campi giusti su ogni sito web.