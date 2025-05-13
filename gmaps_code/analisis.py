import os
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np

def consolidar_yoga_studios(carpeta_resultados="Resultados", tolerancia=0.0001):
    """
    Versión completamente renovada que soluciona el problema de indexación
    """
    try:
        # 1. Configuración inicial
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        columnas_requeridas = ["name", "address", "lat", "lng", "zone"]
        
        # 2. Cargar y combinar archivos
        print("\n📂 Cargando archivos...")
        archivos = [f for f in Path(carpeta_resultados).glob("*.csv") if f.is_file()]
        
        if not archivos:
            print("❌ No se encontraron archivos CSV")
            return

        datos_combinados = []
        for archivo in archivos:
            try:
                df = pd.read_csv(archivo)
                # Asegurar las columnas requeridas
                for col in columnas_requeridas:
                    if col not in df.columns:
                        df[col] = np.nan
                datos_combinados.append(df[columnas_requeridas])
                print(f"✅ {archivo.name} - {len(df)} registros")
            except Exception as e:
                print(f"⚠️ Error en {archivo.name}: {str(e)}")
                continue

        if not datos_combinados:
            print("❌ No hay datos válidos para procesar")
            return

        df_completo = pd.concat(datos_combinados, ignore_index=True)
        print(f"\n📊 Total registros consolidados: {len(df_completo)}")

        # 3. Eliminar duplicados exactos
        df_sin_duplicados = df_completo.drop_duplicates(
            subset=["name", "lat", "lng"],
            keep="first"
        ).reset_index(drop=True)
        print(f"🔍 Registros únicos (exactos): {len(df_sin_duplicados)}")

        # 4. Identificar duplicados por proximidad (nuevo método)
        print("\n🔎 Identificando duplicados por proximidad...")
        df_sin_duplicados = df_sin_duplicados.sort_values(by=["lat", "lng"])
        
        # Marcar duplicados usando un método más seguro
        duplicados_mask = [False] * len(df_sin_duplicados)
        
        for i in range(1, len(df_sin_duplicados)):
            lat_prev = df_sin_duplicados.at[i-1, "lat"]
            lng_prev = df_sin_duplicados.at[i-1, "lng"]
            lat_curr = df_sin_duplicados.at[i, "lat"]
            lng_curr = df_sin_duplicados.at[i, "lng"]
            
            if (abs(lat_curr - lat_prev) <= tolerancia and 
                abs(lng_curr - lng_prev) <= tolerancia):
                duplicados_mask[i] = True

        # 5. Separar y guardar resultados
        df_final = df_sin_duplicados[~pd.Series(duplicados_mask)]
        df_duplicados = df_sin_duplicados[pd.Series(duplicados_mask)]
        
        # Generar nombres de archivo
        archivos_salida = {
            f"consolidado_{timestamp}.csv": df_completo,
            f"unicos_{timestamp}.csv": df_final,
            f"duplicados_{timestamp}.csv": df_duplicados
        }

        print("\n💾 Guardando resultados...")
        for nombre, df in archivos_salida.items():
            df.to_csv(nombre, index=False)
            print(f"- {nombre}: {len(df)} registros")

        print(f"\n✅ Proceso completado exitosamente!")
        print(f"✔ Registros únicos finales: {len(df_final)}")
        print(f"✔ Duplicados detectados: {len(df_duplicados)}")

    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        raise

if __name__ == "__main__":
    consolidar_yoga_studios(carpeta_resultados="Resultados")