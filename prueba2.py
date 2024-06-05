import csv
from unidecode import unidecode

def cargar_datos(ruta_archivo):
    investigaciones = []
    with open(ruta_archivo, newline='', encoding='utf-8-sig') as csvfile:  # Utilizando 'utf-8-sig' para manejar BOM
        lector = csv.DictReader(csvfile, delimiter=';')
        for fila in lector:
            investigaciones.append(fila)
    return investigaciones

def normalizar_texto(texto):
    return unidecode(texto.strip().lower())

def buscar_investigaciones_por_municipio(investigaciones, municipio):
    municipio_normalizado = normalizar_texto(municipio)
    resultados = []
    for investigacion in investigaciones:
        if normalizar_texto(investigacion['MUNICIPIO']) == municipio_normalizado:
            resultados.append(investigacion)
    return resultados

def mostrar_resultados(resultados):
    if resultados:
        print("\nInvestigaciones arqueológicas en el municipio solicitado:")
        for resultado in resultados:
            print(f"Título: {resultado['TITULO'].strip()}\nAutor: {resultado['AUTORES'].strip()}\nFecha: {resultado['AÑO'].strip()}\n")
    else:
        print("No se encontraron investigaciones para el municipio solicitado.")

def main():
    print("Bienvenido al Facilitador de Búsquedas Bibliográficas en Arqueología para el Departamento de Córdoba.")
    municipio = input("Por favor, ingrese el nombre del municipio: ")
    
    # Ruta del archivo CSV
    ruta_archivo = r'C:\Users\pc\Desktop\MAHPSA\chat_bot.csv'  # <--- AQUÍ DEBES REEMPLAZAR POR LA RUTA DE TU ARCHIVO CSV
    
    # Cargar datos de la base de datos
    investigaciones = cargar_datos(ruta_archivo)
    
    # Buscar investigaciones por municipio
    resultados = buscar_investigaciones_por_municipio(investigaciones, municipio)
    
    # Mostrar resultados
    mostrar_resultados(resultados)

if __name__ == "__main__":
    main()
