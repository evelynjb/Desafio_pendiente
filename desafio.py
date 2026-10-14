import os
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

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

def analizar_conducta_edad(datos): #Funcion que guarda la tabla con los datos y cuando se llame realizar todo lo que esta adentro 

    tabla = pd.crosstab(datos['def_clas_edad'], #Esta funcion de pandas permite relacionar dos variables, la cunducta y la clasificacion de edad en un solo cuadro
                        datos['conducta'])

    print("-----Conducta según la edad-----")
    print(tabla)

analizar_conducta_edad(df_resultado)

#Gráfica de las aseguradoras 
def grafico_aseguradoras(datos2):  
    cantidad = datos2['aseguradora'].value_counts() #Cuenta la cantidad de aseguradoras que hay 

    plt.figure(figsize=(10,5))  #Esta parte define el tamaño del gráfico 
    plt.plot(cantidad, color="red", marker="*", markersize=10, markerfacecolor="green", markeredgecolor="blue")  #El tipo de grafico que se quiere con susu caracteristicas de punto y color de puntos
    plt.title("Aseguradoras con mayor frecuencia")
    plt.xlabel("Aseguradoras")
    plt.ylabel("Cantidad de usuarios afiliados")
    plt.grid(True, linestyle="--") #Para poner margen o cuadricula suave 

    plt.xticks(rotation = 45)  #Rota hacia un lado los datos string para que se vean presentables de acuerdo a los grados que den 
    plt.tight_layout() #Ajustan los espacios para que no se corten 
    plt.show()

grafico_aseguradoras(df_resultado) #Se llama la función 

#Gráfico del sexo
def grafico_sexo(datos3): 
    cantidad_sexo = datos3['sexo_'].value_counts() #Cuenta la cantidad de datos en sexo que se repiten 

    plt.figure(figsize=(10,5)) #El tamaño de la gráfica 
    plt.bar(cantidad_sexo.index, cantidad_sexo.values, color=["pink", "blue"]) #Funcion color con lista para que cada barra tenga un color distinto 
    plt.title("Cantidad de pacientes con su género")
    plt.xlabel("Género")
    plt.ylabel("Cantidad de usuarios")
    plt.show() #Muestra la gráfica 

grafico_sexo(df_resultado) #Se llama la función 

def diagrama_dispersion(datos):

    plt.figure(figsize=(10, 8)) #Tamaño del gráfico 
    plt.scatter(
        datos['edad_min'], #Toma los datos de la edad min
        datos['edad_max'], #Toma los datos de la edad max  
        c=datos['edad_min'],  #Asignar un color 
        cmap="plasma", #Una forma para elegir la combinación de colores 
        s=50, #Se define el tamaño de los puntos 
        alpha=0.7, #Da transparencia a los puntos 
        edgecolors="black" #Agrega borde negro a los puntos 
    )

    x = datos['edad_min']
    y = datos['edad_max']

    pendiente, intercepto = np.polyfit(x, y, 1) #Realiza un polonomio de grado 1, realizando una línea recta más ajustada 

    # Crear los puntos para dibujar la linea recta
    linea = pendiente * x + intercepto #Calcula los puntos exactos de la línea recta para cada valor de x aplicando la ecuación de la línea y=mx +b 

    # Dibujar la linea de tendencia
    plt.plot(x, linea, color="green", linewidth=2, label="Linea de tendencia")  #Caracteristicas de la línea de tendencia 

    plt.colorbar(label="Edad minima") #Crea una paleta de color que muestra los datos a partir de una colorimetría 

    plt.title("Relacion entre edad minima y maxima") 
    plt.xlabel("Edad minima") 
    plt.ylabel("Edad maxima") 

    plt.grid(True, linestyle="--", alpha=0.3) #Agrega la cuadrilla y que tan transparente será 

    plt.tight_layout() #Ajusta los espacios para que no se corten 
    plt.show() #Muestra el gráfico 

diagrama_dispersion(df) #Llamo a la función y a el dato que se se tomará para esto 

# 5. Guardar en Excel
df_resultado.to_excel('BdatosD_filtrado.xlsx', index=False)
print('\n¡Archivo Excel creado con éxito con las edades separadas y filtradas!')