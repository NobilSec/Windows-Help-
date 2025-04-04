import os
import sys
import subprocess
import tempfile
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import shutil
from PIL import Image, ImageTk, ImageEnhance, ImageDraw, ImageFont
import requests
import io
import socket
import psutil  # Adăugat pentru a gestiona procesele
import winreg  # Pentru modificări în registry
import speedtest  # Import global pentru speedtest

class UtilitarSistem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Windows Help")
        self.geometry("1000x700")
        self.minsize(800, 600)
        
        # Setez iconul aplicației
        self.create_app_icon()
        
        # Configurare tematică negru-roșu
        self.culoare_principala = "#000000"    # Negru
        self.culoare_accent = "#ff0000"        # Roșu vibrant
        self.culoare_secundara = "#1a0000"     # Roșu închis
        self.culoare_tertiara = "#330000"      # Roșu foarte închis
        self.culoare_buton = "#000000"         # Butoane negre
        self.culoare_text = "#ffffff"          # Text alb
        self.culoare_highlight = "#ff3333"     # Highlight
        
        # Configurare fullscreen
        self.attributes('-fullscreen', False)
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        self.bind("<F11>", lambda event: self.toggleFullScreen())
        
        # Inițializare variabile pentru fundal
        self.background_path = self.get_background_image()
        
        # Creează canvas pentru fundal
        self.canvas = tk.Canvas(self, bg=self.culoare_principala, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Inițializează interfața
        self.creaza_interfata()
        
        # Variabilă pentru a stoca fereastra task manager
        self.task_manager_window = None
        
    def toggleFullScreen(self):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))
    
    def get_background_image(self):
        """Descarcă imaginea și o salvează local pentru utilizări ulterioare"""
        try:
            temp_dir = os.path.join(tempfile.gettempdir(), 'app_images')
            os.makedirs(temp_dir, exist_ok=True)
            img_path = os.path.join(temp_dir, 'background.jpg')
            
            # Verifică dacă imaginea există deja local
            if os.path.exists(img_path):
                return img_path
                
            # Descarcă imaginea
            try:
                response = requests.get("https://4kwallpapers.com/images/walls/thumbs_3t/5918.jpg", stream=True)
                response.raise_for_status()
                
                # Salvează imaginea local
                with open(img_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                return img_path
            except:
                return None
        except:
            return None
    
    def creaza_interfata(self):
        # Procesează și aplică imaginea de fundal o singură dată
        self.actualizare_fundal()
        
        # Crează frame-ul principal cu margini pentru efect de strălucire
        self.frame_outer = tk.Frame(
            self, 
            bg=self.culoare_accent,
            highlightbackground=self.culoare_accent,
            highlightthickness=2,
            padx=2, 
            pady=2
        )
        self.frame_outer.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=830, height=650)
        
        # Frame-ul principal
        self.frame_principal = tk.Frame(
            self.frame_outer, 
            bg=self.culoare_secundara,
            bd=0
        )
        self.frame_principal.pack(fill="both", expand=True)
        
        # Crează header
        header_frame = tk.Frame(self.frame_principal, bg=self.culoare_principala, height=60)
        header_frame.pack(fill="x", padx=2, pady=2)
        
        # Titlu principal
        titlu_label = tk.Label(
            header_frame,
            text="UTILITAR SISTEM",
            font=("Arial", 20, "bold"),
            bg=self.culoare_principala,
            fg=self.culoare_accent,
            pady=12
        )
        titlu_label.pack(side="left", padx=20)
        
        # Conținut principal
        content_frame = tk.Frame(self.frame_principal, bg=self.culoare_secundara)
        content_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Frame pentru butoane cu grilă fixă
        self.frame_butoane = tk.Frame(content_frame, bg=self.culoare_secundara, padx=10, pady=10)
        self.frame_butoane.pack(fill="both", expand=True)
        
        # Adaugă butoane în grilă
        butoane_info = [
            {
                "text": "Dezactivează Windows Defender",
                "icon": "🛡️",
                "command": self.dezactiveaza_defender,
                "descriere": "Deschide setările Windows Defender"
            },
            {
                "text": "Dezactivează Windows Update",
                "icon": "🔄",
                "command": self.dezactiveaza_update,
                "descriere": "Deschide setările Windows Update"
            },
            {
                "text": "Curățare Sistem",
                "icon": "🧹",
                "command": self.curatare_sistem,
                "descriere": "Elimină fișierele temporare și cache-ul"
            },
            {
                "text": "Actualizare Adresă IP",
                "icon": "🌐",
                "command": self.actualizare_ip,
                "descriere": "Reînnoiește adresa IP a sistemului"
            },
            {
                "text": "Ștergere Aplicații Nefolosite",
                "icon": "🗑️",
                "command": self.sterge_aplicatii_nefolosite,
                "descriere": "Identifică și elimină aplicațiile neutilizate"
            },
            {
                "text": "Task Manager",
                "icon": "📊",
                "command": self.deschide_task_manager,
                "descriere": "Control procese și aplicații"
            },
            {
                "text": "Eliminare Bloatware",
                "icon": "📦",
                "command": self.eliminare_bloatware,
                "descriere": "Elimină aplicațiile Windows preinstalate"
            },
            {
                "text": "Informații Sistem",
                "icon": "ℹ️",
                "command": self.afiseaza_info_sistem,
                "descriere": "Afișează informații detaliate despre sistem"
            },
            {
                "text": "Monitorizare Trafic",
                "icon": "📈",
                "command": self.monitorizare_trafic,
                "descriere": "Monitorizează traficul de internet"
            },
            {
                "text": "Test Viteză Internet",
                "icon": "📶",
                "command": self.test_viteza_internet,
                "descriere": "Testează viteza internetului"
            },
            {
                "text": "Proxy Browser",
                "icon": "🌐",
                "command": self.deschide_proxy_browser,
                "descriere": "Deschide URL-uri prin proxy"
            }
        ]
        
        # Dimensiuni fixe pentru butoane (câte 4 pe rând)
        BUTON_WIDTH = 190
        BUTON_HEIGHT = 150
        PADDING = 10
        
        # Creăm un tabel stabil cu dimensiuni fixe: 2 rânduri și 4 coloane
        for i, info_buton in enumerate(butoane_info):
            row, col = divmod(i, 4)
            
            # Poziționăm cu coordonate absolute pentru stabilitate
            x = col * (BUTON_WIDTH + PADDING) + PADDING
            y = row * (BUTON_HEIGHT + PADDING) + PADDING
            
            # Frame pentru fiecare buton cu dimensiuni fixe
            btn_frame = tk.Frame(
                self.frame_butoane, 
                bg=self.culoare_tertiara,
                width=BUTON_WIDTH,
                height=BUTON_HEIGHT,
                highlightbackground=self.culoare_accent,
                highlightthickness=1
            )
            btn_frame.place(x=x, y=y)
            btn_frame.pack_propagate(False)  # Păstrează dimensiunea fixă
            
            # Antet buton
            icon_label = tk.Label(
                btn_frame, 
                text=info_buton["icon"], 
                font=("Arial", 18),
                bg=self.culoare_tertiara,
                fg=self.culoare_accent
            )
            icon_label.pack(pady=(15, 0))
            
            # Titlu buton
            title_label = tk.Label(
                btn_frame,
                text=info_buton["text"],
                font=("Arial", 10, "bold"),
                bg=self.culoare_tertiara,
                fg=self.culoare_text,
                wraplength=170,
                justify="center"
            )
            title_label.pack(pady=(5, 0))
            
            # Descriere buton (opțional, elimină pentru un aspect mai compact)
            desc_label = tk.Label(
                btn_frame,
                text=info_buton["descriere"],
                font=("Arial", 8),
                bg=self.culoare_tertiara,
                fg="#aaaaaa",
                wraplength=170,
                justify="center"
            )
            desc_label.pack(pady=(5, 0))
            
            # Buton
            buton = tk.Button(
                btn_frame,
                text="EXECUTĂ",
                command=info_buton["command"],
                font=("Arial", 9, "bold"),
                bg=self.culoare_buton,
                fg=self.culoare_text,
                activebackground=self.culoare_accent,
                activeforeground=self.culoare_text,
                relief=tk.FLAT,
                bd=0,
                width=15,
                height=1
            )
            buton.pack(pady=(8, 10))
            
            # Efect hover
            btn_frame.bind("<Enter>", lambda e, f=btn_frame: self.frame_hover_enter(f))
            btn_frame.bind("<Leave>", lambda e, f=btn_frame: self.frame_hover_leave(f))
            buton.bind("<Enter>", lambda e, b=buton: self.buton_hover_enter(b))
            buton.bind("<Leave>", lambda e, b=buton: self.buton_hover_leave(b))
            
        # Setează dimensiunea frame-ului pentru butoane pentru a se potrivi cu grilă
        self.frame_butoane.configure(width=(BUTON_WIDTH + PADDING) * 4 + PADDING, 
                                    height=(BUTON_HEIGHT + PADDING) * 2 + PADDING)
        self.frame_butoane.pack_propagate(False)  # Păstrează dimensiunea fixă
        
        # Footer cu buton de ieșire
        footer_frame = tk.Frame(self.frame_principal, bg=self.culoare_principala, height=50)
        footer_frame.pack(fill="x", padx=2, pady=2)
        
        buton_iesire = tk.Button(
            footer_frame,
            text="IEȘIRE",
            command=self.quit,
            font=("Arial", 10, "bold"),
            bg=self.culoare_principala,
            fg=self.culoare_accent,
            activebackground=self.culoare_accent,
            activeforeground=self.culoare_text,
            relief=tk.FLAT,
            bd=0,
            width=15
        )
        buton_iesire.pack(side="right", padx=15, pady=10)
        
        # Status bar
        self.status_text = tk.StringVar()
        self.status_text.set("Sistem pregătit")
        
        self.status = tk.Label(
            self,
            textvariable=self.status_text,
            font=("Arial", 10),
            bg=self.culoare_principala,
            fg=self.culoare_accent,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Redimensionare - o singură legătură pentru eveniment
        self.bind("<Configure>", self.on_resize)
    
    def frame_hover_enter(self, frame):
        frame.config(highlightbackground=self.culoare_highlight, highlightthickness=2)
        
    def frame_hover_leave(self, frame):
        frame.config(highlightbackground=self.culoare_accent, highlightthickness=1)
    
    def buton_hover_enter(self, buton):
        buton.config(bg=self.culoare_accent)
        
    def buton_hover_leave(self, buton):
        buton.config(bg=self.culoare_buton)
    
    def actualizare_fundal(self):
        """Încarcă și aplică imaginea de fundal"""
        try:
            if not self.background_path:
                # Crează un fundal alternativ dacă nu avem imaginea
                self.canvas.config(bg=self.culoare_secundara)
                return
                
            width, height = self.winfo_width(), self.winfo_height()
            if width <= 1 or height <= 1:
                width, height = 1000, 700
                
            # Încarcă imaginea o singură dată pentru performanță
            if not hasattr(self, 'imagine_originala'):
                self.imagine_originala = Image.open(self.background_path)
            
            # Redimensionază și aplică efecte
            redimensionat = self.imagine_originala.resize((width, height), Image.LANCZOS)
            enhancer = ImageEnhance.Brightness(redimensionat)
            redimensionat = enhancer.enhance(0.6)  # Mai întunecat pentru aspect de putere
            
            # Adaugă tenta roșie intensă
            enhancer = ImageEnhance.Color(redimensionat)
            redimensionat = enhancer.enhance(1.4)  # Saturație crescută
            
            # Actualizează imaginea pe canvas
            self.imagine_tk = ImageTk.PhotoImage(redimensionat)
            
            # Verifică dacă există deja o imagine pe canvas
            if hasattr(self, 'imagine_canvas_id'):
                self.canvas.itemconfig(self.imagine_canvas_id, image=self.imagine_tk)
            else:
                self.imagine_canvas_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagine_tk)
        except:
            # În caz de eroare, folosim un fundal de rezervă
            self.canvas.config(bg=self.culoare_secundara)
    
    def on_resize(self, event=None):
        """Handler optimizat pentru evenimentul de redimensionare"""
        acum = time.time()
        if not hasattr(self, 'ultima_redimensionare') or acum - self.ultima_redimensionare > 0.3:
            self.ultima_redimensionare = acum
            self.actualizare_fundal()
    
    def dezactiveaza_defender(self):
        self.status_text.set("Deschid setările Windows Defender...")
        try:
            # Încearcă să deschidă setările Windows Defender
            subprocess.Popen(["ms-settings:windowsdefender"])
            self.status_text.set("Setări Windows Defender deschise")
        except:
            try:
                # Metodă alternativă
                subprocess.Popen(["control", "/name", "Microsoft.WindowsDefender"])
                self.status_text.set("Setări Windows Defender deschise")
            except:
                self.status_text.set("Nu s-au putut deschide setările Windows Defender")
    
    def dezactiveaza_update(self):
        self.status_text.set("Deschid panoul de blocare Windows Update...")
        
        # Verifică dacă fereastra este deja deschisă
        if hasattr(self, 'update_window') and self.update_window is not None and self.update_window.winfo_exists():
            self.update_window.lift()  # Aduce fereastra în prim-plan
            return
        
        # Creează o fereastră nouă pentru opțiunile Windows Update
        self.update_window = tk.Toplevel(self)
        self.update_window.title("Blocare Windows Update")
        self.update_window.geometry("800x600")
        self.update_window.minsize(600, 400)
        self.update_window.configure(bg=self.culoare_principala)
        
        # Adaugă un stil pentru treeview (tabel)
        style = ttk.Style()
        style.theme_use("default")
        
        # Configurează stilul tabelului
        style.configure("Treeview", 
                        background=self.culoare_principala,
                        foreground=self.culoare_text,
                        rowheight=50,
                        fieldbackground=self.culoare_principala)
        style.configure("Treeview.Heading", 
                        background=self.culoare_secundara,
                        foreground=self.culoare_accent,
                        font=('Arial', 10, 'bold'))
        
        # Modifică selecția
        style.map('Treeview', 
                  background=[('selected', self.culoare_accent)],
                  foreground=[('selected', self.culoare_text)])
        
        # Creează un frame pentru titlu și informații
        frame_header = tk.Frame(self.update_window, bg=self.culoare_principala)
        frame_header.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Adaugă titlu
        label_title = tk.Label(
            frame_header,
            text="OPȚIUNI BLOCARE WINDOWS UPDATE",
            font=("Arial", 16, "bold"),
            bg=self.culoare_principala,
            fg=self.culoare_accent
        )
        label_title.pack(side=tk.TOP, padx=10, pady=5)
        
        # Adaugă descriere
        label_desc = tk.Label(
            frame_header,
            text="Selectați o metodă de blocare și apăsați 'Aplică' pentru a dezactiva Windows Update",
            font=("Arial", 10),
            bg=self.culoare_principala,
            fg=self.culoare_text
        )
        label_desc.pack(side=tk.TOP, padx=10, pady=5)
        
        # Creează un frame pentru tabel
        frame_table = tk.Frame(self.update_window, bg=self.culoare_principala)
        frame_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Creează scrollbar
        scrollbar = ttk.Scrollbar(frame_table)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Definește coloanele pentru tabel
        self.update_tree = ttk.Treeview(
            frame_table,
            columns=("method", "description", "impact"),
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.update_tree.yview)
        
        # Configurare coloane
        self.update_tree.heading("method", text="Metodă de blocare")
        self.update_tree.heading("description", text="Descriere")
        self.update_tree.heading("impact", text="Impact")
        
        # Setează lățimile coloanelor
        self.update_tree.column("method", width=200, anchor=tk.W)
        self.update_tree.column("description", width=350, anchor=tk.W)
        self.update_tree.column("impact", width=150, anchor=tk.CENTER)
        
        # Adaugă tabelul la frame
        self.update_tree.pack(fill=tk.BOTH, expand=True)
        
        # Adaugă metodele de blocare în tabel
        metode_blocare = [
            {
                "id": "disable_service",
                "method": "Dezactivare serviciu Windows Update",
                "description": "Oprește și dezactivează complet serviciul Windows Update din sistem",
                "impact": "Mare"
            },
            {
                "id": "registry_disable",
                "method": "Blocare prin Registry",
                "description": "Modifică registrul Windows pentru a dezactiva actualizările automate",
                "impact": "Mare"
            },
            {
                "id": "metered_connection",
                "method": "Conexiune cu măsurare",
                "description": "Configurează conexiunea actuală ca fiind cu măsurare pentru a limita descărcările",
                "impact": "Mediu"
            },
            {
                "id": "notify_only",
                "method": "Doar notificări",
                "description": "Configurează Windows să vă notifice înainte de a descărca sau instala actualizări",
                "impact": "Mic"
            },
            {
                "id": "scheduler_disable",
                "method": "Dezactivare programator",
                "description": "Dezactivează taskurile programate pentru Windows Update",
                "impact": "Mediu"
            },
            {
                "id": "defer_updates",
                "method": "Amânare actualizări",
                "description": "Amânare actualizări de funcționalitate și calitate pentru perioada maximă",
                "impact": "Mediu"
            },
            {
                "id": "group_policy",
                "method": "Blocare prin Politici de Grup",
                "description": "Configurează politicile de grup pentru a dezactiva descărcarea automată",
                "impact": "Mare"
            }
        ]
        
        # Adaugă fiecare metodă în tabel
        for metoda in metode_blocare:
            self.update_tree.insert("", tk.END, values=(
                metoda["method"], 
                metoda["description"], 
                metoda["impact"]), 
                tags=(metoda["id"],)
            )
        
        # Adaugă un frame pentru butoane
        frame_buttons = tk.Frame(self.update_window, bg=self.culoare_principala)
        frame_buttons.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Buton pentru aplicare
        apply_button = tk.Button(
            frame_buttons,
            text="Aplică metodă selectată",
            command=self.aplica_blocare_update,
            font=("Arial", 10, "bold"),
            bg=self.culoare_accent,
            fg=self.culoare_text,
            activebackground=self.culoare_highlight,
            relief=tk.FLAT,
            padx=10,
            pady=5,
            width=20
        )
        apply_button.pack(side=tk.RIGHT, padx=10)
        
        # Buton pentru reactivare
        reactivate_button = tk.Button(
            frame_buttons,
            text="Reactivează Windows Update",
            command=self.reactivare_windows_update,
            font=("Arial", 10),
            bg=self.culoare_buton,
            fg=self.culoare_text,
            activebackground=self.culoare_accent,
            relief=tk.FLAT,
            padx=10,
            pady=5,
            width=20
        )
        reactivate_button.pack(side=tk.LEFT, padx=10)
        
        # Status bar
        self.update_status = tk.Label(
            self.update_window,
            text="Selectați o metodă de blocare",
            font=("Arial", 9),
            bg=self.culoare_principala,
            fg=self.culoare_accent,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.update_status.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Adaugă eveniment pentru dublu-click pe o metodă
        self.update_tree.bind("<Double-1>", lambda event: self.aplica_blocare_update())
        
        self.status_text.set("Panou blocare Windows Update deschis")
    
    def aplica_blocare_update(self):
        """Aplică metoda selectată pentru blocarea Windows Update"""
        try:
            # Obține elementul selectat
            selected_item = self.update_tree.selection()[0]
            item_id = self.update_tree.item(selected_item, "tags")[0]
            values = self.update_tree.item(selected_item, "values")
            method_name = values[0]
            
            # Confirmă acțiunea
            confirm = messagebox.askyesno(
                "Confirmare", 
                f"Sigur doriți să aplicați metoda '{method_name}'?\n\nAceasta va dezactiva Windows Update și poate afecta securitatea sistemului."
            )
            
            if not confirm:
                return
            
            # Indică procesarea
            self.update_status.config(text=f"Se aplică metoda: {method_name}...")
            
            # Aplică metoda selectată
            result = False
            message = ""
            
            if item_id == "disable_service":
                result, message = self.dezactiveaza_serviciu_wu()
            elif item_id == "registry_disable":
                result, message = self.dezactiveaza_registry_wu()
            elif item_id == "metered_connection":
                result, message = self.seteaza_conexiune_cu_masurare()
            elif item_id == "notify_only":
                result, message = self.seteaza_doar_notificari()
            elif item_id == "scheduler_disable":
                result, message = self.dezactiveaza_programator_wu()
            elif item_id == "defer_updates":
                result, message = self.amana_actualizari()
            elif item_id == "group_policy":
                result, message = self.configureaza_group_policy()
            
            # Actualizează status
            if result:
                self.update_status.config(text=f"Metodă aplicată cu succes: {method_name}")
                messagebox.showinfo("Succes", message)
            else:
                self.update_status.config(text=f"Eroare la aplicarea metodei: {method_name}")
                messagebox.showerror("Eroare", message)
                
        except IndexError:
            messagebox.showwarning("Avertisment", "Selectați o metodă pentru a o aplica.")
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la aplicarea metodei: {str(e)}")
            self.update_status.config(text=f"Eroare: {str(e)}")
    
    def dezactiveaza_serviciu_wu(self):
        """Dezactivează serviciul Windows Update"""
        try:
            # Oprește serviciul
            subprocess.run(["sc", "stop", "wuauserv"], shell=True, check=True)
            subprocess.run(["sc", "config", "wuauserv", "start=disabled"], shell=True, check=True)
            
            # Oprește și alte servicii conexe
            subprocess.run(["sc", "stop", "UsoSvc"], shell=True, check=False)
            subprocess.run(["sc", "config", "UsoSvc", "start=disabled"], shell=True, check=False)
            
            subprocess.run(["sc", "stop", "WaaSMedicSvc"], shell=True, check=False)
            subprocess.run(["sc", "config", "WaaSMedicSvc", "start=disabled"], shell=True, check=False)
            
            subprocess.run(["sc", "stop", "BITS"], shell=True, check=False)
            subprocess.run(["sc", "config", "BITS", "start=disabled"], shell=True, check=False)
            
            return True, "Serviciul Windows Update a fost oprit și dezactivat cu succes."
        except Exception as e:
            return False, f"Nu s-a putut dezactiva serviciul Windows Update: {str(e)}"
    
    def dezactiveaza_registry_wu(self):
        """Dezactivează Windows Update prin modificări în registry"""
        try:
            # Calea către cheile de registry pentru Windows Update
            wu_key_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate"
            au_key_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
            
            # Deschide sau creează cheile în registry
            try:
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, wu_key_path)
                wu_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, wu_key_path, 0, winreg.KEY_WRITE)
                
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, au_key_path)
                au_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, au_key_path, 0, winreg.KEY_WRITE)
                
                # Dezactivează actualizările automate (0 = Dezactivat)
                winreg.SetValueEx(au_key, "NoAutoUpdate", 0, winreg.REG_DWORD, 1)
                
                # Dezactivează interfața GUI Windows Update
                winreg.SetValueEx(au_key, "EnableFeaturedSoftware", 0, winreg.REG_DWORD, 0)
                
                # Dezactivează descărcarea automată
                winreg.SetValueEx(au_key, "AUOptions", 0, winreg.REG_DWORD, 1)
                
                # Închide cheile
                winreg.CloseKey(au_key)
                winreg.CloseKey(wu_key)
                
                # Alternativ, foloseste REG ADD din linia de comandă pentru a fi sigur
                try:
                    subprocess.run([
                        "reg", "add", 
                        r"HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU", 
                        "/v", "NoAutoUpdate", "/t", "REG_DWORD", "/d", "1", "/f"
                    ], shell=True, check=True)
                except:
                    pass
                
                return True, "Windows Update a fost dezactivat cu succes prin modificări în registry."
            except PermissionError:
                # Încearcă varianta cu PowerShell elevat
                temp_dir = tempfile.gettempdir()
                ps_script_path = os.path.join(temp_dir, "disable_wu_registry.ps1")
                
                with open(ps_script_path, "w") as f:
                    f.write(r'''
                    New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate" -Force
                    New-Item -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Force
                    Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "NoAutoUpdate" -Value 1 -Type DWord
                    Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "AUOptions" -Value 1 -Type DWord
                    ''')
                
                # Execută scriptul PowerShell
                result = subprocess.run([
                    "powershell", "-ExecutionPolicy", "Bypass", "-File", ps_script_path
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    return False, f"Nu s-au putut aplica modificările în registry. Eroare: {result.stderr}"
                
                return True, "Windows Update a fost dezactivat cu succes prin modificări în registry (PowerShell)."
        except Exception as e:
            return False, f"Nu s-au putut aplica modificările în registry: {str(e)}"
    
    def seteaza_conexiune_cu_masurare(self):
        """Setează conexiunea actuală ca fiind cu măsurare pentru a limita descărcările"""
        try:
            # Metoda PowerShell pentru a seta conexiunea ca fiind cu măsurare
            temp_dir = tempfile.gettempdir()
            ps_script_path = os.path.join(temp_dir, "set_metered_connection.ps1")
            
            with open(ps_script_path, "w") as f:
                f.write(r'''
                # Setează conexiunea ca fiind cu măsurare
                $connectionProfile = [Windows.Networking.Connectivity.NetworkInformation,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::GetInternetConnectionProfile()
                $telemerySettings = [Windows.Networking.Connectivity.NetworkUsageStates,Windows.Networking.Connectivity,ContentType=WindowsRuntime]::CreateFromStates([Windows.Networking.Connectivity.TriStates]::DoNotCare, [Windows.Networking.Connectivity.TriStates]::True)
                $connectionProfile.SetConnectionProfileMeteredOverride([Windows.Networking.Connectivity.MeteredConnectionCost]::Fixed)
                
                # Verifică succes
                if (Get-NetConnectionProfile) {
                    Write-Host "Conexiune setată ca fiind cu măsurare."
                    exit 0
                } else {
                    Write-Host "Nu s-a putut seta conexiunea ca fiind cu măsurare."
                    exit 1
                }
                ''')
            
            # Deschide setările pentru conexiunea cu măsurare
            subprocess.Popen(["ms-settings:network-ethernet"])
            
            message = (
                "Pentru a activa conexiunea cu măsurare:\n\n"
                "1. În fereastra deschisă, selectați conexiunea de rețea activă\n"
                "2. Comutați opțiunea 'Setați ca rețea cu măsurare' la 'Activat'\n\n"
                "Acest lucru va împiedica Windows Update să descarce automat actualizările."
            )
            
            return True, message
        except Exception as e:
            return False, f"Nu s-a putut seta conexiunea ca fiind cu măsurare: {str(e)}"
    
    def seteaza_doar_notificari(self):
        """Configurează Windows să notifice înainte de a descărca sau instala actualizări"""
        try:
            # Deschide sau creează cheile în registry
            au_key_path = r"SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU"
            
            try:
                winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, au_key_path)
                au_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, au_key_path, 0, winreg.KEY_WRITE)
                
                # Setează AUOptions la 2 (Notifică înainte de descărcare)
                winreg.SetValueEx(au_key, "AUOptions", 0, winreg.REG_DWORD, 2)
                
                # Închide cheia
                winreg.CloseKey(au_key)
                
                # Folosește și metoda cu linie de comandă pentru siguranță
                subprocess.run([
                    "reg", "add", 
                    r"HKLM\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU", 
                    "/v", "AUOptions", "/t", "REG_DWORD", "/d", "2", "/f"
                ], shell=True, check=False)
                
                return True, "Windows Update a fost configurat să notifice înainte de a descărca actualizări."
            except PermissionError:
                # Deschide setările Windows Update
                subprocess.Popen(["ms-settings:windowsupdate"])
                
                # Afișează instrucțiuni pentru utilizator
                message = (
                    "Pentru a configura notificările pentru actualizări:\n\n"
                    "1. În fereastra deschisă, accesați 'Opțiuni avansate'\n"
                    "2. Selectați 'Notifică pentru a descărca și notifică pentru a instala' din lista derulantă\n\n"
                    "Windows va notifica acum înainte de a descărca sau instala actualizări."
                )
                
                return True, message
        except Exception as e:
            return False, f"Nu s-a putut seta notificarea pentru actualizări: {str(e)}"
    
    def dezactiveaza_programator_wu(self):
        """Dezactivează taskurile programate pentru Windows Update"""
        try:
            # Dezactivează toate taskurile programate pentru Windows Update
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\WindowsUpdate\Automatic App Update", "/Disable"
            ], shell=True, check=False)
            
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\WindowsUpdate\Scheduled Start", "/Disable"
            ], shell=True, check=False)
            
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\UpdateOrchestrator\Refresh Settings", "/Disable"
            ], shell=True, check=False)
            
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\UpdateOrchestrator\Schedule Scan", "/Disable"
            ], shell=True, check=False)
            
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\UpdateOrchestrator\USO_UxBroker", "/Disable"
            ], shell=True, check=False)
            
            return True, "Taskurile programate pentru Windows Update au fost dezactivate cu succes."
        except Exception as e:
            return False, f"Nu s-au putut dezactiva taskurile programate: {str(e)}"
    
    def amana_actualizari(self):
        """Configurează amânarea actualizărilor pentru perioada maximă permisă"""
        try:
            # Deschide setările Windows Update
            subprocess.Popen(["ms-settings:windowsupdate-options"])
            
            # Creează o fereastră cu instrucțiuni
            instruction_window = tk.Toplevel(self)
            instruction_window.title("Instrucțiuni amânare actualizări")
            instruction_window.geometry("500x400")
            instruction_window.configure(bg=self.culoare_principala)
            
            # Adaugă text cu instrucțiuni
            instructions = tk.Label(
                instruction_window,
                text="Pentru a amâna actualizările Windows, urmați acești pași:",
                font=("Arial", 12, "bold"),
                bg=self.culoare_principala,
                fg=self.culoare_accent,
                wraplength=450,
                justify="left"
            )
            instructions.pack(padx=20, pady=20)
            
            steps = tk.Label(
                instruction_window,
                text=(
                    "1. În fereastra deschisă, accesați 'Opțiuni avansate'\n\n"
                    "2. Activați opțiunea 'Amânare actualizări de calitate' și setați la 35 de zile\n\n"
                    "3. Activați opțiunea 'Amânare actualizări de caracteristici' și setați la 365 de zile\n\n"
                    "4. În secțiunea 'Pauză actualizări', setați actualizările la pauză pentru perioada maximă"
                ),
                font=("Arial", 10),
                bg=self.culoare_principala,
                fg=self.culoare_text,
                wraplength=450,
                justify="left"
            )
            steps.pack(padx=20)
            
            # Buton pentru închidere
            close_button = tk.Button(
                instruction_window,
                text="Am înțeles",
                command=instruction_window.destroy,
                bg=self.culoare_accent,
                fg=self.culoare_text,
                font=("Arial", 10),
                relief=tk.FLAT
            )
            close_button.pack(pady=20)
            
            return True, "Setările pentru amânarea actualizărilor au fost deschise. Urmați instrucțiunile afișate."
        except Exception as e:
            return False, f"Nu s-au putut configura setările pentru amânarea actualizărilor: {str(e)}"

    def configureaza_group_policy(self):
        """Configurează politicile de grup pentru a dezactiva Windows Update"""
        try:
            # Verifică dacă gpedit.msc este disponibil (doar pe Windows Pro/Enterprise)
            has_gpedit = True
            try:
                subprocess.run(["gpedit.msc"], shell=True, check=True)
            except:
                has_gpedit = False
            
            if has_gpedit:
                # Dacă gpedit există, deschide-l și oferă instrucțiuni
                subprocess.Popen(["gpedit.msc"])
                
                # Creează o fereastră cu instrucțiuni
                instruction_window = tk.Toplevel(self)
                instruction_window.title("Instrucțiuni Group Policy")
                instruction_window.geometry("600x450")
                instruction_window.configure(bg=self.culoare_principala)
                
                # Adaugă text cu instrucțiuni
                instructions = tk.Label(
                    instruction_window,
                    text="Pentru a dezactiva Windows Update prin Group Policy Editor, urmați acești pași:",
                    font=("Arial", 12, "bold"),
                    bg=self.culoare_principala,
                    fg=self.culoare_accent,
                    wraplength=550,
                    justify="left"
                )
                instructions.pack(padx=20, pady=20)
                
                steps = tk.Label(
                    instruction_window,
                    text=(
                        "1. Navigați la: Computer Configuration > Administrative Templates > Windows Components > Windows Update\n\n"
                        "2. Faceți dublu clic pe 'Configure Automatic Updates'\n\n"
                        "3. Selectați 'Dezactivat' și apoi apăsați OK\n\n"
                        "4. De asemenea, puteți deschide 'Remove access to use all Windows Update features' și setați-l la 'Activat'\n\n"
                        "5. Apoi executați 'gpupdate /force' în Command Prompt pentru a aplica schimbările"
                    ),
                    font=("Arial", 10),
                    bg=self.culoare_principala,
                    fg=self.culoare_text,
                    wraplength=550,
                    justify="left"
                )
                steps.pack(padx=20)
                
                # Buton pentru închidere
                close_button = tk.Button(
                    instruction_window,
                    text="Am înțeles",
                    command=instruction_window.destroy,
                    bg=self.culoare_accent,
                    fg=self.culoare_text,
                    font=("Arial", 10),
                    relief=tk.FLAT
                )
                close_button.pack(pady=20)
                
                return True, "Group Policy Editor a fost deschis. Urmați instrucțiunile afișate."
            else:
                # Dacă gpedit nu există, folosește registry pentru a simula aceleași setări
                reg_script = os.path.join(tempfile.gettempdir(), "disable_wu_gpo.reg")
                
                with open(reg_script, "w") as f:
                    f.write('''Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate]
"DisableWindowsUpdateAccess"=dword:00000001

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU]
"NoAutoUpdate"=dword:00000001
''')
                
                # Importă setările de registry
                subprocess.run(["regedit", "/s", reg_script], shell=True)
                
                return True, "Windows Update a fost dezactivat prin modificări de registry care simulează politicile de grup."
        except Exception as e:
            return False, f"Nu s-au putut configura politicile de grup: {str(e)}"

    def reactivare_windows_update(self):
        """Reactivează serviciile Windows Update"""
        try:
            # Afișează un mesaj de confirmare
            confirm = messagebox.askyesno(
                "Confirmare", 
                "Sigur doriți să reactivați Windows Update?\n\nAceasta va reactiva toate serviciile și setările pentru actualizări."
            )
            
            if not confirm:
                return
            
            self.update_status.config(text="Se reactivează Windows Update...")
            
            # 1. Reactivează serviciile Windows Update
            subprocess.run(["sc", "config", "wuauserv", "start=auto"], shell=True)
            subprocess.run(["sc", "start", "wuauserv"], shell=True)
            
            # Reactivează și alte servicii conexe
            subprocess.run(["sc", "config", "UsoSvc", "start=auto"], shell=True)
            subprocess.run(["sc", "start", "UsoSvc"], shell=True)
            
            subprocess.run(["sc", "config", "WaaSMedicSvc", "start=auto"], shell=True)
            subprocess.run(["sc", "start", "WaaSMedicSvc"], shell=True)
            
            subprocess.run(["sc", "config", "BITS", "start=auto"], shell=True)
            subprocess.run(["sc", "start", "BITS"], shell=True)
            
            # 2. Curăță setările de registry
            registry_script = os.path.join(tempfile.gettempdir(), "enable_wu.reg")
            
            with open(registry_script, "w") as f:
                f.write('''Windows Registry Editor Version 5.00

[-HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate]
''')
            
            # Importă setările de registry pentru a șterge cheile de blocare
            subprocess.run(["regedit", "/s", registry_script], shell=True)
            
            # 3. Reactivează taskurile programate
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\WindowsUpdate\Automatic App Update", "/Enable"
            ], shell=True)
            
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\WindowsUpdate\Scheduled Start", "/Enable"
            ], shell=True)
            
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\UpdateOrchestrator\Refresh Settings", "/Enable"
            ], shell=True)
            
            subprocess.run([
                "schtasks", "/Change", "/TN", r"Microsoft\Windows\UpdateOrchestrator\Schedule Scan", "/Enable"
            ], shell=True)
            
            # 4. Actualizează fereastra UI
            self.update_status.config(text="Windows Update a fost reactivat cu succes")
            messagebox.showinfo("Succes", "Windows Update a fost reactivat. Sistemul va primi din nou actualizări automate.")
            
        except Exception as e:
            self.update_status.config(text=f"Eroare la reactivarea Windows Update: {str(e)}")
            messagebox.showerror("Eroare", f"Nu s-a putut reactiva Windows Update: {str(e)}")
    
    def _obtine_aplicatii(self):
        """Obține lista de aplicații instalate în sistem"""
        aplicatii = []
        
        # Lista pentru a stoca toate aplicațiile găsite
        toate_aplicatiile = []
        
        try:
            # 1. Obține aplicațiile instalate din Registry (aplicații desktop standard)
            try:
                import winreg
                
                # Cheia pentru aplicațiile instalate
                uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
                
                # Deschide cheia
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key)
                
                # Iterează prin subchei
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        
                        try:
                            nume = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            
                            # Ignoră aplicațiile fără nume de afișare
                            if nume and len(nume.strip()) > 0:
                                app_info = {
                                    "name": nume,
                                    "type": "Desktop",
                                    "uninstall_string": "",
                                    "publisher": "",
                                    "version": "",
                                    "install_date": "",
                                    "size": "",
                                    "key_path": f"HKLM\\{uninstall_key}\\{subkey_name}"
                                }
                                
                                # Obține detalii suplimentare (opțional)
                                try:
                                    app_info["publisher"] = winreg.QueryValueEx(subkey, "Publisher")[0]
                                except:
                                    pass
                                    
                                try:
                                    app_info["version"] = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                except:
                                    pass
                                    
                                try:
                                    app_info["install_date"] = winreg.QueryValueEx(subkey, "InstallDate")[0]
                                except:
                                    pass
                                    
                                try:
                                    size_kb = winreg.QueryValueEx(subkey, "EstimatedSize")[0] / 1024
                                    app_info["size"] = f"{size_kb:.1f} MB"
                                except:
                                    pass
                                    
                                try:
                                    app_info["uninstall_string"] = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                except:
                                    pass
                                
                                toate_aplicatiile.append(app_info)
                        except:
                            pass
                            
                        winreg.CloseKey(subkey)
                        i += 1
                    except WindowsError:
                        break
                        
                winreg.CloseKey(key)
                
                # Verifică și în HKEY_CURRENT_USER
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, uninstall_key)
                
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        
                        try:
                            nume = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            
                            if nume and len(nume.strip()) > 0:
                                app_info = {
                                    "name": nume,
                                    "type": "Desktop",
                                    "uninstall_string": "",
                                    "publisher": "",
                                    "version": "",
                                    "install_date": "",
                                    "size": "",
                                    "key_path": f"HKCU\\{uninstall_key}\\{subkey_name}"
                                }
                                
                                try:
                                    app_info["publisher"] = winreg.QueryValueEx(subkey, "Publisher")[0]
                                except:
                                    pass
                                    
                                try:
                                    app_info["version"] = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                except:
                                    pass
                                    
                                try:
                                    app_info["install_date"] = winreg.QueryValueEx(subkey, "InstallDate")[0]
                                except:
                                    pass
                                    
                                try:
                                    size_kb = winreg.QueryValueEx(subkey, "EstimatedSize")[0] / 1024
                                    app_info["size"] = f"{size_kb:.1f} MB"
                                except:
                                    pass
                                    
                                try:
                                    app_info["uninstall_string"] = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                except:
                                    pass
                                
                                toate_aplicatiile.append(app_info)
                        except:
                            pass
                            
                        winreg.CloseKey(subkey)
                        i += 1
                    except WindowsError:
                        break
                        
                winreg.CloseKey(key)
            except Exception as e:
                print(f"Eroare la obținerea aplicațiilor din registry: {str(e)}")
            
            # 2. Obține aplicațiile universale Windows (AppX/Microsoft Store)
            try:
                # Folosim PowerShell pentru a obține lista aplicațiilor AppX
                import subprocess
                
                # Comanda PowerShell pentru a obține aplicațiile instalate
                ps_command = "Get-AppxPackage | Select-Object Name, PackageFullName, Publisher, Version, InstallLocation | ConvertTo-Csv -NoTypeInformation"
                
                # Execută comanda
                result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout:
                    # Parsează rezultatul (format CSV)
                    import csv
                    from io import StringIO
                    
                    reader = csv.DictReader(StringIO(result.stdout))
                    
                    for row in reader:
                        app_info = {
                            "name": row.get("Name", "").replace("Microsoft.", ""),  # Simplifică numele
                            "type": "Windows App",
                            "uninstall_string": f"Remove-AppxPackage {row.get('PackageFullName', '')}",
                            "publisher": row.get("Publisher", ""),
                            "version": row.get("Version", ""),
                            "install_date": "",
                            "size": "",
                            "appx_name": row.get("PackageFullName", "")
                        }
                        
                        # Calculează dimensiunea dosarului (opțional)
                        try:
                            install_location = row.get("InstallLocation", "")
                            if install_location and os.path.exists(install_location):
                                total_size = 0
                                for dirpath, dirnames, filenames in os.walk(install_location):
                                    for f in filenames:
                                        try:
                                            fp = os.path.join(dirpath, f)
                                            total_size += os.path.getsize(fp)
                                        except:
                                            pass
                                
                                app_info["size"] = f"{total_size / (1024 * 1024):.1f} MB"
                        except:
                            pass
                        
                        toate_aplicatiile.append(app_info)
            except Exception as e:
                print(f"Eroare la obținerea aplicațiilor Windows: {str(e)}")
            
            # Sortează toate aplicațiile alfabetic
            toate_aplicatiile.sort(key=lambda x: x["name"].lower())
            
            # Actualizează interfața în thread-ul principal
            self.bloatware_window.after(0, lambda: self._actualizeaza_tabel_aplicatii(toate_aplicatiile))
            
        except Exception as e:
            self.bloatware_window.after(0, lambda: self.bloatware_status.config(
                text=f"Eroare la obținerea aplicațiilor: {str(e)}"
            ))
    
    def _actualizeaza_tabel_aplicatii(self, aplicatii):
        """Actualizeaza tabelul cu aplicații"""
        # Salvează lista completă pentru filtrare ulterioară
        self.toate_aplicatiile = aplicatii
        
        # Filtrarea la afișarea inițială se face prin funcția de filtrare
        self.filtrare_aplicatii()
        
        # Actualizează statusul
        self.bloatware_status.config(text=f"Total aplicații: {len(aplicatii)}")
    
    def filtrare_aplicatii(self, search_var=None):
        """Filtrează aplicațiile conform criteriilor selectate"""
        # Obține textul de căutare
        search_text = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        
        # Obține tipul de aplicație pentru filtrare
        show_type = self.show_type.get() if hasattr(self, 'show_type') else "all"
        
        # Șterge toate elementele existente
        for item in self.apps_tree.get_children():
            self.apps_tree.delete(item)
        
        # Verifică dacă avem lista de aplicații
        if not hasattr(self, 'toate_aplicatiile'):
            return
        
        # Filtrează aplicațiile
        aplicatii_filtrate = []
        for app in self.toate_aplicatiile:
            # Verifică tipul
            if show_type == "win_apps" and app["type"] != "Windows App":
                continue
            elif show_type == "desktop" and app["type"] != "Desktop":
                continue
            
            # Verifică textul de căutare
            if search_text:
                name_match = search_text in app["name"].lower()
                publisher_match = search_text in app.get("publisher", "").lower()
                
                if not (name_match or publisher_match):
                    continue
            
            aplicatii_filtrate.append(app)
        
        # Adaugă aplicațiile filtrate în tabel
        for app in aplicatii_filtrate:
            self.apps_tree.insert("", tk.END, values=(
                app["name"],
                app.get("publisher", ""),
                app.get("version", ""),
                app.get("install_date", ""),
                app.get("size", ""),
                app["type"]
            ), tags=(app["type"],))
        
        # Actualizează statusul
        self.bloatware_status.config(text=f"Aplicații afișate: {len(aplicatii_filtrate)} din {len(self.toate_aplicatiile)}")
    
    def dezinstaleaza_aplicatie(self, quiet=False):
        """Dezinstalează aplicația selectată"""
        try:
            # Verifică dacă este selectată o aplicație
            selection = self.apps_tree.selection()
            if not selection:
                messagebox.showwarning("Avertisment", "Selectați o aplicație pentru a o dezinstala.")
                return
            
            # Obține detaliile aplicației selectate
            selected_item = selection[0]
            values = self.apps_tree.item(selected_item, "values")
            
            app_name = values[0]
            app_type = values[5]
            
            # Confirmă dezinstalarea
            if not quiet:
                confirm = messagebox.askyesno(
                    "Confirmare", 
                    f"Sigur doriți să dezinstalați aplicația '{app_name}'?\n\n"
                    "Acest proces nu poate fi anulat."
                )
                
                if not confirm:
                    return
            
            # Actualizează statusul
            self.bloatware_status.config(text=f"Se dezinstalează {app_name}...")
            
            # Găsește aplicația completă în lista de aplicații
            app_info = None
            for app in self.toate_aplicatiile:
                if app["name"] == app_name and app["type"] == app_type:
                    app_info = app
                    break
                
            if not app_info:
                messagebox.showerror("Eroare", "Nu s-au putut găsi informațiile aplicației.")
                self.bloatware_status.config(text="Eroare: Nu s-au putut găsi informațiile aplicației.")
                return
            
            # Dezinstalează aplicația în funcție de tip
            if app_type == "Windows App":
                # Pentru aplicațiile Windows (AppX)
                appx_name = app_info.get("appx_name", "")
                
                if appx_name:
                    # Folosim PowerShell pentru dezinstalare
                    ps_command = f"Remove-AppxPackage -Package '{appx_name}'"
                    
                    # Execută comanda
                    self.bloatware_window.after(0, lambda: threading.Thread(
                        target=self._run_uninstall_command,
                        args=(ps_command, app_name, "powershell"),
                        daemon=True
                    ).start())
                else:
                    messagebox.showerror("Eroare", "Nu s-a putut găsi numele pachetului pentru dezinstalare.")
                    self.bloatware_status.config(text="Eroare: Lipsă informații de dezinstalare.")
            
            else:  # Desktop apps
                uninstall_string = app_info.get("uninstall_string", "")
                
                if uninstall_string:
                    # Pentru aplicațiile cu string de dezinstalare
                    if uninstall_string.startswith("MsiExec"):
                        # Pentru aplicații MSI, adăugăm /quiet pentru dezinstalare silențioasă
                        if quiet:
                            uninstall_string = f"{uninstall_string} /quiet"
                    
                    # Execută comanda
                    self.bloatware_window.after(0, lambda: threading.Thread(
                        target=self._run_uninstall_command,
                        args=(uninstall_string, app_name, "cmd"),
                        daemon=True
                    ).start())
                else:
                    # Deschide panoul Control pentru dezinstalare manuală
                    subprocess.Popen(["appwiz.cpl"])
                    messagebox.showinfo(
                        "Dezinstalare manuală", 
                        f"Nu s-a găsit metoda de dezinstalare automată pentru '{app_name}'.\n\n"
                        "Folosiți Panoul de Control pentru a dezinstala aplicația manual."
                    )
                    self.bloatware_status.config(text="Panou Control deschis pentru dezinstalare manuală.")
        
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la dezinstalarea aplicației: {str(e)}")
            self.bloatware_status.config(text=f"Eroare: {str(e)}")
    
    def _run_uninstall_command(self, command, app_name, command_type="cmd"):
        """Execută comanda de dezinstalare într-un thread separat"""
        try:
            if command_type == "powershell":
                result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Verifică rezultatul
            if result.returncode == 0:
                # Actualizează statusul
                self.bloatware_window.after(0, lambda: self.bloatware_status.config(
                    text=f"Aplicația '{app_name}' a fost dezinstalată cu succes."
                ))
                
                # Reîmprospătează lista după dezinstalare
                self.bloatware_window.after(2000, self.listeaza_aplicatii)
            else:
                error_msg = result.stderr or "Cod de eroare: " + str(result.returncode)
                
                # Deschide dezinstalarea manuală dacă automatică eșuează
                subprocess.Popen(["appwiz.cpl"])
                
                self.bloatware_window.after(0, lambda: messagebox.showinfo(
                    "Dezinstalare manuală", 
                    f"Dezinstalarea automată pentru '{app_name}' a eșuat.\n\n"
                    "Folosiți Panoul de Control deschis pentru a dezinstala aplicația manual."
                ))
                
                self.bloatware_window.after(0, lambda: self.bloatware_status.config(
                    text=f"Dezinstalare automată eșuată, folosiți Panoul de Control."
                ))
        
        except Exception as e:
            self.bloatware_window.after(0, lambda: self.bloatware_status.config(
                text=f"Eroare la execuție comandă: {str(e)}"
            ))
            
            # Deschide dezinstalarea manuală ca alternativă
            subprocess.Popen(["appwiz.cpl"])
    
    def afiseaza_info_sistem(self):
        self.status_text.set("Deschid informații sistem...")
        try:
            # Deschide informații sistem Windows
            subprocess.Popen(["msinfo32.exe"])
            self.status_text.set("Informații sistem deschise")
        except:
            self.status_text.set("Nu s-au putut deschide informațiile de sistem")
    
    def curatare_sistem(self):
        self.status_text.set("Inițiez curățarea sistemului...")
        try:
            # Lansează disk cleanup
            subprocess.Popen(["cleanmgr.exe"])
            
            # Curăță fișierele temporare
            temp_folder = os.environ.get('TEMP', '')
            
            def clean_temp():
                try:
                    files_removed = 0
                    if temp_folder and os.path.exists(temp_folder):
                        for item in os.listdir(temp_folder):
                            item_path = os.path.join(temp_folder, item)
                            try:
                                if os.path.isfile(item_path):
                                    os.unlink(item_path)
                                    files_removed += 1
                                elif os.path.isdir(item_path):
                                    shutil.rmtree(item_path, ignore_errors=True)
                                    files_removed += 1
                            except:
                                pass
                    
                    self.after(0, lambda: self.status_text.set(f"Curățare finalizată. {files_removed} fișiere eliminate"))
                except:
                    self.after(0, lambda: self.status_text.set("Disk Cleanup pornit"))
            
            threading.Thread(target=clean_temp, daemon=True).start()
            
        except:
            self.status_text.set("S-a încercat pornirea Disk Cleanup")
            
    def actualizare_ip(self):
        self.status_text.set("Deschid setările de rețea...")
        try:
            # Metodă care deschide setările de rețea
            subprocess.Popen(["ms-settings:network-status"])
            self.status_text.set("Setări de rețea deschise")
        except:
            try:
                # Metodă alternativă
                subprocess.Popen(["control", "ncpa.cpl"])
                self.status_text.set("Setări de rețea deschise")
            except:
                self.status_text.set("Nu s-au putut deschide setările de rețea")
    
    def sterge_aplicatii_nefolosite(self):
        self.status_text.set("Deschid panoul de dezinstalare aplicații...")
        try:
            # Deschide panoul de control pentru dezinstalarea programelor
            subprocess.Popen(["appwiz.cpl"])
            self.status_text.set("Panou Control Programe deschis")
        except:
            self.status_text.set("Nu s-a putut deschide panoul de control")
    
    def deschide_task_manager(self):
        self.status_text.set("Deschid Task Manager...")
        
        # Creează fereastra pentru task manager
        task_window = tk.Toplevel(self)
        task_window.title("Task Manager")
        task_window.geometry("900x600")
        task_window.configure(bg=self.culoare_principala)
        
        # Adaugă un header
        header_frame = tk.Frame(task_window, bg=self.culoare_principala)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="MANAGER DE PROCESE",
            font=("Arial", 16, "bold"),
            bg=self.culoare_principala,
            fg=self.culoare_accent
        )
        title_label.pack(side=tk.LEFT)
        
        # Creează un frame pentru tabel
        table_frame = tk.Frame(task_window, bg=self.culoare_principala)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Adaugă tabel pentru procese
        columns = ("pid", "nume", "memorie", "cpu", "status")
        
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        
        # Configurează coloanele
        tree.heading("pid", text="PID")
        tree.heading("nume", text="Proces")
        tree.heading("memorie", text="Memorie (MB)")
        tree.heading("cpu", text="CPU (%)")
        tree.heading("status", text="Status")
        
        # Setează lățimile coloanelor
        tree.column("pid", width=80)
        tree.column("nume", width=200)
        tree.column("memorie", width=120)
        tree.column("cpu", width=100)
        tree.column("status", width=100)
        
        # Adaugă scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        # Buton pentru terminarea procesului selectat
        def termina_proces():
            selected_item = tree.selection()
            if selected_item:
                item = tree.item(selected_item[0])
                pid = int(item['values'][0])
                nume_proces = item['values'][1]
                
                try:
                    # Confirmă închiderea procesului
                    if messagebox.askyesno("Confirmare", f"Doriți să închideți procesul {nume_proces} (PID: {pid})?"):
                        process = psutil.Process(pid)
                        process.terminate()
                        messagebox.showinfo("Succes", f"Procesul {nume_proces} (PID: {pid}) a fost terminat")
                        actualizeaza_procese()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
                    messagebox.showerror("Eroare", f"Nu s-a putut termina procesul: {str(e)}")
        
        # Adaugă buton pentru terminarea procesului
        btn_termina = tk.Button(
            header_frame,
            text="Termină proces",
            command=termina_proces,
            bg=self.culoare_accent,
            fg=self.culoare_text,
            font=("Arial", 10),
            relief=tk.FLAT
        )
        btn_termina.pack(side=tk.RIGHT, padx=10)
        
        # Buton de actualizare manuală
        def actualizeaza_procese():
            for item in tree.get_children():
                tree.delete(item)
            
            try:
                for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent', 'status']):
                    try:
                        process_info = proc.info
                        pid = process_info['pid']
                        nume = process_info['name']
                        memorie = process_info['memory_info'].rss / 1024 / 1024  # Convertit la MB
                        cpu = process_info['cpu_percent']
                        status = process_info['status']
                        
                        tree.insert("", "end", values=(
                            pid,
                            nume,
                            f"{memorie:.2f}",
                            f"{cpu:.1f}",
                            status
                        ))
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                    except Exception as e:
                        continue
            except Exception as e:
                messagebox.showerror("Eroare", f"Nu s-au putut obține procesele: {str(e)}")
            
            # Actualizează periodic
            task_window.after(5000, actualizeaza_procese)
        
        btn_refresh = tk.Button(
            header_frame,
            text="Actualizare",
            command=actualizeaza_procese,
            bg=self.culoare_buton,
            fg=self.culoare_text,
            font=("Arial", 10),
            relief=tk.FLAT
        )
        btn_refresh.pack(side=tk.RIGHT, padx=10)
        
        # Prima actualizare
        actualizeaza_procese()
        self.status_text.set("Manager de procese deschis")
            
    def eliminare_bloatware(self):
        self.status_text.set("Deschid panoul de dezinstalare aplicații...")
        try:
            # Deschide panoul de control pentru dezinstalarea programelor
            subprocess.Popen(["appwiz.cpl"])
            self.status_text.set("Panou Control Programe deschis")
        except:
            self.status_text.set("Nu s-a putut deschide panoul de control")
    
    def monitorizare_trafic(self):
        self.status_text.set("Deschid monitorul de trafic...")
        
        # Creează fereastra pentru monitorizarea traficului
        monitor_window = tk.Toplevel(self)
        monitor_window.title("Monitor Trafic Internet")
        monitor_window.geometry("900x600")
        monitor_window.configure(bg=self.culoare_principala)
        
        # Adaugă un header
        header_frame = tk.Frame(monitor_window, bg=self.culoare_principala)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="MONITOR TRAFIC INTERNET",
            font=("Arial", 16, "bold"),
            bg=self.culoare_principala,
            fg=self.culoare_accent
        )
        title_label.pack(side=tk.LEFT)
        
        # Creează un frame pentru tabel
        table_frame = tk.Frame(monitor_window, bg=self.culoare_principala)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Adaugă tabel pentru conexiuni
        columns = ("proces", "local_ip", "local_port", "remote_ip", "remote_port", "status", "trafic")
        
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )
        
        # Configurează coloanele
        tree.heading("proces", text="Aplicație")
        tree.heading("local_ip", text="IP Local")
        tree.heading("local_port", text="Port Local")
        tree.heading("remote_ip", text="IP Distant")
        tree.heading("remote_port", text="Port Distant")
        tree.heading("status", text="Status")
        tree.heading("trafic", text="Trafic")
        
        # Setează lățimile coloanelor
        tree.column("proces", width=150)
        tree.column("local_ip", width=120)
        tree.column("local_port", width=80)
        tree.column("remote_ip", width=120)
        tree.column("remote_port", width=80)
        tree.column("status", width=100)
        tree.column("trafic", width=100)
        
        # Adaugă scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        # Funcție pentru actualizarea conexiunilor
        def actualizeaza_conexiuni():
            for item in tree.get_children():
                tree.delete(item)
            
            try:
                connections = psutil.net_connections(kind='inet')
                for conn in connections:
                    try:
                        pid = conn.pid
                        if pid is None:
                            continue
                        
                        proc = psutil.Process(pid)
                        proc_name = proc.name()
                        
                        laddr = f"{conn.laddr.ip}" if conn.laddr else "N/A"
                        lport = f"{conn.laddr.port}" if conn.laddr else "N/A"
                        raddr = f"{conn.raddr.ip}" if conn.raddr else "N/A"
                        rport = f"{conn.raddr.port}" if conn.raddr else "N/A"
                        
                        # Obține traficul per proces (aproximativ)
                        io = proc.io_counters() if hasattr(proc, 'io_counters') else None
                        trafic = f"{io.read_bytes/1024/1024:.1f}MB" if io else "N/A"
                        
                        tree.insert("", "end", values=(
                            proc_name,
                            laddr,
                            lport,
                            raddr,
                            rport,
                            conn.status,
                            trafic
                        ))
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                    except Exception:
                        continue
            except Exception as e:
                tk.messagebox.showerror("Eroare", f"Nu s-au putut obține conexiunile: {str(e)}")
            
            monitor_window.after(5000, actualizeaza_conexiuni)
        
        # Buton de actualizare manuală
        btn_refresh = tk.Button(
            header_frame,
            text="Actualizare",
            command=actualizeaza_conexiuni,
            bg=self.culoare_buton,
            fg=self.culoare_text,
            font=("Arial", 10),
            relief=tk.FLAT
        )
        btn_refresh.pack(side=tk.RIGHT, padx=10)
        
        # Prima actualizare
        actualizeaza_conexiuni()
        self.status_text.set("Monitor trafic internet pornit")
    
    def test_viteza_internet(self):
        self.status_text.set("Inițiez testul de viteză...")
        
        # Creează fereastra pentru testul de viteză
        speed_window = tk.Toplevel(self)
        speed_window.title("Test Viteză Internet")
        speed_window.geometry("600x500")
        speed_window.configure(bg=self.culoare_principala)
        
        # Adaugă header
        header_frame = tk.Frame(speed_window, bg=self.culoare_principala)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="TEST VITEZĂ INTERNET",
            font=("Arial", 16, "bold"),
            bg=self.culoare_principala,
            fg=self.culoare_accent
        )
        title_label.pack(side=tk.LEFT)
        
        # Frame principal pentru rezultate
        results_frame = tk.Frame(speed_window, bg=self.culoare_secundara, padx=20, pady=20)
        results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Etichete pentru rezultate
        download_label = tk.Label(
            results_frame,
            text="DOWNLOAD",
            font=("Arial", 14, "bold"),
            bg=self.culoare_secundara,
            fg=self.culoare_text
        )
        download_label.pack(pady=(20, 5))
        
        download_value = tk.Label(
            results_frame,
            text="-- Mbps",
            font=("Arial", 24, "bold"),
            bg=self.culoare_secundara,
            fg=self.culoare_accent
        )
        download_value.pack()
        
        upload_label = tk.Label(
            results_frame,
            text="UPLOAD",
            font=("Arial", 14, "bold"),
            bg=self.culoare_secundara,
            fg=self.culoare_text
        )
        upload_label.pack(pady=(20, 5))
        
        upload_value = tk.Label(
            results_frame,
            text="-- Mbps",
            font=("Arial", 24, "bold"),
            bg=self.culoare_secundara,
            fg=self.culoare_accent
        )
        upload_value.pack()
        
        ping_label = tk.Label(
            results_frame,
            text="PING",
            font=("Arial", 14, "bold"),
            bg=self.culoare_secundara,
            fg=self.culoare_text
        )
        ping_label.pack(pady=(20, 5))
        
        ping_value = tk.Label(
            results_frame,
            text="-- ms",
            font=("Arial", 24, "bold"),
            bg=self.culoare_secundara,
            fg=self.culoare_accent
        )
        ping_value.pack()
        
        # Status bar
        status_label = tk.Label(
            speed_window,
            text="Pregătit pentru test",
            font=("Arial", 10),
            bg=self.culoare_principala,
            fg=self.culoare_accent,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Buton pentru start test
        test_button = tk.Button(
            header_frame,
            text="Start Test",
            command=lambda: run_test(),
            bg=self.culoare_accent,
            fg=self.culoare_text,
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            padx=10
        )
        test_button.pack(side=tk.RIGHT, padx=10)
        
        # Funcție pentru rularea testului
        def run_test():
            download_value.config(text="-- Mbps")
            upload_value.config(text="-- Mbps")
            ping_value.config(text="-- ms")
            
            status_label.config(text="Se inițiază testul...")
            test_button.config(state=tk.DISABLED)
            
            def perform_test():
                try:
                    # Utilizăm modulul speedtest deja importat, nu mai facem import aici
                    
                    status_label.config(text="Conectare la serverele de test...")
                    st = speedtest.Speedtest()
                    st.get_best_server()
                    
                    status_label.config(text="Testare viteză download...")
                    download = st.download() / 1000000  # Convert to Mbps
                    speed_window.after(0, lambda: download_value.config(text=f"{download:.2f} Mbps"))
                    
                    status_label.config(text="Testare viteză upload...")
                    upload = st.upload() / 1000000  # Convert to Mbps
                    speed_window.after(0, lambda: upload_value.config(text=f"{upload:.2f} Mbps"))
                    
                    status_label.config(text="Testare ping...")
                    ping = st.results.ping
                    speed_window.after(0, lambda: ping_value.config(text=f"{ping:.0f} ms"))
                    
                    speed_window.after(0, lambda: status_label.config(text="Test finalizat!"))
                    speed_window.after(0, lambda: test_button.config(state=tk.NORMAL))
                    
                except Exception as e:
                    speed_window.after(0, lambda: status_label.config(text=f"Eroare: {str(e)}"))
                    speed_window.after(0, lambda: test_button.config(state=tk.NORMAL))
            
            # Rulează testul într-un thread separat
            threading.Thread(target=perform_test, daemon=True).start()
        
        self.status_text.set("Testare viteză internet deschisă")
    
    def deschide_proxy_browser(self):
        self.status_text.set("Inițiez browser proxy...")
        
        # Creez fereastra pentru browser proxy
        proxy_window = tk.Toplevel(self)
        proxy_window.title("Proxy Browser")
        proxy_window.geometry("600x500")
        proxy_window.configure(bg=self.culoare_principala)
        
        # Adaug header
        header_frame = tk.Frame(proxy_window, bg=self.culoare_principala)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="PROXY BROWSER",
            font=("Arial", 16, "bold"),
            bg=self.culoare_principala,
            fg=self.culoare_accent
        )
        title_label.pack(side=tk.LEFT)
        
        # Frame pentru introducerea URL-ului
        url_frame = tk.Frame(proxy_window, bg=self.culoare_secundara, padx=20, pady=20)
        url_frame.pack(fill="x", padx=20, pady=20)
        
        url_label = tk.Label(
            url_frame,
            text="Introduceți URL-ul:",
            font=("Arial", 12),
            bg=self.culoare_secundara,
            fg=self.culoare_text
        )
        url_label.pack(anchor="w", pady=(0, 10))
        
        url_var = tk.StringVar()
        url_entry = tk.Entry(
            url_frame,
            textvariable=url_var,
            font=("Arial", 12),
            bg=self.culoare_tertiara,
            fg=self.culoare_text,
            insertbackground=self.culoare_accent,
            width=50
        )
        url_entry.pack(fill="x", pady=(0, 10))
        url_entry.focus_set()
        
        # Frame pentru setările proxy
        proxy_settings_frame = tk.Frame(proxy_window, bg=self.culoare_secundara, padx=20, pady=20)
        proxy_settings_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        proxy_label = tk.Label(
            proxy_settings_frame,
            text="Proxy Server (opțional):",
            font=("Arial", 12),
            bg=self.culoare_secundara,
            fg=self.culoare_text
        )
        proxy_label.pack(anchor="w", pady=(0, 10))
        
        proxy_var = tk.StringVar(value="socks5://127.0.0.1:9050")  # Valoare implicită Tor
        proxy_entry = tk.Entry(
            proxy_settings_frame,
            textvariable=proxy_var,
            font=("Arial", 12),
            bg=self.culoare_tertiara,
            fg=self.culoare_text,
            insertbackground=self.culoare_accent,
            width=50
        )
        proxy_entry.pack(fill="x", pady=(0, 10))
        
        # Checkbox pentru a folosi proxy
        use_proxy_var = tk.BooleanVar(value=True)
        use_proxy_check = tk.Checkbutton(
            proxy_settings_frame,
            text="Folosește proxy",
            variable=use_proxy_var,
            font=("Arial", 10),
            bg=self.culoare_secundara,
            fg=self.culoare_text,
            selectcolor=self.culoare_tertiara,
            activebackground=self.culoare_secundara,
            activeforeground=self.culoare_accent
        )
        use_proxy_check.pack(anchor="w")
        
        # Frame pentru răspuns
        response_frame = tk.Frame(proxy_window, bg=self.culoare_secundara, padx=20, pady=20)
        response_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Text widget pentru afișarea stării
        status_text = tk.Text(
            response_frame,
            height=10,
            font=("Courier New", 10),
            bg=self.culoare_tertiara,
            fg=self.culoare_text,
            insertbackground=self.culoare_accent
        )
        status_text.pack(fill="both", expand=True)
        status_text.insert("1.0", "Pregătit pentru navigare. Introduceți un URL și apăsați pe Accesează.")
        status_text.config(state="disabled")
        
        # Buton pentru accesare URL
        access_button = tk.Button(
            proxy_window,
            text="ACCESEAZĂ",
            command=lambda: self.acceseaza_url_proxy(url_var.get(), proxy_var.get() if use_proxy_var.get() else None, status_text),
            font=("Arial", 10, "bold"),
            bg=self.culoare_accent,
            fg=self.culoare_text,
            activebackground=self.culoare_highlight,
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        access_button.pack(pady=(0, 20))
        
        self.status_text.set("Browser proxy deschis")
    
    def acceseaza_url_proxy(self, url, proxy, status_text):
        """Accesează un URL prin proxy și deschide rezultatul într-un browser"""
        # Activează editarea textului de status
        status_text.config(state="normal")
        status_text.delete("1.0", "end")
        
        # Verifică URL-ul
        if not url:
            status_text.insert("1.0", "Eroare: URL-ul nu poate fi gol.")
            status_text.config(state="disabled")
            return
        
        # Adaugă http:// dacă nu există
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        status_text.insert("1.0", f"Se accesează: {url}\n")
        if proxy:
            status_text.insert("end", f"Folosind proxy: {proxy}\n\n")
            
        # Salvăm referința către fereastra proxy pentru a putea actualiza interfața
        proxy_window = status_text.winfo_toplevel()
        
        # Crează un thread separat pentru a nu bloca interfața
        def acceseaza_in_background():
            try:
                # Pregătește proxy-urile în formatul cerut de requests
                proxies = None
                if proxy:
                    if proxy.startswith("socks5://"):
                        proxies = {"http": proxy, "https": proxy}
                    elif ":" in proxy:
                        host, port = proxy.split(":")
                        proxies = {
                            "http": f"http://{host}:{port}",
                            "https": f"http://{host}:{port}"
                        }
                
                # Adaugă informații în caseta de text
                proxy_window.after(0, lambda: status_text.insert("end", "Se trimite cererea...\n"))
                
                # Execută cererea
                start_time = time.time()
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                
                # Folosește biblioteca requests pentru a face cererea prin proxy
                response = requests.get(url, proxies=proxies, headers=headers, timeout=30)
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Adaugă informații despre răspuns
                proxy_window.after(0, lambda: status_text.insert("end", f"Răspuns primit! ({duration:.2f} secunde)\n"))
                proxy_window.after(0, lambda: status_text.insert("end", f"Status code: {response.status_code}\n"))
                
                # Creează un fișier temporar pentru conținutul paginii
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
                temp_file.write(response.content)
                temp_file.close()
                
                # Deschide fișierul HTML în browser
                import webbrowser
                webbrowser.open(f"file://{temp_file.name}")
                
                proxy_window.after(0, lambda: status_text.insert("end", f"Pagina a fost deschisă în browser.\n"))
                
            except Exception as e:
                proxy_window.after(0, lambda: status_text.insert("end", f"Eroare: {str(e)}\n"))
            finally:
                proxy_window.after(0, lambda: status_text.config(state="disabled"))
        
        # Pornește thread-ul pentru accesarea URL-ului
        threading.Thread(target=acceseaza_in_background, daemon=True).start()

    def create_app_icon(self):
        """Creează și setează iconul aplicației cu un dragon roșu"""
        try:
            # Verificăm dacă avem deja un icon salvat
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "windows_help_icon.ico")
            
            # Dacă nu există, îl creăm
            if not os.path.exists(icon_path):
                # Creează un icon pentru dragon roșu
                icon_size = (128, 128)
                icon_img = Image.new('RGBA', icon_size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(icon_img)
                
                # Culori pentru dragon
                red_color = (220, 0, 0, 255)  # Roșu intens
                dark_red = (150, 0, 0, 255)   # Roșu închis pentru detalii
                
                # Desenează corpul dragonului (formă simplificată)
                # Cap
                draw.ellipse([(40, 20), (75, 55)], fill=red_color)
                
                # Corp
                points = [
                    (60, 45),   # Conectare la cap
                    (85, 60),   # Umăr
                    (70, 90),   # Curbă spate
                    (85, 105),  # Coadă început
                    (95, 115),  # Coadă mijloc
                    (105, 100), # Coadă vârf
                    (80, 85),   # Coadă interior
                    (50, 75),   # Burtă
                    (45, 60),   # Piept
                    (60, 45)    # Închidere
                ]
                draw.polygon(points, fill=red_color, outline=dark_red)
                
                # Aripi
                wing_points = [
                    (65, 65),   # Bază aripă
                    (45, 45),   # Vârf sus
                    (25, 65),   # Vârf mijloc
                    (30, 85),   # Vârf jos
                    (65, 75)    # Bază aripă jos
                ]
                draw.polygon(wing_points, fill=red_color, outline=dark_red)
                
                # Ochi
                draw.ellipse([(50, 30), (55, 35)], fill=(255, 255, 255, 255))
                draw.ellipse([(51, 31), (54, 34)], fill=(0, 0, 0, 255))
                
                # Foc/Flacără
                flame_points = [
                    (40, 38),   # Gură
                    (25, 30),   # Flacără sus
                    (15, 38),   # Flacără mijloc
                    (25, 45),   # Flacără jos
                    (40, 42)    # Gură jos
                ]
                draw.polygon(flame_points, fill=(255, 165, 0, 255), outline=(255, 140, 0, 255))
                
                # Salvăm iconul
                icon_img.save(icon_path, format="ICO")
            
            # Setăm iconul aplicației
            self.iconbitmap(icon_path)
            
        except Exception as e:
            print(f"Nu s-a putut seta iconul: {str(e)}")
            # Continuăm chiar dacă iconul nu poate fi setat

# Punctul de intrare principal
if __name__ == "__main__":
    try:
        # Asigură-te că bibliotecile necesare sunt importate
        import tkinter as tk
        from PIL import Image, ImageTk, ImageEnhance
        import requests
        import psutil
        import speedtest  # Import global pentru speedtest
    except ImportError as e:
        print(f"Eroare la import: {e}")
        print("Instalați bibliotecile lipsă folosind:")
        print("pip install pillow requests psutil speedtest-cli")
        input("Apăsați Enter pentru a ieși...")
        exit(1)
        
    # Pornește aplicația
    app = UtilitarSistem()
    app.mainloop()