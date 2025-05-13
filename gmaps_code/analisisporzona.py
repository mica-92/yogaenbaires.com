import pandas as pd
from pathlib import Path

def clasificar_por_zona(archivo_unicos="unicos_20250513_153851.csv"):
    """
    Clasifica los estudios de yoga por zonas y guarda archivos separados
    
    Args:
        archivo_unicos (str): Ruta al archivo CSV con los resultados únicos
    """
    try:
        # Cargar los datos
        df = pd.read_csv(archivo_unicos)
        
        # Verificar que exista la columna zone
        if 'zone' not in df.columns:
            raise ValueError("El archivo no contiene la columna 'zone'")
        
        # Normalizar nombres de zonas (por si hay variaciones)
        df['zone'] = df['zone'].str.lower().str.replace(' ', '').str.replace('_', '')
        
        # Definir las agrupaciones de zonas
        zonas = {
            'zonanorte': ['sanisidro2', 'sanisidro', 'vilo2', 'vilo'],
            'zonasure': ['lomas2', 'lomas'],
            'caba': ['centro', 'centro2', 'coghlan', 'coghlan2', 
                    'palermo', 'palermo2', 'caballito', 'caballito2']
        }
        
        # Crear carpeta para resultados si no existe
        Path("resultados_por_zona").mkdir(exist_ok=True)
        
        # Procesar cada zona
        for nombre_zona, subzonas in zonas.items():
            # Filtrar los registros
            mascara = df['zone'].isin(subzonas)
            df_zona = df[mascara].copy()
            
            # Guardar el archivo
            ruta_archivo = f"resultados_por_zona/{nombre_zona}.csv"
            df_zona.to_csv(ruta_archivo, index=False)
            print(f"✅ {ruta_archivo} - {len(df_zona)} registros")
            
        print("\n🗂️ Clasificación completada exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

# Ejemplo de uso
if __name__ == "__main__":
    clasificar_por_zona()