import csv
from unidecode import unidecode
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

def cargar_datos(ruta_archivo):
    investigaciones = []
    with open(ruta_archivo, newline='', encoding='utf-8-sig') as csvfile:
        lector = csv.DictReader(csvfile, delimiter=';')
        for fila in lector:
            investigaciones.append(fila)
    return investigaciones

def normalizar_texto(texto):
    return unidecode(texto.strip().lower())

def buscar_investigaciones(investigaciones, departamento, municipio):
    departamento_normalizado = normalizar_texto(departamento)
    municipio_normalizado = normalizar_texto(municipio)
    resultados = []
    for investigacion in investigaciones:
        if (normalizar_texto(investigacion['DEPARTAMENTO']) == departamento_normalizado and 
            normalizar_texto(investigacion['MUNICIPIO']) == municipio_normalizado):
            resultados.append(investigacion)
    return resultados

def mostrar_resultados(resultados):
    if not resultados:
        messagebox.showinfo("Resultados de Búsqueda", "No se encontraron investigaciones, verifique el nombre del departamento o municipio.")
        mostrar_bienvenida()
        return

    result_window = tk.Toplevel(root)
    result_window.title("Investigaciones encontradas")
    result_window.geometry("1200x700")
    center_window(result_window, 1200, 700)
    result_window.configure(bg=COLORS['cornsilk']['DEFAULT'])

    canvas = tk.Canvas(result_window, bg=COLORS['cornsilk']['DEFAULT'], highlightthickness=0)
    scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=canvas.yview, style='Custom.Vertical.TScrollbar')
    scrollable_frame = ttk.Frame(canvas, style='Result.TFrame')

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=20)
    scrollbar.pack(side="right", fill="y")

    result_window.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    style.configure('Result.TFrame', background=COLORS['cornsilk']['DEFAULT'])
    style.configure('Card.TFrame', background='white', relief='solid', borderwidth=1, bordercolor=COLORS['tea_green']['DEFAULT'])
    style.configure('CardContent.TFrame', background='white')
    style.configure('CardTitle.TLabel', font=('Montserrat', 14, 'bold'), foreground=COLORS['buff']['800'], background='white')
    style.configure('CardText.TLabel', font=('Segoe UI', 11), foreground=COLORS['tea_green']['200'], background='white')
    style.configure('CardBold.TLabel', font=('Segoe UI', 11, 'bold'), foreground=COLORS['tea_green']['200'], background='white')

    style.map('Card.TFrame', 
             background=[('active', COLORS['cornsilk']['200'])], 
             relief=[('active', 'solid')], 
             borderwidth=[('active', 1)], 
             bordercolor=[('active', COLORS['buff']['DEFAULT'])])

    for resultado in resultados:
        item_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        item_frame.pack(fill="x", pady=(0, 15), padx=10)

        content_frame = ttk.Frame(item_frame, style='CardContent.TFrame')
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)

        titulo_text = tk.Text(content_frame, wrap='word', font=('Montserrat', 13, 'bold'), foreground=COLORS['buff']['800'], bg='white', height=2, borderwidth=0)
        titulo_text.insert(tk.END, resultado['TITULO'].strip())
        titulo_text.config(state=tk.DISABLED)
        titulo_text.pack(anchor='w', pady=(0, 10), fill='x')

        autor_text = tk.Text(content_frame, wrap='word', font=('Segoe UI', 11, 'bold'), foreground=COLORS['tea_green']['200'], bg='white', height=1, borderwidth=0)
        autor_text.insert(tk.END, "Autor: " + resultado['AUTORES'].strip())
        autor_text.config(state=tk.DISABLED)
        autor_text.pack(anchor='w', fill='x')

        anio_text = tk.Text(content_frame, wrap='word', font=('Segoe UI', 11, 'bold'), foreground=COLORS['tea_green']['200'], bg='white', height=1, borderwidth=0)
        anio_text.insert(tk.END, "Año: " + resultado['AÑO'].strip())
        anio_text.config(state=tk.DISABLED)
        anio_text.pack(anchor='w', pady=(5, 0), fill='x')

    sali_image_path = r"C:\Users\pc\Desktop\MAHPSA\images\sali.png"
    sali_image = Image.open(sali_image_path)
    sali_image = sali_image.resize((340, 180), Image.LANCZOS)
    sali_photo = ImageTk.PhotoImage(sali_image)
    sali_image_label = tk.Label(result_window, image=sali_photo, bg=COLORS['cornsilk']['DEFAULT'])
    sali_image_label.image = sali_photo
    sali_image_label.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=20)

    home_button = ttk.Button(result_window, text="Inicio", command=mostrar_bienvenida, style='Dialog.TButton')
    home_button.place(relx=1.0, rely=0.0, anchor='ne', x=-110, y=210)

