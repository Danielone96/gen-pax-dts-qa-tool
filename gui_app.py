import tkinter as tk
from tkinter import ttk, messagebox
import home
from datetime import datetime
import random

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gen_Pax_Dts v1.4")
        self.geometry("1000x800")

        # Inizializza Variabili Tema Scuro
        self.is_dark_mode = True # Impostato come default
        self.setup_styles()      # Carica subito i colori scuri ad alto contrasto

        # --- Menu contestuale (Tasto Destro) ---
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copia Dati", command=self.copy_selected)
        self.current_tree = None

        # --- Top Bar (Tema Scuro) ---
        top_bar = ttk.Frame(self)
        top_bar.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.btn_theme = ttk.Button(top_bar, text="☀️ Tema Chiaro", command=self.toggle_theme)
        self.btn_theme.pack(side=tk.RIGHT)

        # --- Input Frame (Unificato) ---
        input_frame = ttk.LabelFrame(self, text="Generazione e Inserimento Dati (Lascia vuoti i campi per la generazione casuale)", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # Stile per etichette specifiche
        style = ttk.Style(self)
        style.configure("Bold.TLabel", font=('Helvetica', 9, 'bold'))

        # Riga 0
        ttk.Label(input_frame, text="Numero Totale Record:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.num_passengers_var = tk.StringVar(value="2")
        ttk.Spinbox(input_frame, from_=1, to=100, textvariable=self.num_passengers_var, width=5).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Di cui Junior (<18 anni):").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.num_junior_var = tk.StringVar(value="0")
        ttk.Spinbox(input_frame, from_=0, to=100, textvariable=self.num_junior_var, width=5).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Sesso:", style="Bold.TLabel").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.man_sesso = tk.StringVar(value="Casuale")
        ttk.Combobox(input_frame, textvariable=self.man_sesso, values=["Casuale", "M", "F"], state="readonly", width=8).grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)

        # Riga 1
        ttk.Label(input_frame, text="Nome:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.man_nome = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.man_nome).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Cognome:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.man_cognome = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.man_cognome).grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Riga 2
        ttk.Label(input_frame, text="Nazionalità (per Nomi):", style="Bold.TLabel").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.nationality_var = tk.StringVar(value="IT")
        nat_combo = ttk.Combobox(input_frame, textvariable=self.nationality_var, values=["IT", "US"], state="readonly", width=5)
        nat_combo.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        nat_combo.bind("<<ComboboxSelected>>", self.update_date_hint)

        self.date_hint_var = tk.StringVar(value="Data Nascita (GG/MM/AAAA):")
        ttk.Label(input_frame, textvariable=self.date_hint_var).grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.man_data = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.man_data).grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        # Riga 3
        ttk.Label(input_frame, text="Club No.:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.man_voyager = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.man_voyager).grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Membership:").grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.man_membership = tk.StringVar(value="")
        ttk.Combobox(input_frame, textvariable=self.man_membership, values=["", "Classic", "Silver", "Gold", "Diamond"], state="readonly", width=10).grid(row=3, column=3, padx=5, pady=5, sticky=tk.W)

        # Riga 4 (Pulsante Centrale)
        ttk.Button(input_frame, text="Genera / Aggiungi Dati", command=self.process_unified_generation).grid(row=4, column=0, columnspan=6, pady=(10, 0))

        # --- Area Divisa: Nuovi Dati (Sopra) e Vecchi Dati (Sotto) ---
        paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        paned.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Frame Dati Recenti
        frame_new = ttk.LabelFrame(paned, text="Dati Generati/Inseriti nella Sessione Corrente", padding="10")
        paned.add(frame_new, weight=1)
        self.tree_new = self.create_treeview(frame_new)

        # Sistema a Schede (Notebook) per il Database
        notebook_frame = ttk.LabelFrame(paned, text="Archivio Dati", padding="10")
        paned.add(notebook_frame, weight=2)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # --- TAB 1: Database Completo ---
        tab1_db = ttk.Frame(self.notebook)
        self.notebook.add(tab1_db, text="Tutti i Clienti")

        filter_frame = ttk.Frame(tab1_db)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filtra per:", style="Bold.TLabel").pack(side=tk.LEFT, padx=(0, 5))
        self.search_field = tk.StringVar(value="Tutti")
        ttk.Combobox(filter_frame, textvariable=self.search_field, values=["Tutti", "Nome", "Cognome", "Sesso", "Nazionalità"], state="readonly", width=12).pack(side=tk.LEFT, padx=5)
        
        self.search_query = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.search_query).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(filter_frame, text="Cerca", command=self.load_old_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Mostra Tutti", command=self.reset_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="❌ Elimina", command=self.delete_selected_record).pack(side=tk.RIGHT, padx=5)
        ttk.Button(filter_frame, text="✏️ Modifica", command=self.edit_selected_record).pack(side=tk.RIGHT, padx=5)

        self.tree_old = self.create_treeview(tab1_db)

        # --- TAB 2: Voyager Club ---
        tab2_voyager = ttk.Frame(self.notebook)
        self.notebook.add(tab2_voyager, text="Voyager Club")

        filter_voyager_frame = ttk.Frame(tab2_voyager)
        filter_voyager_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_voyager_frame, text="Filtra per Membership:", style="Bold.TLabel").pack(side=tk.LEFT, padx=(0, 5))
        self.voyager_filter_var = tk.StringVar(value="Tutti")
        voy_combo = ttk.Combobox(filter_voyager_frame, textvariable=self.voyager_filter_var, values=["Tutti", "Classic", "Silver", "Gold", "Diamond"], state="readonly", width=12)
        voy_combo.pack(side=tk.LEFT, padx=5)
        voy_combo.bind("<<ComboboxSelected>>", lambda e: self.load_old_data())

        self.tree_voyager = self.create_voyager_treeview(tab2_voyager)
        
        # Caricamento Iniziale Database
        self.load_old_data()

    def create_treeview(self, parent_frame):
        # Definizione di tutte le colonne
        columns = (
            "nome", "cognome", "data_nascita", "sesso", "nazionalita", "categoria", "voyagerclub_no",
            "membership", "nationality_full", "place_of_birth", "document_number", "date_of_issue", "date_of_expiration",
            "country_of_issue", "address_1", "city", "country_of_residence", "zip_code", "prefix",
            "mobile_number", "email_address", "emergency_prefix", "emergency_phone", "emergency_contact_name"
        )
        
        # Mappatura 'id_colonna' -> 'Testo Intestazione'
        headings = {
            "nome": "Nome", "cognome": "Cognome", "data_nascita": "Data Nascita", "sesso": "Sesso",
            "nazionalita": "Naz. Gen.", "categoria": "Cat.", "voyagerclub_no": "Club No.", "membership": "Membership",
            "nationality_full": "Nazionalità", "place_of_birth": "Luogo Nascita", "document_number": "Doc. Numero",
            "date_of_issue": "Doc. Rilascio", "date_of_expiration": "Doc. Scadenza", "country_of_issue": "Doc. Paese",
            "address_1": "Indirizzo", "city": "Città", "country_of_residence": "Paese Residenza",
            "zip_code": "CAP", "prefix": "Prefisso", "mobile_number": "Cellulare",
            "email_address": "Email", "emergency_prefix": "Pref. Emergenza", "emergency_phone": "Tel. Emergenza",
            "emergency_contact_name": "Contatto Emergenza"
        }

        tree = ttk.Treeview(parent_frame, columns=columns, show="headings")

        for col, text in headings.items():
            tree.heading(col, text=text)
            tree.column(col, width=120, anchor=tk.W) # Larghezza di default

        # Personalizzazione larghezze specifiche
        tree.column("sesso", width=50, anchor=tk.CENTER)
        tree.column("nazionalita", width=70, anchor=tk.CENTER)
        tree.column("categoria", width=50, anchor=tk.CENTER)
        tree.column("prefix", width=60, anchor=tk.CENTER)
        tree.column("emergency_prefix", width=100, anchor=tk.CENTER)
        tree.column("email_address", width=180)
        tree.column("emergency_contact_name", width=150)

        # --- Scrollbar Orizzontale e Verticale ---
        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=tree.yview)        
        x_scrollbar = ttk.Scrollbar(parent_frame, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Packing: prima le scrollbar, poi il treeview
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Binding per Tasto Destro (copia)
        tree.bind("<Button-3>", lambda event, t=tree: self.show_context_menu(event, t))
        # Aggiungo binding per il doppio click per caricare i dati (futura feature?)
        
        return tree

    def create_voyager_treeview(self, parent_frame):
        # Treeview ridotto solo per Voyager Club
        columns = ("membership", "voyagerclub_no", "nome", "cognome")
        headings = {"membership": "Membership", "voyagerclub_no": "Club No.", "nome": "Nome", "cognome": "Cognome"}

        tree = ttk.Treeview(parent_frame, columns=columns, show="headings")
        
        for col, text in headings.items():
            tree.heading(col, text=text)
            tree.column(col, width=150, anchor=tk.W)
            
        tree.column("membership", width=100, anchor=tk.CENTER)
        tree.column("voyagerclub_no", width=120, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(parent_frame, orient=tk.VERTICAL, command=tree.yview)        
        tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Permette di copiare i dati anche da questa tabella (copierà solo i 4 campi visualizzati)
        tree.bind("<Button-3>", lambda event, t=tree: self.show_context_menu(event, t))
        return tree

    def show_context_menu(self, event, tree):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            self.current_tree = tree
            self.context_menu.post(event.x_root, event.y_root)

    def copy_selected(self):
        if not self.current_tree: return
        selected = self.current_tree.selection()
        if selected:
            values = self.current_tree.item(selected[0])['values']
            text = " | ".join(str(v) for v in values)
            self.clipboard_clear()
            self.clipboard_append(text)

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        if not self.is_dark_mode:
            # Nuovo Tema Chiaro Moderno (Material Light)
            bg_color = '#F3F4F6'
            element_bg = '#FFFFFF'
            text_color = '#202124'
            accent_color = '#0b57d0'
            btn_bg = '#E1E3E1'
            
            self.configure(bg=bg_color)
            
            # Forza i colori del menu a tendina (Listbox aperto)
            self.option_add("*TCombobox*Listbox.background", element_bg)
            self.option_add("*TCombobox*Listbox.foreground", text_color)
            self.option_add("*TCombobox*Listbox.selectBackground", accent_color)
            self.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

            style.configure(".", background=bg_color, foreground=text_color, fieldbackground=element_bg, insertcolor=text_color)
            style.configure("TLabel", background=bg_color, foreground=text_color)
            style.configure("TEntry", fieldbackground=element_bg, foreground=text_color, insertcolor=text_color)
            style.configure("TCombobox", fieldbackground=element_bg, foreground=text_color, selectbackground=accent_color, selectforeground="#ffffff")
            
            # Stile Combobox e mappatura per lo stato Readonly
            style.configure("TCombobox", fieldbackground=element_bg, foreground=text_color)
            style.map("TCombobox", fieldbackground=[('readonly', element_bg)], selectbackground=[('readonly', accent_color)], selectforeground=[('readonly', '#ffffff')])
            
            style.configure("TSpinbox", fieldbackground=element_bg, foreground=text_color, insertcolor=text_color)
            style.configure("TLabelframe", background=element_bg, foreground=text_color)
            style.configure("TLabelframe.Label", background=element_bg, foreground=accent_color, font=('Helvetica', 9, 'bold'))
            
            # Stile per le Schede (Notebook)
            style.configure("TNotebook", background=bg_color, borderwidth=0)
            style.configure("TNotebook.Tab", background=btn_bg, foreground=text_color, padding=[10, 2], font=('Helvetica', 9, 'bold'))
            style.map("TNotebook.Tab", background=[("selected", element_bg)], foreground=[("selected", accent_color)])
            
            style.configure("Treeview", background=element_bg, foreground=text_color, fieldbackground=element_bg, bordercolor="#cccccc")
            style.configure("Treeview.Heading", background=btn_bg, foreground=text_color, font=('Helvetica', 9, 'bold'))
            style.map("Treeview", background=[('selected', accent_color)], foreground=[('selected', '#ffffff')])
            style.configure("TButton", background=btn_bg, foreground=text_color, font=('Helvetica', 9, 'bold'))
            style.map("TButton", background=[('active', '#d2d4d2')])
        else:
            # Nuovo Tema Scuro Moderno (Material Dark)
            bg_color = '#202124'
            element_bg = '#292A2D'
            input_bg = '#3C4043'
            text_color = '#E8EAED'
            accent_color = '#8AB4F8'
            btn_bg = '#3C4043'

            self.configure(bg=bg_color)
            style.configure(".", background=bg_color, foreground=text_color, fieldbackground=input_bg, insertcolor=text_color, bordercolor=bg_color, lightcolor=bg_color, darkcolor=bg_color)
            
            # Forza i colori del menu a tendina nel tema scuro
            self.option_add("*TCombobox*Listbox.background", input_bg)
            self.option_add("*TCombobox*Listbox.foreground", text_color)
            self.option_add("*TCombobox*Listbox.selectBackground", accent_color)
            self.option_add("*TCombobox*Listbox.selectForeground", "#202124")

            style.configure(".", background=bg_color, foreground=text_color, fieldbackground=input_bg, insertcolor=text_color)
            style.configure("TLabel", background=bg_color, foreground=text_color)
            style.configure("TEntry", fieldbackground=input_bg, foreground=text_color, insertcolor=text_color)
            style.configure("TCombobox", fieldbackground=input_bg, foreground=text_color, selectbackground=accent_color, selectforeground="#202124")
            
            # Stile Combobox e mappatura per lo stato Readonly
            style.configure("TCombobox", fieldbackground=input_bg, foreground=text_color)
            style.map("TCombobox", fieldbackground=[('readonly', input_bg)], selectbackground=[('readonly', accent_color)], selectforeground=[('readonly', '#202124')])
            
            style.configure("TSpinbox", fieldbackground=input_bg, foreground=text_color, insertcolor=text_color, arrowcolor=text_color)
            style.configure("TLabelframe", background=element_bg, foreground=text_color, bordercolor="#5f6368")
            style.configure("TLabelframe.Label", background=element_bg, foreground=accent_color, font=('Helvetica', 9, 'bold'))
            
            # Stile per le Schede (Notebook)
            style.configure("TNotebook", background=bg_color, borderwidth=0)
            style.configure("TNotebook.Tab", background=btn_bg, foreground=text_color, padding=[10, 2], font=('Helvetica', 9, 'bold'))
            style.map("TNotebook.Tab", background=[("selected", element_bg)], foreground=[("selected", accent_color)])

            style.configure("Treeview", background=element_bg, foreground=text_color, fieldbackground=element_bg, borderwidth=0)
            style.configure("Treeview.Heading", background=btn_bg, foreground=text_color, font=('Helvetica', 9, 'bold'), relief="flat")
            style.map("Treeview", background=[('selected', '#3b5b82')], foreground=[('selected', '#ffffff')])
            style.configure("TButton", background=btn_bg, foreground=text_color, font=('Helvetica', 9, 'bold'))
            style.map("TButton", background=[('active', '#5f6368')])

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.btn_theme.config(text="☀️ Tema Chiaro" if self.is_dark_mode else "🌙 Tema Scuro")
        self.setup_styles()

    def update_date_hint(self, event=None):
        if self.nationality_var.get() == "IT":
            self.date_hint_var.set("Data Nascita (GG/MM/AAAA):")
        else:
            self.date_hint_var.set("Data Nascita (MM/DD/YYYY):")

    def process_unified_generation(self):
        try:
            num = int(self.num_passengers_var.get())
            num_jun = int(self.num_junior_var.get())
            if num <= 0 or num_jun < 0 or num_jun > num:
                raise ValueError
        except ValueError:
            messagebox.showerror("Errore", "Valori record non validi.\nEs: Totale 3, Junior 1 (Significa 2 Adulti e 1 Junior).")
            return

        naz = self.nationality_var.get()
        in_nome = self.man_nome.get().strip().capitalize()
        in_cognome = self.man_cognome.get().strip().capitalize()
        in_data = self.man_data.get().strip()
        in_sesso = self.man_sesso.get()
        in_voyager = self.man_voyager.get().strip()
        in_membership = self.man_membership.get()

        new_data = []
        for i in range(num):
            # Identifica se questa iterazione deve generare un junior o un adulto
            age_cat = 'minor' if i < num_jun else 'adult'
            
            # Genera record con vincolo di età
            p = home.generate_passenger_data(1, naz, age_category=age_cat)[0]

            # Sovrascrive il Sesso e bilancia il nome
            if in_sesso != "Casuale":
                p['sesso'] = in_sesso
                if not in_nome:
                    # Mantiene la concordanza sesso/nome se forzato dal manuale
                    if naz == 'IT':
                        p['nome'] = random.choice(home.first_names_m_it if in_sesso == 'M' else home.first_names_f_it)
                    else:
                        p['nome'] = random.choice(home.first_names_m_us if in_sesso == 'M' else home.first_names_f_us)

            # Sovrascrive le preferenze testuali forzate SOLO per il primo passeggero
            if i == 0:
                if in_nome: p['nome'] = in_nome
                if in_cognome: p['cognome'] = in_cognome
                if in_voyager: p['voyagerclub_no'] = in_voyager
                if in_membership: p['membership'] = in_membership
                
                # Gestione data forzata
                if in_data:
                    fmt = "%d/%m/%Y" if naz == 'IT' else "%m/%d/%Y"
                    try:
                        dt = datetime.strptime(in_data, fmt)
                        p['data_nascita'] = dt.strftime(fmt) # Assicura la sintassi perfetta
                        p['categoria'] = home.get_category_from_date(dt)
                    except ValueError:
                        messagebox.showerror("Errore Data", f"Hai inserito una data non compatibile.\nFormato richiesto: {fmt} per {naz}")
                        return

            new_data.append(p)

        self.process_new_data(new_data)
        
        # Svuota i campi opzionali pronti per una nuova generazione ma mantiene i contatori comodi
        # (Non respiro il numero_record in modo da permettere multiple generazioni veloci)
        self.num_junior_var.set("0")
        self.man_nome.set("")
        self.man_cognome.set("")
        self.man_data.set("")
        self.man_voyager.set("")
        self.man_membership.set("")
        self.man_sesso.set("Casuale")

    def process_new_data(self, new_data):
        try:
            home.save_to_csv(new_data, "database.csv")
        except PermissionError as pe:
            messagebox.showerror("Errore File", str(pe))
            return
        except Exception as e:
            messagebox.showerror("Errore Salvataggio", f"Errore: {e}")
            return

        # Mostra in cima alla tabella dei nuovi dati
        for p in new_data:
            self.tree_new.insert("", 0, values=list(p.values())) # 0 inserisce in cima
            
        self.load_old_data() # Aggiorna il database storico sotto

    def delete_selected_record(self):
        selected_items = self.tree_old.selection()
        if not selected_items:
            messagebox.showwarning("Nessuna Selezione", "Per favore, seleziona un record dalla tabella del database da eliminare.")
            return
        
        selected_item = selected_items[0]
        
        try:
            item_values = self.tree_old.item(selected_item)['values']
            nome = str(item_values[0])
            cognome = str(item_values[1])
            data_nascita = str(item_values[2])
        except (IndexError, ValueError):
            messagebox.showerror("Errore", "Impossibile identificare il record in modo univoco. Dati corrotti?")
            return

        home.delete_record(nome, cognome, data_nascita)
        self.load_old_data() # Ricarica la tabella per mostrare il cambiamento

    def edit_selected_record(self):
        selected_items = self.tree_old.selection()
        if not selected_items:
            messagebox.showwarning("Nessuna Selezione", "Seleziona un record da modificare.")
            return
            
        item = selected_items[0]
        values = self.tree_old.item(item)['values']
        columns = self.tree_old['columns']
        
        # Associa le colonne ai valori correnti
        current_data = dict(zip(columns, values))
        
        # Crea la finestra di Modifica
        edit_win = tk.Toplevel(self)
        edit_win.title("Modifica Utente")
        edit_win.geometry("800x600")
        edit_win.configure(bg=self.cget('bg')) # Applica lo sfondo del tema
        
        # Rimuove i bordi bianchi del canvas
        canvas = tk.Canvas(edit_win, bg=self.cget('bg'), highlightthickness=0)
        scrollbar = ttk.Scrollbar(edit_win, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Ancora il frame per farlo espandere orizzontalmente
        canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_frame, width=e.width))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")
        
        # Configura le colonne per centrare i contenuti
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=1)
        scrollable_frame.columnconfigure(2, weight=1)
        scrollable_frame.columnconfigure(3, weight=1)
        
        entries = {}
        row_idx = 0
        col_idx = 0
        
        for col in columns:
            lbl_text = col.replace("_", " ").title() + ":"
            ttk.Label(scrollable_frame, text=lbl_text).grid(row=row_idx, column=col_idx, padx=(10, 5), pady=8, sticky=tk.E)
            
            var = tk.StringVar(value=str(current_data.get(col, "")))
            
            if col == "membership":
                combo = ttk.Combobox(scrollable_frame, textvariable=var, values=["", "Classic", "Silver", "Gold", "Diamond"], state="readonly", width=23)
                combo.grid(row=row_idx, column=col_idx+1, padx=(5, 20), pady=8, sticky=tk.W)
            else:
                ttk.Entry(scrollable_frame, textvariable=var, width=25).grid(row=row_idx, column=col_idx+1, padx=(5, 20), pady=8, sticky=tk.W)
                
            entries[col] = var
            
            col_idx += 2
            if col_idx > 2:
                col_idx = 0
                row_idx += 1
                
        def save_changes():
            new_dict = {col: var.get() for col, var in entries.items()}
            home.update_record(str(current_data['nome']), str(current_data['cognome']), str(current_data['data_nascita']), new_dict)
            self.load_old_data()
            edit_win.destroy()
            
        ttk.Button(edit_win, text="Salva Modifiche", command=save_changes).pack(pady=10)

    def reset_filter(self):
        self.search_query.set("")
        self.search_field.set("Tutti")
        self.load_old_data()

    def load_old_data(self):
        for item in self.tree_old.get_children():
            self.tree_old.delete(item)
        for item in self.tree_voyager.get_children():
            self.tree_voyager.delete(item)
            
        all_data = home.read_from_csv("database.csv")
        query = self.search_query.get().lower().strip()
        field = self.search_field.get()
        voy_filter = self.voyager_filter_var.get()

        for row in all_data:
            # --- Logica Tab 1 (Tutti i clienti) ---
            match = False
            if not query:
                match = True
            elif field == "Tutti":
                if any(query in str(v).lower() for v in row.values()): match = True
            elif field == "Nome" and query in row.get("nome", "").lower(): match = True
            elif field == "Cognome" and query in row.get("cognome", "").lower(): match = True
            elif field == "Sesso" and query == row.get("sesso", "").lower(): match = True
            elif field == "Nazionalità" and query == row.get("nazionalita", "").lower(): match = True
            
            if match:
                # Usa una list comprehension per caricare dinamicamente tutti i valori nell'ordine corretto
                values = tuple(row.get(col, "") for col in self.tree_old['columns'])
                self.tree_old.insert("", tk.END, values=values)
                
            # --- Logica Tab 2 (Voyager Club) ---
            voy_no = row.get("voyagerclub_no", "").strip()
            if voy_no:
                mem_type = row.get("membership", "")
                if voy_filter == "Tutti" or voy_filter == mem_type:
                    self.tree_voyager.insert("", tk.END, values=(mem_type, voy_no, row.get("nome"), row.get("cognome")))

if __name__ == "__main__":
    app = App()
    app.mainloop()