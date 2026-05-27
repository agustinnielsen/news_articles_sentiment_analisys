import pandas as pd
import nltk
import os
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("📥 Descargando recursos necesarios de NLTK...")
nltk.download('punkt')
nltk.download('punkt_tab')

def procesar_csv_a_oraciones(archivo_entrada, archivo_salida):
    if not os.path.exists(archivo_entrada):
        print(f"❌ Error: No se encontró el archivo {archivo_entrada}")
        return

    print(f"📖 Leyendo artículos desde {archivo_entrada}...")

    # 2. Leemos el CSV
    df_articulos = pd.read_csv(
        archivo_entrada,
        sep=';',
        encoding='utf-8-sig'
    )

    # Limpiamos filas que puedan estar vacías por error
    df_articulos = df_articulos.dropna(subset=['texto_completo'])

    filas_oraciones = []

    print("✂️ Segmentando textos en oraciones...")
    for _, fila in df_articulos.iterrows():
        # Segmentación por idioma español
        oraciones = nltk.sent_tokenize(str(fila['texto_completo']), language='spanish')

        for i, oracion in enumerate(oraciones):
            # Limpieza básica
            texto_limpio = oracion.replace('\n', ' ').strip()

            # Solo guardamos oraciones con una longitud mínima de 10 caracteres.
            if len(texto_limpio) > 10:
                filas_oraciones.append({
                    'url_origen': fila['url'],
                    'nro_oracion': i,
                    'texto_oracion': texto_limpio
                })

    # 3. Creamos el nuevo DataFrame de oraciones
    df_oraciones = pd.DataFrame(filas_oraciones)

    # 4. Guardamos el resultado
    df_oraciones.to_csv(archivo_salida, index=False, encoding='utf-8-sig', sep=';')

    print(f"✅ ¡Proceso terminado!")
    print(f"📊 De {len(df_articulos)} artículos generamos {len(df_oraciones)} oraciones.")
    print(f"💾 Archivo guardado como: {archivo_salida}")


#EJECUCIÓN
archivo_input = "articulos_scrapeados.csv"
archivo_output = "oraciones_para_clasificar.csv"

procesar_csv_a_oraciones(archivo_input, archivo_output)