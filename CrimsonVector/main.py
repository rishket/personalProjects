# CrimsonVector Red Team Toolkit

import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading

class CrimsonVectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CrimsonVector Red Team Toolkit - Developer: RKV")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        self.nmap_tab = ttk.Frame(self.notebook)
        self.whois_tab = ttk.Frame(self.notebook)
        self.nikto_tab = ttk.Frame(self.notebook)
        self.gobuster_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.nmap_tab, text="Nmap")
        self.notebook.add(self.whois_tab, text="Whois")
        self.notebook.add(self.nikto_tab, text="Nikto")
        self.notebook.add(self.gobuster_tab, text="Gobuster")

        self.build_nmap_tab()
        self.build_whois_tab()
        self.build_nikto_tab()
        self.build_gobuster_tab()
    # Nmap Scanner
    def build_nmap_tab(self):
        input_frame = ttk.Frame(self.nmap_tab)
        input_frame.pack(pady=5, fill="x")
        description = ttk.Label(self.nmap_tab, text="Use this tab to perform network scans with Nmap.\n"
        "Enter an IP or hostname, then click 'Scan'.\n"
        "Use 'Kill Scan' if you need to stop early.",
        foreground="red"
        )
        description.pack(padx=5, pady=5, anchor="w")
        
        ttk.Label(input_frame, text="Target:").pack(side="left")
        self.nmap_target_entry = ttk.Entry(input_frame, width=40)
        self.nmap_target_entry.pack(side="left", padx=5)

        self.nmap_scan_button = ttk.Button(input_frame, text="Scan", command=self.start_scan)
        self.nmap_scan_button.pack(side="left", padx=5)

        self.nmap_kill_button = ttk.Button(input_frame, text="Kill Scan", command=self.kill_scan, state=tk.DISABLED)
        self.nmap_kill_button.pack(side="left")

        self.nmap_output_box = scrolledtext.ScrolledText(self.nmap_tab, wrap=tk.WORD, height=20, width=80)
        self.nmap_output_box.pack(padx=5, pady=5, fill="both", expand=True)

        self.nmap_process = None

    def run_scan(self, target):
        try:
            self.nmap_process = subprocess.Popen(
                ["nmap", target],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in self.nmap_process.stdout:
                self.append_output(line, tab="nmap")
        except Exception as e:
            self.append_output(f"Error: {e}\n", tab="nmap")
        finally:
            self.nmap_scan_button.config(state=tk.NORMAL)
            self.nmap_kill_button.config(state=tk.DISABLED)
            self.nmap_process = None

    def start_scan(self):
        target = self.nmap_target_entry.get().strip()
        if not target:
            self.append_output("No target specified.\n", tab="nmap")
            return
        self.append_output(f"Scanning {target} with Nmap...\n", tab="nmap")
        self.nmap_scan_button.config(state=tk.DISABLED)
        self.nmap_kill_button.config(state=tk.NORMAL)
        threading.Thread(target=self.run_scan, args=(target,), daemon=True).start()

    def kill_scan(self):
        if self.nmap_process and self.nmap_process.poll() is None:
            self.append_output("Killing scan...\n", tab="nmap")
            self.nmap_process.terminate()
            self.nmap_process = None
            self.nmap_scan_button.config(state=tk.NORMAL)
            self.nmap_kill_button.config(state=tk.DISABLED)

    # Whois Lookup
    def build_whois_tab(self):
        input_frame = ttk.Frame(self.whois_tab)
        input_frame.pack(pady=5, fill="x")
        description = ttk.Label(
        self.whois_tab,
        text="Perform WHOIS lookups to gather domain registration info.\n"
        "Enter a domain (e.g., example.com) and click 'Lookup'.",
        foreground="red"
        )
        description.pack(padx=5, pady=5, anchor="w")

        ttk.Label(input_frame, text="Target:").pack(side="left")
        self.whois_target_entry = ttk.Entry(input_frame, width=40)
        self.whois_target_entry.pack(side="left", padx=5)
        
        self.whois_lookup_button = ttk.Button(input_frame, text="Lookup", command=self.start_lookup)
        self.whois_lookup_button.pack(side="left", padx=5)
        
        self.whois_output_box = scrolledtext.ScrolledText(self.whois_tab, wrap=tk.WORD, height=20, width=80)
        self.whois_output_box.pack(padx=5, pady=5, fill="both", expand=True)

    def run_lookup(self):
        target = self.whois_target_entry.get().strip()
        if not target:
            self.append_output("No target specified.\n", tab="whois")
            return
        self.append_output(f"Looking up {target}...\n", tab="whois")
        try:
            result = subprocess.run(["whois", target], capture_output=True, text=True)
            if result.returncode == 0:
                self.append_output(result.stdout, tab="whois")
            else:
                self.append_output(f"Error: {result.stderr}\n", tab="whois")
        except Exception as e:
            self.append_output(f"Error: {e}\n", tab="whois")

    def start_lookup(self):
        threading.Thread(target=self.run_lookup, daemon=True).start()
        
    # Nikto
    def build_nikto_tab(self):
        input_frame = ttk.Frame(self.nikto_tab)
        input_frame.pack(pady=5, fill="x")
        
        description = ttk.Label(
        self.nikto_tab,
        text="Run web vulnerability scans with Nikto.\n"
        "Enter a target URL (http:// or https:// or www.) and click 'Scan'.\n"
        "USE RESPONSIBLY — this can be intrusive.",
        foreground="red"
        )
        
        description.pack(padx=5, pady=5, anchor="w")
        ttk.Label(input_frame, text="Target URL: ").pack(side="left")
        self.nikto_entry = ttk.Entry(input_frame, width=40)
        self.nikto_entry.pack(side="left", padx=5)  
        
        self.nikto_scan_button = ttk.Button(input_frame, text="Scan", command=self.start_nikto_scan)
        self.nikto_scan_button.pack(side="left", padx=5)
        
        self.nikto_kill_button = ttk.Button(input_frame, text="Kill Scan", command=self.kill_nikto_scan, state=tk.DISABLED)
        self.nikto_kill_button.pack(side="left")
        
        self.nikto_output_box = scrolledtext.ScrolledText(self.nikto_tab, wrap=tk.WORD, height=20, width=80)
        self.nikto_output_box.pack(padx=5, pady=5, fill="both", expand=True)
        
        self.nikto_process = None
        
    def run_nikto_scan(self, target):
        try:
            self.nikto_process = subprocess.Popen(
                ["nikto", "-h", target],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in self.nikto_process.stdout:
                self.append_output(line, tab="nikto")
        except Exception as e:
            self.append_output(f"Error: {e}\n", tab="nikto")
        finally:
            self.nikto_scan_button.config(state=tk.NORMAL)
            self.nikto_kill_button.config(state=tk.DISABLED)
            self.nikto_process = None
            
    def start_nikto_scan(self):
        target = self.nikto_entry.get().strip()
        if not target:
            self.append_output("No target specified.\n", tab="nikto")
            return
        self.append_output(f"Scanning {target} with Nikto...\n", tab="nikto")
        self.nikto_scan_button.config(state=tk.DISABLED)
        self.nikto_kill_button.config(state=tk.NORMAL)
        threading.Thread(target=self.run_nikto_scan, args=(target,), daemon=True).start()
        
    def kill_nikto_scan(self):
        if self.nikto_process and self.nikto_process.poll() is None:
            self.append_nikto_output("Killing scan...\n")
            self.nikto_process.terminate()
            self.nikto_process = None
            self.nikto_scan_button.config(state=tk.NORMAL)
            self.nikto_kill_button.config(state=tk.DISABLED)

    def append_output(self, text, tab="nmap"):
        if tab == "nmap":
            self.nmap_output_box.insert(tk.END, text)
            self.nmap_output_box.see(tk.END)
        elif tab == "whois":
            self.whois_output_box.insert(tk.END, text)
            self.whois_output_box.see(tk.END)
        elif tab == "nikto":
            self.nikto_output_box.insert(tk.END, text)
            self.nikto_output_box.see(tk.END)
            
    # Gobuster
# --- inside CrimsonVectorApp class ---

    def build_gobuster_tab(self):
        description = ttk.Label(self.gobuster_tab, text="Use Gobuster to brute-force directories and files on web servers.\n"
        "Enter a target URL and select a wordlist, then click 'Scan'.\n"
        "You can also enter a custom wordlist path if needed.",
        foreground="red"
        )
        description.pack(padx=5, pady=5, anchor="w")
        input_frame = ttk.Frame(self.gobuster_tab)
        input_frame.pack(pady=5, fill="x")

        # Target URL
        ttk.Label(input_frame, text="Target URL:").pack(side="left")
        self.gobuster_target_entry = ttk.Entry(input_frame, width=40)
        self.gobuster_target_entry.pack(side="left", padx=5)

        # Wordlist selector
        wordlist_frame = ttk.Frame(self.gobuster_tab)
        wordlist_frame.pack(pady=5, fill="x")

        ttk.Label(wordlist_frame, text="Wordlist:").pack(side="left")

        # Gather wordlists
        import glob, os
        default_wordlists = glob.glob("/usr/share/wordlists/**/*.txt", recursive=True)
        if not default_wordlists:
            default_wordlists = []

        self.wordlist_var = tk.StringVar()
        if default_wordlists:
            self.wordlist_dropdown = ttk.Combobox(wordlist_frame, textvariable=self.wordlist_var, values=default_wordlists, width=60)
            self.wordlist_dropdown.current(0)
        else:
            self.wordlist_dropdown = ttk.Combobox(wordlist_frame, textvariable=self.wordlist_var, values=[], width=60)
        self.wordlist_dropdown.pack(side="left", padx=5)

        # Custom wordlist entry fallback
        self.gobuster_wordlist_entry = ttk.Entry(wordlist_frame, width=40)
        self.gobuster_wordlist_entry.pack(side="left", padx=5)
        self.gobuster_wordlist_entry.insert(0, "Optional: Enter custom wordlist path")

        # Buttons
        button_frame = ttk.Frame(self.gobuster_tab)
        button_frame.pack(pady=5, fill="x")

        self.gobuster_scan_button = ttk.Button(button_frame, text="Scan", command=self.start_gobuster_scan)
        self.gobuster_scan_button.pack(side="left", padx=5)

        self.gobuster_kill_button = ttk.Button(button_frame, text="Kill Scan", command=self.kill_gobuster_scan, state=tk.DISABLED)
        self.gobuster_kill_button.pack(side="left")

        # Output box
        self.gobuster_output_box = scrolledtext.ScrolledText(self.gobuster_tab, wrap=tk.WORD, height=20, width=80)
        self.gobuster_output_box.pack(padx=5, pady=5, fill="both", expand=True)

        self.gobuster_process = None

    def append_gobuster_output(self, text, tab="gobuster"):
        if tab == "gobuster":
            self.gobuster_output_box.insert(tk.END, text)
            self.gobuster_output_box.see(tk.END)

    def run_gobuster_scan(self, target, wordlist):
        try:
            self.gobuster_process = subprocess.Popen(
                ["gobuster", "dir", "-u", target, "-w", wordlist],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            for line in self.gobuster_process.stdout:
                self.append_gobuster_output(line)
        except Exception as e:
            self.append_gobuster_output(f"Error: {e}\n")
        finally:
            self.gobuster_scan_button.config(state=tk.NORMAL)
            self.gobuster_kill_button.config(state=tk.DISABLED)
            self.gobuster_process = None

    def start_gobuster_scan(self):
        target = self.gobuster_target_entry.get().strip()
        wordlist = self.wordlist_var.get().strip() or self.gobuster_wordlist_entry.get().strip()

        if not target or not wordlist:
            self.append_gobuster_output("Target or wordlist not specified.\n")
            return
        self.append_gobuster_output(f"Running Gobuster on {target} with wordlist {wordlist}...\n")
        self.gobuster_scan_button.config(state=tk.DISABLED)
        self.gobuster_kill_button.config(state=tk.NORMAL)
        threading.Thread(target=self.run_gobuster_scan, args=(target, wordlist), daemon=True).start()

    def kill_gobuster_scan(self):
        if self.gobuster_process and self.gobuster_process.poll() is None:
            self.append_gobuster_output("Killing scan...\n")
            self.gobuster_process.terminate()
            self.gobuster_process = None
            self.gobuster_scan_button.config(state=tk.NORMAL)
            self.gobuster_kill_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrimsonVectorApp(root)
    root.mainloop()
