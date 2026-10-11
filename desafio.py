import os
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# NOTA: Para evitar errores, también es posible leer un archivo .csv sin transformarlo a xlsx; solo transformar en caso de ser totalmente necesario.
# 1. Leer archivo de Excel, teniendo en cuenta la ubicación en fila de las columnas donde se encuentre la información a buscar
df = pd.read_excel('BdatosD.xlsx', header=1)

# Limpiar posibles espacios en los nombres de las columnas
df.columns = df.columns.str.strip()

# 2. Tomar 50 filas
df_50 = df.head(50)

# 3. Filtrar columnas deseadas
columnas_Cn = df_50[['clasif_edad', 'def_clas_edad', 'sexo_', 'aseguradora', 'conducta']]

# 4. Imprimir resumen
print("Dimensiones:", columnas_Cn.shape)
print("\nPrimeros registros:\n", columnas_Cn.head())

# 5. Guardar en Excel
columnas_Cn.to_excel('BdatosD_filtrado.xlsx', index=False)
print("\n¡Archivo Excel creado con éxito!")