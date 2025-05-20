from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import os, shutil, zipfile, time
from PIL import Image, ImageTk

app = Tk()
app.title("MyWorkspace")
app.geometry("1000x600")
app.configure(bg="#f0f0f0")
app.iconphoto(False, PhotoImage(file="folder_icon.png"))

path = StringVar()
path.set(os.getcwd())
img_now = None

def update():
    listbox.delete(0, END)
    try:
        files = os.listdir(path.get())
        for f in files:
            listbox.insert(END, f)
    except:
        pass

def delete():
    sel = listbox.curselection()
    for i in sel[::-1]:
        p = os.path.join(path.get(), listbox.get(i))
        try:
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p)
        except:
            pass
    update()

def rename():
    sel = listbox.curselection()
    if not sel:
        return
    old = listbox.get(sel[0])
    new = simpledialog.askstring("✏️ Rename", f"Rename '{old}' to:")
    if new:
        os.rename(os.path.join(path.get(), old), os.path.join(path.get(), new))
    update()

def zipf():
    name = os.path.basename(path.get()) + ".zip"
    with zipfile.ZipFile(name, 'w') as z:
        for root, dirs, files in os.walk(path.get()):
            for f in files:
                fp = os.path.join(root, f)
                z.write(fp, os.path.relpath(fp, path.get()))
    update()

def search():
    q = simpledialog.askstring("🔍 Search", "Enter file name:")
    if not q:
        return
    listbox.delete(0, END)
    for f in os.listdir(path.get()):
        if q.lower() in f.lower():
            listbox.insert(END, f)

def dark():
    b = app.cget("bg")
    d = b == "#f0f0f0"
    app.configure(bg="#1e1e1e" if d else "#f0f0f0")
    listbox.configure(bg="#2b2b2b" if d else "white", fg="white" if d else "black")
    buttonbar.configure(bg="#1e1e1e" if d else "#f0f0f0")

def newfolder():
    name = simpledialog.askstring("📁 New Folder", "Folder name:")
    if name:
        p = os.path.join(path.get(), name)
        if not os.path.exists(p):
            os.makedirs(p)
    update()

def info():
    s = listbox.curselection()
    if not s:
        return
    f = listbox.get(s[0])
    p = os.path.join(path.get(), f)
    st = os.stat(p)
    msg = f"Name: {f}\nType: {'Folder' if os.path.isdir(p) else 'File'}\nSize: {st.st_size} bytes\nCreated: {time.ctime(st.st_ctime)}\nModified: {time.ctime(st.st_mtime)}"
    messagebox.showinfo("📊 Info", msg)

def newfile():
    name = simpledialog.askstring("📄 New File", "File name:")
    if name:
        p = os.path.join(path.get(), name)
        with open(p, 'w'):
            pass
    update()

def openf():
    s = listbox.curselection()
    if not s:
        return
    f = listbox.get(s[0])
    p = os.path.join(path.get(), f)
    if os.path.isdir(p):
        path.set(p)
        update()

def back():
    path.set(os.path.dirname(path.get()))
    update()

def show(e):
    global img_now
    sel = listbox.curselection()
    if not sel:
        previewtext.delete("1.0", END)
        previewimage.config(image="")
        return
    f = listbox.get(sel[0])
    p = os.path.join(path.get(), f)
    previewtext.delete("1.0", END)
    previewimage.config(image="")
    img_now = None
    try:
        if os.path.isfile(p):
            ext = os.path.splitext(p)[1].lower()
            if ext in [".png", ".jpg", ".jpeg", ".gif"]:
                img = Image.open(p)
                img.thumbnail((250, 250))
                img_now = ImageTk.PhotoImage(img)
                previewimage.config(image=img_now)
            elif ext in [".txt", ".py", ".json", ".html", ".csv", ".md", ".js"]:
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                previewtext.insert(END, content)
    except:
        previewtext.insert(END, "[Preview Error]")

buttonbar_holder = Frame(app)
buttonbar_holder.pack(fill=X)

bar_canvas = Canvas(buttonbar_holder, height=40, bg="#f0f0f0", highlightthickness=0)
bar_scroll = Scrollbar(buttonbar_holder, orient=HORIZONTAL, command=bar_canvas.xview)
bar_canvas.configure(xscrollcommand=bar_scroll.set)
bar_scroll.pack(side=BOTTOM, fill=X)
bar_canvas.pack(side=TOP, fill=X, expand=True)

buttonbar = Frame(bar_canvas, bg="#f0f0f0")
bar_canvas.create_window((0, 0), window=buttonbar, anchor="nw")

buttonbar.bind("<Configure>", lambda e: bar_canvas.configure(scrollregion=bar_canvas.bbox("all")))

Button(buttonbar, text="🗑️", command=delete).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="✏️", command=rename).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="📦", command=zipf).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="🔍", command=search).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="🌙", command=dark).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="📁", command=newfolder).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="📄", command=newfile).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="📊", command=info).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="📂", command=openf).pack(side=LEFT, padx=5, pady=5)
Button(buttonbar, text="🔙", command=back).pack(side=LEFT, padx=5, pady=5)

main = Frame(app, bg="#f0f0f0")
main.pack(fill=BOTH, expand=True)
main.columnconfigure(0, weight=3)
main.columnconfigure(1, weight=1)
main.rowconfigure(0, weight=1)

listbox = Listbox(main, selectmode=EXTENDED, bg="white", fg="black")
listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
listbox.bind("<<ListboxSelect>>", show)

previewbox = Frame(main, bg="lightgrey")
previewbox.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)

previewtitle = Label(previewbox, text="📄 Preview", font=("Arial", 12, "bold"), bg="lightgrey", anchor="w")
previewtitle.pack(anchor="w", padx=5, pady=(0, 5))

previewtext_frame = Frame(previewbox, bg="lightgrey")
previewtext_frame.pack(fill=BOTH, expand=True)

text_scroll = Scrollbar(previewtext_frame)
text_scroll.pack(side=RIGHT, fill=Y)

previewtext = Text(previewtext_frame, wrap=WORD, font=("Consolas", 10), bg="lightgrey", fg="black", yscrollcommand=text_scroll.set)
previewtext.pack(fill=BOTH, expand=True, padx=5, pady=5)
text_scroll.config(command=previewtext.yview)

previewimage = Label(previewbox, bg="lightgrey")
previewimage.pack()

update()
app.mainloop()

