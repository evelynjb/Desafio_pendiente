import os
import pandas as pd
import matplotlib.pyplot as plt 

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# NOTA: Para evitar errores, también es posible leer un archivo .csv sin transformarlo a xlsx; solo transformar en caso de ser totalmente necesario.
# 1. Leer archivo de Excel, teniendo en cuenta la ubicación en fila de las columnas donde se encuentre la información a buscar
df = pd.read_excel('BdatosD.xlsx', header=1)

# 2. Extraer los números de clasif_edad SIN importar el separador ("A", "Y MAS", "-", etc.)
numeros = df['clasif_edad'].str.findall(r'\d+')

nuevas_edades = pd.DataFrame({
    # El primer número es la edad mínima
    'edad_min': numeros.apply(lambda x: int(x[0]) if len(x) > 0 else None),
    # El último número es la edad máxima
    'edad_max': numeros.apply(lambda x: int(x[-1]) if len(x) > 0 else None)
})
nuevas_edades['edad_min'] = pd.to_numeric(nuevas_edades['edad_min'], errors='coerce')
nuevas_edades['edad_max'] = pd.to_numeric(nuevas_edades['edad_max'], errors='coerce')

df = pd.concat([df, nuevas_edades], axis=1)

# 3. Calcular promedio y desviación estándar
promedio_edad_min = df['edad_min'].mean()
desviacion_edad_min = df['edad_min'].std()

print("--- ANÁLISIS DE DATOS ---")
print(f"Promedio de edad mínima: {promedio_edad_min:.2f}")
print(f"Desviación estándar de edad mínima: {desviacion_edad_min:.2f}")

# 4. Filtrar las filas cuya edad mínima sea mayor o igual al promedio
df_filtrado_promedio = df[df['edad_min'] >= promedio_edad_min]

df_final = df_filtrado_promedio.head(50)

columnas_deseadas = ['clasif_edad', 'edad_min', 'edad_max', 'def_clas_edad', 'sexo_', 'aseguradora', 'conducta']
df_resultado = df_final[[c for c in columnas_deseadas if c in df_final.columns]]

# Contar cuántas personas hay en cada tipo de conducta
print("\n--- CONTEO POR CONDUCTA ---")
print(df_resultado['conducta'].value_counts())

#Gráfica de las aseguradoras 
def grafico_aseguradoras(datos):
    cantidad = datos['aseguradora'].value_counts()#Cuenta la cantidad de aseguradoras que hay 

    plt.figure(figsize=(10,5))  #Esta parte define el tamaño del gráfico 
    plt.plot(cantidad, color="red", marker="*", markersize=10, markerfacecolor="green", markeredgecolor="blue")  #El tipo de grafico que se quiere con susu caracteristicas de punto y color de puntos
    plt.title("Aseguradoras con mayor frecuencia")
    plt.xlabel("Aseguradoras")
    plt.ylabel("Cantidad de usuarios afiliados")

    plt.xticks(rotation = 45) 
    plt.tight_layout()
    plt.show()

grafico_aseguradoras(df_resultado) #Se llama la función 

#Gráfico del sexo
def grafico_sexo(datos2): 
    cantidad_sexo = datos2['sexo_'].value_counts() #Cuenta la cantidad de datos en sexo que se repiten 

    plt.figure(figsize=(10,5)) #El tamaño de la gráfica 
    plt.bar(cantidad_sexo.index, cantidad_sexo.values, color=["pink", "blue"]) #Funcion color con lista para que cada barra tenga un color distinto 
    plt.title("Cantidad de pacientes con su género")
    plt.xlabel("Género")
    plt.ylabel("Cantidad de usuarios")
    plt.show() #Muestra la gráfica 

grafico_sexo(df_resultado) #Se llama la función 

# 5. Guardar en Excel
df_resultado.to_excel('BdatosD_filtrado.xlsx', index=False)
print('\n¡Archivo Excel creado con éxito con las edades separadas y filtradas!')