import csv
from unidecode import unidecode
import tkinter as tk
from tkinter import messagebox, font

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
        
        result_text = tk.Text(result_window, wrap="word", font=("Helvetica", 12), spacing1=2, spacing2=2, spacing3=2)
        result_text.pack(expand=True, fill="both", padx=10, pady=10)

        result_text.insert("1.0", "Investigaciones arqueológicas en el municipio solicitado:\n\n")

        for resultado in resultados:
            result_text.insert(tk.END, "Título: ", "bold")
            result_text.insert(tk.END, f"{resultado['TITULO'].strip()}\n")
            result_text.insert(tk.END, "Autor: ", "bold")
            result_text.insert(tk.END, f"{resultado['AUTORES'].strip()}\n")
            result_text.insert(tk.END, "Fecha: ", "bold")
            result_text.insert(tk.END, f"{resultado['AÑO'].strip()}\n\n")

        result_text.tag_configure("bold", font=("Helvetica", 12, "bold"))
        result_text.tag_configure("justify", justify="left")

        result_text.config(state="disabled")
    else:
        messagebox.showinfo("Resultados de Búsqueda", "No se encontraron investigaciones para el municipio solicitado.")

def pedir_departamento():
    dialog = tk.Toplevel(root)
    dialog.title("Entrada")
    dialog.geometry("400x200")

    dialog_frame = tk.Frame(dialog)
    dialog_frame.place(relx=0.5, rely=0.5, anchor='center')

    label_font = font.Font(size=12, weight="bold")
    entry_font = font.Font(size=12)

    label = tk.Label(dialog_frame, text="Por favor, ingrese el nombre del departamento:", font=label_font)
    label.pack(pady=10)

    entry = tk.Entry(dialog_frame, font=entry_font)
    entry.pack(pady=10)

    def on_submit():
        dialog.departamento = entry.get()
        dialog.destroy()

    submit_button = tk.Button(dialog_frame, text="Enviar", command=on_submit, font=entry_font)
    submit_button.pack(pady=10)

    root.wait_window(dialog)
    return getattr(dialog, 'departamento', None)

def pedir_municipio():
    dialog = tk.Toplevel(root)
    dialog.title("Entrada")
    dialog.geometry("400x200")

    dialog_frame = tk.Frame(dialog)
    dialog_frame.place(relx=0.5, rely=0.5, anchor='center')

    label_font = font.Font(size=12, weight="bold")
    entry_font = font.Font(size=12)

    label = tk.Label(dialog_frame, text="Por favor, ingrese el nombre del municipio:", font=label_font)
    label.pack(pady=10)

    entry = tk.Entry(dialog_frame, font=entry_font)
    entry.pack(pady=10)

    def on_submit():
        dialog.municipio = entry.get()
        dialog.destroy()

    submit_button = tk.Button(dialog_frame, text="Enviar", command=on_submit, font=entry_font)
    submit_button.pack(pady=10)

    root.wait_window(dialog)
    return getattr(dialog, 'municipio', None)

def buscar():
    departamento = pedir_departamento()
    if departamento:
        municipio = pedir_municipio()
        if municipio:
            resultados = buscar_investigaciones(investigaciones, departamento, municipio)
            mostrar_resultados(resultados)

# Ruta del archivo CSV
ruta_archivo = r'C:\Users\pc\Desktop\MAHPSA\CHATBOT_CARIBE.csv'

# Cargar datos de la base de datos
investigaciones = cargar_datos(ruta_archivo)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Facilitador de Búsquedas Bibliográficas en Arqueología")
root.geometry("400x200")

# Centrar la ventana principal en la pantalla
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Configuración del botón de búsqueda
custom_font = font.Font(size=12, weight="bold")
buscar_button = tk.Button(root, text="Buscar Investigaciones", command=buscar, width=20, height=2, font=custom_font)

# Crear un frame para centrar el botón
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')
buscar_button.pack()

# Iniciar el bucle de eventos
root.mainloop()
