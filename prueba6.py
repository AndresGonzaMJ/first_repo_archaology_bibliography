import csv
from unidecode import unidecode
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
    if resultados:
        result_window = tk.Toplevel(root)
        result_window.title("Investigaciones encontradas")
        result_window.geometry("800x600")
        result_window.configure(bg=COLORS['cornsilk']['DEFAULT'])

        canvas = tk.Canvas(result_window, bg=COLORS['cornsilk']['DEFAULT'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Result.TFrame')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=20)
        scrollbar.pack(side="right", fill="y")

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

            titulo_label = ttk.Label(content_frame, text=resultado['TITULO'].strip(), font=('Montserrat', 13, 'bold'), foreground=COLORS['buff']['800'], wraplength=650, justify='left', style='CardTitle.TLabel')
            titulo_label.pack(anchor='w', pady=(0, 10))

            autor_label = ttk.Label(content_frame, text="Autor:", font=('Segoe UI', 11, 'bold'), foreground=COLORS['tea_green']['200'], style='CardBold.TLabel')
            autor_label.pack(anchor='w')
            autor_value_label = ttk.Label(content_frame, text=resultado['AUTORES'].strip(), font=('Segoe UI', 11), foreground=COLORS['tea_green']['200'], style='CardText.TLabel')
            autor_value_label.pack(anchor='w')

            anio_label = ttk.Label(content_frame, text="Año:", font=('Segoe UI', 11, 'bold'), foreground=COLORS['tea_green']['200'], style='CardBold.TLabel')
            anio_label.pack(anchor='w')
            anio_value_label = ttk.Label(content_frame, text=resultado['AÑO'].strip(), font=('Segoe UI', 11), foreground=COLORS['tea_green']['200'], style='CardText.TLabel')
            anio_value_label.pack(anchor='w', pady=(5, 0))

    else:
        messagebox.showinfo("Resultados de Búsqueda", "No se encontraron investigaciones para el municipio solicitado.")

def pedir_datos():
    dialog = tk.Toplevel(root)
    dialog.title("Buscar por Ubicación")
    dialog.geometry("500x300")
    dialog.configure(bg=COLORS['papaya_whip']['DEFAULT'])

    style.configure('Dialog.TFrame', background=COLORS['papaya_whip']['DEFAULT'])
    style.configure('Dialog.TLabel', font=('Montserrat', 14), foreground=COLORS['buff']['800'], background=COLORS['papaya_whip']['DEFAULT'])
    style.configure('Dialog.TEntry', font=('Segoe UI', 12), fieldbackground='white')
    style.configure('Dialog.TButton', font=('Segoe UI', 13, 'bold'), background=COLORS['cornsilk']['200'], foreground=COLORS['buff']['800'], padding=(15, 10))

    style.map('Dialog.TButton',
             background=[('active', COLORS['cornsilk']['300']), ('pressed', COLORS['cornsilk']['200'])],
             foreground=[('active', 'white'), ('pressed', COLORS['buff']['800'])])

    dialog_frame = ttk.Frame(dialog, style='Dialog.TFrame', padding="20 20 20 20")
    dialog_frame.place(relx=0.5, rely=0.5, anchor='center')

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
        dialog.destroy()
        resultados = buscar_investigaciones(investigaciones, departamento, municipio)
        mostrar_resultados(resultados)

    submit_button = ttk.Button(dialog_frame, text="Continuar", command=on_submit_departamento, style='Dialog.TButton')
    submit_button.pack(pady=(20, 0))

    entry.bind("<Return>", on_submit_departamento)
    entry.focus_set()

    root.wait_window(dialog)

def buscar():
    pedir_datos()

COLORS = {
    'tea_green': { 'DEFAULT': '#ccd5ae', '200': '#5b6635' },
    'beige': { 'DEFAULT': '#e9edc9' },
    'cornsilk': { 'DEFAULT': '#fefae0', '200': '#faf3dd', '300': '#f2e5b8', '400': '#fbeb84' },
    'papaya_whip': { 'DEFAULT': '#faedcd' },
    'buff': { 'DEFAULT': '#d4a373', '800': '#4d2c0d' }
}

# Ruta del archivo CSV
ruta_archivo = r'C:\Users\pc\Desktop\MAHPSA\CHATBOT_CARIBE.csv'

# Cargar datos de la base de datos
investigaciones = cargar_datos(ruta_archivo)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Arqueología del Caribe colombiano")
root.geometry("600x400")
root.configure(bg=COLORS['papaya_whip']['DEFAULT'])

# Centrar la ventana principal en la pantalla
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Aplicar estilos modernos
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=COLORS['papaya_whip']['DEFAULT'])
style.configure('Title.TLabel', font=('Montserrat', 18, 'bold'), foreground=COLORS['buff']['800'], background=COLORS['papaya_whip']['DEFAULT'])
style.configure('Text.TLabel', font=('Segoe UI', 12), foreground=COLORS['tea_green']['200'], background=COLORS['papaya_whip']['DEFAULT'])
style.configure('TButton', font=('Segoe UI', 13, 'bold'), background=COLORS['cornsilk']['200'], foreground=COLORS['buff']['800'], padding=(15, 10))

style.map('TButton',
         background=[('active', COLORS['cornsilk']['300']), ('pressed', COLORS['cornsilk']['200'])],
         foreground=[('active', 'white'), ('pressed', COLORS['buff']['800'])])

title_label = ttk.Label(root, text="Arqueología del Caribe colombiano", style='Title.TLabel')
title_label.pack(pady=(50, 20))

subtitle_label = ttk.Label(root, text="Encuentre investigaciones por ubicación", style='Text.TLabel')
subtitle_label.pack()

buscar_button = ttk.Button(root, text="Iniciar búsqueda", command=buscar, style='TButton')
buscar_button.pack(pady=40)

# Iniciar el bucle de eventos
root.mainloop()
