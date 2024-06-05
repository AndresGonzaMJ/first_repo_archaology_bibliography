import csv
from unidecode import unidecode

def cargar_datos(ruta_archivo):
    investigaciones = []
    with open(ruta_archivo, newline='', encoding='utf-8-sig') as csvfile:
        lector = csv.DictReader(csvfile, delimiter=';')
        for fila in lector:
            investigaciones.append(fila)
    return investigaciones

def normalizar_texto(texto):
    return unidecode(texto.strip().lower())

def buscar_investigaciones_por_departamento_y_municipio(investigaciones, departamento, municipio):
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
        print("\nInvestigaciones arqueológicas en el municipio solicitado:")
        for resultado in resultados:
            print(f"Título: {resultado['TITULO'].strip()}\nAutor: {resultado['AUTORES'].strip()}\nFecha: {resultado['AÑO'].strip()}\n")
    else:
        print("No se encontraron investigaciones para el municipio solicitado.")

def main():
    print("Bienvenido al facilitador de búsquedas bibliográficas en arqueología para la región Caribe.")
    departamento = input("Por favor, ingrese el nombre del departamento: ")
    municipio = input("Por favor, ingrese el nombre del municipio: ")
    
    # Ruta del archivo CSV
    ruta_archivo = r'C:\Users\pc\Desktop\MAHPSA\cCHATBOT_CARIBE.csv'  # <--- AQUÍ DEBES REEMPLAZAR POR LA RUTA DE TU ARCHIVO CSV
    
    # Cargar datos de la base de datos
    investigaciones = cargar_datos(ruta_archivo)
    
    # Buscar investigaciones por departamento y municipio
    resultados = buscar_investigaciones_por_departamento_y_municipio(investigaciones, departamento, municipio)
    
    # Mostrar resultados
    mostrar_resultados(resultados)

if __name__ == "__main__":
    main()
