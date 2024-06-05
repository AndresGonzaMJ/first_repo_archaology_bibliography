import csv
from unidecode import unidecode
import tkinter as tk
from tkinter import messagebox, font
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
        result_window.title("Resultados de Búsqueda")
        result_window.geometry("800x600")
        result_window.configure(bg="#F0F8FF")

        title_font = ('Montserrat', 16, 'bold')
        text_font = ('Open Sans', 11)
        bold_font = ('Open Sans', 11, 'bold')

        title_label = tk.Label(result_window, text="Investigaciones Arqueológicas", font=title_font, fg='#1E88E5', bg='#F0F8FF')
        title_label.pack(pady=(20, 10))

        canvas = tk.Canvas(result_window, bg='#F0F8FF', highlightthickness=0)
        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='TFrame')

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=20)
        scrollbar.pack(side="right", fill="y")

        for resultado in resultados:
            item_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
            item_frame.pack(fill="x", pady=(0, 15), padx=10)

            content_frame = ttk.Frame(item_frame, style='CardContent.TFrame')
            content_frame.pack(fill="both", expand=True, padx=15, pady=15)

            titulo_label = ttk.Label(content_frame, text=resultado['TITULO'].strip(), font=bold_font, foreground='#1E88E5', wraplength=650, justify='left', style='CardTitle.TLabel')
            titulo_label.pack(anchor='w', pady=(0, 10))

            autor_label = ttk.Label(content_frame, text=f"Por {resultado['AUTORES'].strip()}", font=text_font, foreground='#333333', style='CardText.TLabel')
            autor_label.pack(anchor='w')

            anio_label = ttk.Label(content_frame, text=f"Año: {resultado['AÑO'].strip()}", font=text_font, foreground='#333333', style='CardText.TLabel')
            anio_label.pack(anchor='w', pady=(5, 0))

        style.configure('Card.TFrame', background='#FFFFFF', relief='solid', borderwidth=1, bordercolor='#E0E0E0')
        style.configure('CardContent.TFrame', background='#FFFFFF')
        style.configure('CardTitle.TLabel', background='#FFFFFF')
        style.configure('CardText.TLabel', background='#FFFFFF')

        style.map('Card.TFrame', 
                 background=[('active', '#FAFAFA')], 
                 relief=[('active', 'solid')], 
                 borderwidth=[('active', 1)], 
                 bordercolor=[('active', '#B0B0B0')])
    else:
        messagebox.showinfo("Resultados de Búsqueda", "No se encontraron investigaciones para el municipio solicitado.")

def pedir_datos():
    dialog = tk.Toplevel(root)
    dialog.title("Buscar Investigación")
    dialog.geometry("500x300")
    dialog.configure(bg="#F0F8FF")

    style.configure('Title.TLabel', font=('Montserrat', 16, 'bold'), foreground='#1E88E5', background='#F0F8FF')
    style.configure('Text.TLabel', font=('Segoe UI', 12), foreground='#333333', background='#F0F8FF')
    style.configure('TEntry', font=('Segoe UI', 12), fieldbackground='white')
    style.configure('TButton', font=('Segoe UI', 12, 'bold'), background='#4CAF50', foreground='white', padding=(10, 5))

    title_label = ttk.Label(dialog, text="Buscar por Ubicación", style='Title.TLabel')
    title_label.pack(pady=(20, 10))

    label = ttk.Label(dialog, text="Ingrese el nombre del departamento:", style='Text.TLabel')
    label.pack(pady=(10, 5))

    entry = ttk.Entry(dialog, width=30, style='TEntry')
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

    submit_button = ttk.Button(dialog, text="Continuar", command=on_submit_departamento, style='TButton')
    submit_button.pack(pady=(20, 10))

    entry.bind("<Return>", on_submit_departamento)
    entry.focus_set()

    root.wait_window(dialog)

def buscar():
    pedir_datos()

# Ruta del archivo CSV
ruta_archivo = r'C:\Users\pc\Desktop\MAHPSA\CHATBOT_CARIBE.csv'

# Cargar datos de la base de datos
investigaciones = cargar_datos(ruta_archivo)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Búsquedas Bibliográficas - Arqueología Caribe")
root.geometry("600x400")
root.configure(bg="#F0F8FF")

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
style.configure('TFrame', background='#F0F8FF')
style.configure('Title.TLabel', font=('Montserrat', 18, 'bold'), foreground='#1E88E5', background='#F0F8FF')
style.configure('Text.TLabel', font=('Segoe UI', 12), foreground='#333333', background='#F0F8FF')
style.configure('TButton', font=('Segoe UI', 13, 'bold'), background='#4CAF50', foreground='white', padding=(15, 10))

title_label = ttk.Label(root, text="Arqueología del Caribe Colombiano", style='Title.TLabel')
title_label.pack(pady=(50, 20))

subtitle_label = ttk.Label(root, text="Encuentre investigaciones por ubicación", style='Text.TLabel')
subtitle_label.pack()

buscar_button = ttk.Button(root, text="Iniciar Búsqueda", command=buscar, style='TButton')
buscar_button.pack(pady=40)

# Iniciar el bucle de eventos
root.mainloop()