def pedir_datos():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Buscar por Ubicación")
    root.geometry("500x300")
    center_window(root, 500, 300)
    root.configure(bg=COLORS['papaya_whip']['DEFAULT'])

    style.configure('Dialog.TFrame', background=COLORS['papaya_whip']['DEFAULT'])
    style.configure('Dialog.TLabel', font=('Montserrat', 14), foreground=COLORS['buff']['800'], background=COLORS['papaya_whip']['DEFAULT'])
    style.configure('Dialog.TEntry', font=('Segoe UI', 12), fieldbackground='white')
    style.configure('Dialog.TButton', font=('Segoe UI', 13, 'bold'), background=COLORS['cornsilk']['200'], foreground=COLORS['buff']['800'], padding=(15, 10))

    style.map('Dialog.TButton',
             background=[('active', COLORS['cornsilk']['300']), ('pressed', COLORS['cornsilk']['200'])],
             foreground=[('active', 'white'), ('pressed', COLORS['buff']['800'])])

    back_button = ttk.Button(root, text="← Volver", command=mostrar_bienvenida, style='Back.TButton')
    back_button.place(relx=0.0, rely=0.0, anchor='nw', x=10, y=10)
    style.configure('Back.TButton', font=('Segoe UI', 12, 'bold'), background=COLORS['cornsilk']['200'], foreground=COLORS['buff']['800'], padding=(1, 1))

    dialog_frame = ttk.Frame(root, style='Dialog.TFrame', padding="20 20 20 20")
    dialog_frame.place(relx=0.5, rely=0.7, anchor='center')

    label = ttk.Label(dialog_frame, text="Ingrese el nombre del departamento:", style='Dialog.TLabel')
    label.pack(pady=(0, 10))

    entry = ttk.Entry(dialog_frame, width=30, style='Dialog.TEntry')
    entry.pack()

    def on_submit_departamento(event=None):
        departamento = entry.get()
        label.config(text="Ingrese el nombre del municipio:")
        entry.delete(0, tk.END)
        submit_button.config(command=lambda: on_submit_municipio(departamento), text="Buscar")
        entry.bind("<Return>", lambda event: on_submit_municipio(departamento))

    def on_submit_municipio(departamento, event=None):
        municipio = entry.get()
        resultados = buscar_investigaciones(investigaciones, departamento, municipio)
        mostrar_resultados(resultados)

    submit_button = ttk.Button(dialog_frame, text="Continuar", command=on_submit_departamento, style='Dialog.TButton')
    submit_button.pack(pady=(20, 0))

    entry.bind("<Return>", on_submit_departamento)
    entry.focus_set()

    dialog_image_path = r"C:\Users\pc\Desktop\MAHPSA\images\depar.png"
    dialog_image = Image.open(dialog_image_path)
    dialog_image = dialog_image.resize((200, 120), Image.LANCZOS)
    dialog_photo = ImageTk.PhotoImage(dialog_image)
    dialog_image_label = tk.Label(root, image=dialog_photo, bg=COLORS['papaya_whip']['DEFAULT'])
    dialog_image_label.image = dialog_photo
    dialog_image_label.place(relx=0.5, rely=0.0, anchor='n', y=10)

