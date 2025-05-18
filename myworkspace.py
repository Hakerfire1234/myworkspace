import os
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import shutil
import zipfile

is_dark_mode = False

def apply_theme():
    bg = "#1e1e1e" if is_dark_mode else "#f0f0f0"
    fg = "#ffffff" if is_dark_mode else "#000000"
    shadow = "#333333" if is_dark_mode else "#aaaaaa"
    list_bg = "#2e2e2e" if is_dark_mode else "#ffffff"

    root.configure(bg=bg)
    label.config(bg=bg, fg=fg)
    file_frame.config(bg=shadow)
    file_list.config(bg=list_bg, fg=fg)
    btn_frame.config(bg=bg)
    toggle_btn.config(bg=list_bg, fg=fg, activebackground=shadow)

    for frame in button_frames:
        frame.config(bg=shadow)
        for widget in frame.winfo_children():
            widget.config(bg=list_bg, fg=fg, activebackground=shadow)

def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    apply_theme()

def list_files():
    file_list.delete(0, tk.END)
    for file in os.listdir(folder_path):
        file_list.insert(tk.END, file)

def delete_files():
    selected = file_list.curselection()
    for i in selected:
        file_name = file_list.get(i)
        full_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(full_path):
                os.remove(full_path)
            elif os.path.isdir(full_path):
                shutil.rmtree(full_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    list_files()

def rename_file():
    selected = file_list.curselection()
    if len(selected) != 1:
        messagebox.showinfo("Rename", "Select only one file to rename.")
        return
    old_name = file_list.get(selected[0])
    new_name = simpledialog.askstring("Rename", f"New name for {old_name}:")
    if new_name:
        os.rename(os.path.join(folder_path, old_name), os.path.join(folder_path, new_name))
        list_files()

def zip_folder():
    save_path = filedialog.asksaveasfilename(defaultextension=".zip")
    if not save_path:
        return
    with zipfile.ZipFile(save_path, "w") as zipf:
        for file in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file)
            zipf.write(full_path, file)
    messagebox.showinfo("Zip", "Folder zipped!")

def search_files():
    keyword = simpledialog.askstring("Search", "Enter part of a file name:")
    if not keyword:
        return
    file_list.delete(0, tk.END)
    for file in os.listdir(folder_path):
        if keyword.lower() in file.lower():
            file_list.insert(tk.END, file)

# Setup
folder_path = os.getcwd()
root = tk.Tk()
root.title("🧰 MyWorkspace")

label = tk.Label(root, text=f"📁 Folder: {folder_path}", font=("Segoe UI", 11), anchor="w")
label.pack(fill="x", padx=10, pady=5)

file_frame = tk.Frame(root, bd=1, relief="sunken")
file_frame.pack(padx=10, pady=5, fill="both", expand=True)

file_list = tk.Listbox(file_frame, selectmode=tk.MULTIPLE, font=("Segoe UI", 10), bd=0, highlightthickness=0, relief="flat")
file_list.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)

scrollbar = tk.Scrollbar(file_frame, command=file_list.yview)
scrollbar.pack(side="right", fill="y")
file_list.config(yscrollcommand=scrollbar.set)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

button_frames = []

def shadow_button(text, command):
    frame = tk.Frame(btn_frame)
    frame.pack(side="left", padx=6, pady=4)
    btn = tk.Button(frame, text=text, command=command, font=("Segoe UI", 10),
                    width=10, bd=1, relief="flat")
    btn.pack()
    button_frames.append(frame)

shadow_button("🔄 Refresh", list_files)
shadow_button("🗑️ Delete", delete_files)
shadow_button("✏️ Rename", rename_file)
shadow_button("📦 Zip", zip_folder)
shadow_button("🔍 Search", search_files)

toggle_btn = tk.Button(root, text="🌙 Toggle Dark Mode", command=toggle_dark_mode, font=("Segoe UI", 10), bd=1)
toggle_btn.pack(pady=(0, 10))

apply_theme()
list_files()
root.mainloop()
