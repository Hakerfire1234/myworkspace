from tkinter import *
from tkinter import simpledialog, messagebox
import os
import shutil
import zipfile
import time

window = Tk()
window.title("MyWorkspace")
window.geometry("700x500")
window.configure(bg="#f0f0f0")

folder_path = StringVar()
folder_path.set(os.getcwd())

def show_files():
    file_list.delete(0, END)
    try:
        items = os.listdir(folder_path.get())
        for name in items:
            file_list.insert(END, name)
    except:
        pass

def delete_files():
    selected = file_list.curselection()
    for i in selected[::-1]:
        name = file_list.get(i)
        path = os.path.join(folder_path.get(), name)
        try:
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
        except:
            pass
    show_files()

def rename_file():
    selected = file_list.curselection()
    if not selected:
        return
    old_name = file_list.get(selected[0])
    new_name = simpledialog.askstring("Rename", "New name:")
    if new_name:
        os.rename(os.path.join(folder_path.get(), old_name), os.path.join(folder_path.get(), new_name))
    show_files()

def zip_files():
    folder_name = os.path.basename(folder_path.get())
    zip_name = folder_name + ".zip"
    with zipfile.ZipFile(zip_name, "w") as z:
        for root, dirs, files in os.walk(folder_path.get()):
            for f in files:
                path = os.path.join(root, f)
                z.write(path, os.path.relpath(path, folder_path.get()))
    show_files()

def search_file():
    word = simpledialog.askstring("Search", "File name:")
    if not word:
        return
    file_list.delete(0, END)
    for name in os.listdir(folder_path.get()):
        if word.lower() in name.lower():
            file_list.insert(END, name)

def toggle_theme():
    if window["bg"] == "#f0f0f0":
        window.configure(bg="#1e1e1e")
        top_bar.configure(bg="#1e1e1e")
        file_list.configure(bg="#2b2b2b", fg="white")
    else:
        window.configure(bg="#f0f0f0")
        top_bar.configure(bg="#f0f0f0")
        file_list.configure(bg="white", fg="black")

def new_folder():
    name = simpledialog.askstring("New Folder", "Folder name:")
    if name:
        new_path = os.path.join(folder_path.get(), name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        show_files()

def file_info():
    selected = file_list.curselection()
    if not selected:
        return
    name = file_list.get(selected[0])
    path = os.path.join(folder_path.get(), name)
    info = os.stat(path)
    size = info.st_size
    created = time.ctime(info.st_ctime)
    changed = time.ctime(info.st_mtime)
    is_folder = os.path.isdir(path)
    text = f"Name: {name}\nType: {'Folder' if is_folder else 'File'}\nSize: {size} bytes\nCreated: {created}\nModified: {changed}"
    messagebox.showinfo("Info", text)

top_bar = Frame(window, bg="#f0f0f0")
top_bar.pack(fill=X)

Button(top_bar, text="🗑 Delete", command=delete_files).pack(side=LEFT, padx=5, pady=5)
Button(top_bar, text="✏️ Rename", command=rename_file).pack(side=LEFT, padx=5, pady=5)
Button(top_bar, text="📦 Zip", command=zip_files).pack(side=LEFT, padx=5, pady=5)
Button(top_bar, text="🔍 Search", command=search_file).pack(side=LEFT, padx=5, pady=5)
Button(top_bar, text="🌙 Dark Mode", command=toggle_theme).pack(side=LEFT, padx=5, pady=5)
Button(top_bar, text="📁 New Folder", command=new_folder).pack(side=LEFT, padx=5, pady=5)
Button(top_bar, text="📊 View Info", command=file_info).pack(side=LEFT, padx=5, pady=5)

file_list = Listbox(window, selectmode=EXTENDED, bg="white", fg="black")
file_list.pack(fill=BOTH, expand=True, padx=10, pady=10)

show_files()
window.mainloop()