def mostrar_bienvenida():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Arqueología del Caribe colombiano")
    root.geometry("600x400")
    center_window(root, 600, 400)
    root.configure(bg=COLORS['papaya_whip']['DEFAULT'])

    title_label = ttk.Label(root, text="Arqueología del Caribe colombiano", style='Title.TLabel')
    title_label.pack(pady=(50, 20))

    subtitle_label = ttk.Label(root, text="Encuentre investigaciones por ubicación", style='Text.TLabel')
    subtitle_label.pack()

    buscar_button = ttk.Button(root, text="Iniciar búsqueda", command=pedir_datos, style='TButton')
    buscar_button.pack(pady=20)

    credit_label = ttk.Label(root, text="Desarrollado por Andrés González", style='Credit.TLabel')
    credit_label.place(relx=0.5, rely=0.9, anchor='s')

    image_path = r"C:\Users\pc\Desktop\MAHPSA\images\Pieza arqueologica@2x.png"
    image = Image.open(image_path)
    image = image.resize((130, 260), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=photo, bg=COLORS['papaya_whip']['DEFAULT'])
    image_label.image = photo
    image_label.place(relx=0.0, rely=1.0, anchor='sw', x=20, y=-20)

    image_inverted = image.transpose(Image.FLIP_LEFT_RIGHT)
    photo_inverted = ImageTk.PhotoImage(image_inverted)
    image_label_right = tk.Label(root, image=photo_inverted, bg=COLORS['papaya_whip']['DEFAULT'])
    image_label_right.image = photo_inverted
    image_label_right.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x}+{y}')

COLORS = {
    'tea_green': { 'DEFAULT': '#ccd5ae', '200': '#5b6635' },
    'beige': { 'DEFAULT': '#e9edc9' },
    'cornsilk': { 'DEFAULT': '#fefae0', '200': '#faf3dd', '300': '#f2e5b8', '400': '#fbeb84' },
    'papaya_whip': { 'DEFAULT': '#faedcd' },
    'buff': { 'DEFAULT': '#d4a373', '800': '#4d2c0d' }
}

ruta_archivo = r'C:\Users\pc\Desktop\MAHPSA\CHATBOT_CARIBE.csv'
investigaciones = cargar_datos(ruta_archivo)
root = tk.Tk()

style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=COLORS['papaya_whip']['DEFAULT'])
style.configure('Title.TLabel', font=('Montserrat', 18, 'bold'), foreground=COLORS['buff']['800'], background=COLORS['papaya_whip']['DEFAULT'])
style.configure('Text.TLabel', font=('Segoe UI', 12), foreground=COLORS['tea_green']['200'], background=COLORS['papaya_whip']['DEFAULT'])
style.configure('TButton', font=('Segoe UI', 13, 'bold'), background=COLORS['cornsilk']['200'], foreground=COLORS['buff']['800'], padding=(15, 10))
style.configure('Credit.TLabel', font=('Segoe UI', 10, 'italic'), foreground=COLORS['tea_green']['200'], background=COLORS['papaya_whip']['DEFAULT'])

style.map('TButton',
         background=[('active', COLORS['cornsilk']['300']), ('pressed', COLORS['cornsilk']['200'])],
         foreground=[('active', 'white'), ('pressed', COLORS['buff']['800'])])

# Estilo moderno para scrollbar
style.element_create('Custom.Vertical.TScrollbar.trough', 'from', 'clam')
style.layout('Custom.Vertical.TScrollbar',
             [('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'unit': 1, 'children': [('Vertical.Scrollbar.grip', {'sticky': ''})], 'sticky': 'nswe'})], 'sticky': 'ns'})])
style.configure('Custom.Vertical.TScrollbar', troughcolor=COLORS['beige']['DEFAULT'], background=COLORS['buff']['DEFAULT'], darkcolor=COLORS['buff']['800'], lightcolor=COLORS['buff']['DEFAULT'])

mostrar_bienvenida()

root.mainloop()
