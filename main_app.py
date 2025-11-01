import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import webbrowser
import os

CSV_FILE = "playlists.csv"

def load_playlists(csv_path=CSV_FILE):
    if not os.path.exists(csv_path):
        messagebox.showerror("File missing", f"{csv_path} not found in the project folder.")
        return pd.DataFrame(columns=["mood","language","playlist_name","link"])
    df = pd.read_csv(csv_path)
    df['mood'] = df['mood'].fillna('other').str.lower()
    df['language'] = df['language'].fillna('english').str.lower()
    return df

class PlaylistApp:
    def __init__(self, root):
        self.root = root
        root.title("Mood → Spotify Playlists")
        root.geometry("700x420")
        root.resizable(False, False)
        self.df = load_playlists()
        self.moods = sorted(self.df['mood'].unique())
        self.create_ui()

    def create_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill='both', expand=True)

        header = ttk.Label(frm, text="Select your mood to open curated Spotify playlists", font=("Segoe UI", 14))
        header.pack(pady=(0,10))

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(fill='x', pady=(0,10))
        cols = 4
        for idx, mood in enumerate(self.moods):
            btn = ttk.Button(btn_frame, text=mood.capitalize(), width=18, command=lambda m=mood: self.show_playlists(m))
            r = idx // cols
            c = idx % cols
            btn.grid(row=r, column=c, padx=6, pady=6)

        self.list_frame = ttk.Frame(frm)
        self.list_frame.pack(fill='both', expand=True, pady=(10,0))

        info = ttk.Label(self.list_frame, text="Click a mood button to see playlists (English + Hindi where available).", wraplength=620)
        info.pack(pady=(0,6))

        self.playlist_box = tk.Listbox(self.list_frame, height=8, width=90)
        self.playlist_box.pack(side='left', fill='both', expand=True, padx=(0,6))

        scrollbar = ttk.Scrollbar(self.list_frame, orient='vertical', command=self.playlist_box.yview)
        scrollbar.pack(side='right', fill='y')
        self.playlist_box.configure(yscrollcommand=scrollbar.set)

        open_btn = ttk.Button(frm, text="Open Selected Playlist", command=self.open_selected)
        open_btn.pack(pady=(8,0))

        open_all_btn = ttk.Button(frm, text="Open All Shown Playlists", command=self.open_all)
        open_all_btn.pack(pady=(6,0))

    def show_playlists(self, mood):
        mood = mood.lower()
        dfm = self.df[self.df['mood'] == mood]
        self.playlist_box.delete(0, tk.END)
        if dfm.empty:
            self.playlist_box.insert(tk.END, f"No playlists found for mood: {mood}")
            return
        for idx, row in dfm.iterrows():
            display = f"{row['playlist_name']} ({row['language'].capitalize()})  - {row['link']}"
            self.playlist_box.insert(tk.END, display)

    def open_selected(self):
        sel = self.playlist_box.curselection()
        if not sel:
            messagebox.showinfo("Select one", "Please select a playlist from the list first.")
            return
        text = self.playlist_box.get(sel[0])
        # extract URL
        import re
        m = re.search(r"(https?://\S+)", text)
        if m:
            webbrowser.open(m.group(1))
        else:
            messagebox.showinfo("No link", "Couldn't extract a link.")

    def open_all(self):
        items = self.playlist_box.get(0, tk.END)
        import re
        links = []
        for it in items:
            m = re.search(r"(https?://\S+)", it)
            if m:
                links.append(m.group(1))
        if not links:
            messagebox.showinfo("No links", "No links to open.")
            return
        for link in links:
            webbrowser.open(link)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistApp(root)
    root.mainloop()
