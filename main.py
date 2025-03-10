import requests
import customtkinter as ctk
from git import Repo
import os
import json

class DiscordEmbed2:
    def __init__(self, root):
        self.root = root
        self.webhooks = {}
        self.last_message_settings = {}
        self.load_webhooks()
        self.load_last_message_settings()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("DiscordEmbed2 - Ein Produkt von Nico Inc. Ver.: 2.0.1")
        self.root.geometry("700x600")

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

        self.title_entry = ctk.CTkEntry(self.main_tab, placeholder_text="Enter title")
        self.title_entry.pack(pady=(0, 10), fill="x", padx=10)

        # Message Entry
        self.message_label = ctk.CTkLabel(self.main_tab, text="Body")
        self.message_label.pack(pady=(10, 0))

        self.message_entry = ctk.CTkTextbox(self.main_tab, height=100)
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
        self.send_button = ctk.CTkButton(self.main_tab, text="Send Message", command=self.send_message)
        self.send_button.pack(pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(self.main_tab, text="")
        self.status_label.pack(pady=10)

        # Load last message settings
        self.load_last_message_settings_ui()

    def setup_settings_tab(self):
        # Webhook URL and Name Entry
        self.webhook_url_label = ctk.CTkLabel(self.settings_tab, text="Webhook URL")
        self.webhook_url_label.pack(pady=(10, 0))

        self.webhook_entry = ctk.CTkEntry(self.settings_tab, placeholder_text="Webhook URL")
        self.webhook_entry.pack(pady=(0, 10))

        self.webhook_name_label = ctk.CTkLabel(self.settings_tab, text="Webhook Name")
        self.webhook_name_label.pack(pady=(10, 0))

        self.webhook_name_entry = ctk.CTkEntry(self.settings_tab, placeholder_text="Webhook Name")
        self.webhook_name_entry.pack(pady=(0, 10))

        self.add_webhook_button = ctk.CTkButton(self.settings_tab, text="Add Webhook", command=self.add_webhook)
        self.add_webhook_button.pack(pady=10)

        # Webhook Selector Label
        self.webhook_selector_label = ctk.CTkLabel(self.settings_tab, text="No Webhooks Configured" if not self.webhooks else "Select Webhook")
        self.webhook_selector_label.pack(pady=10)

    def add_webhook(self):
        url = self.webhook_entry.get()
        name = self.webhook_name_entry.get()
        if url and name:
            self.webhooks[name] = url
            self.webhook_selector.configure(values=list(self.webhooks.keys()))
            self.webhook_selector_label.configure(text="Select Webhook")
            self.save_webhooks()

    def format_text(self, formatting):
        try:
            selected_text = self.message_entry.get("sel.first", "sel.last")
            if selected_text:
                self.message_entry.insert("sel.first", formatting)
                self.message_entry.insert("sel.last", formatting)
        except:
            pass

    def send_message(self):
        webhook_name = self.webhook_selector.get()
        title = self.title_entry.get()
        message = self.message_entry.get("1.0", "end-1c")
        embed_color = self.get_embed_color()

        if not webhook_name:
            self.status_label.configure(text="Error: No webhook selected", text_color="red")
            return
        if not message:
            self.status_label.configure(text="Error: No message entered", text_color="red")
            return

        try:
            # Add signature to the message with a line break
            signature = "\n\n*by Nico Inc. Vers.: 2.0.1*"
            full_message = f"**{title}**\n{message}{signature}" if title else f"{message}{signature}"

            embed = None
            if title or embed_color:
                embed = {
                    "title": title,
                    "description": message + signature,  # Add signature to the embed description
                    "color": embed_color
                }

            payload = {
                "content": full_message if not title else None,
                "embeds": [embed] if embed else None
            }

            response = requests.post(self.webhooks[webhook_name], json=payload)
            if response.status_code == 204:
                self.status_label.configure(text="Message sent successfully", text_color="green")
                self.save_last_message_settings(webhook_name, title, message, embed_color)
            else:
                self.status_label.configure(text=f"Error: {response.status_code}", text_color="red")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def get_embed_color(self):
        color_choice = self.embed_color_selector.get()
        if color_choice == "Benutzerdefiniert":
            return int(self.embed_color_entry.get()[1:], 16) if self.embed_color_entry.get() else None
        else:
            return int(color_choice.split(" (#")[1][:-1], 16)

    def load_last_message_settings_ui(self):
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
        self.last_message_settings = {
            "webhook_name": webhook_name,
            "title": title,
            "message": message,
            "embed_color": embed_color
        }
        with open("last_message_settings.json", "w") as file:
            json.dump(self.last_message_settings, file)

    def load_last_message_settings(self):
        if os.path.exists("last_message_settings.json"):
            with open("last_message_settings.json", "r") as file:
                self.last_message_settings = json.load(file)

    def load_webhooks(self):
        if os.path.exists("webhooks.json"):
            with open("webhooks.json", "r") as file:
                self.webhooks = json.load(file)

    def save_webhooks(self):
        with open("webhooks.json", "w") as file:
            json.dump(self.webhooks, file)

    def update_repo(self):
        try:
            repo = Repo(os.getcwd())
            origin = repo.remotes.origin
            origin.pull()
        except Exception as e:
            print(f"Error updating repo: {e}")

if __name__ == "__main__":
    root = ctk.CTk()
    app = DiscordEmbed2(root)
    root.mainloop()