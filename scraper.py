# Importamos bibliotecas.
## Usamos "trafilatura" para scrapear. Más info. en: https://github.com/adbar/trafilatura
import trafilatura
import pandas as pd
import json

# Definimos función de scraping.
def ejecutar_escrapeo(lista_urls):
    dataset = []

    for url in lista_urls:
        print(f"Procesando: {url}")
        try:
            # Descargamos el contenido (incluye manejo básico de headers)
            descarga = trafilatura.fetch_url(url)
            resultado_raw = trafilatura.extract(descarga, output_format='json')

            if resultado_raw:
                datos = json.loads(resultado_raw)
                dataset.append({
                    'url': url,
                    'titulo': datos.get('title'),
                    'fecha': datos.get('date'),
                    'texto_completo': datos.get('text')
                })
        except Exception as e:
            print(f"Error en {url}: {e}")

    return pd.DataFrame(dataset)

mis_urls = [""] # Completar con fuentes propias.
df_articulos = ejecutar_escrapeo(mis_urls)

# Guardamos el resultado en csv.
nombre_archivo = "articulos_scrapeados.csv"

df_articulos.to_csv(nombre_archivo, index=False, encoding='utf-8-sig', sep=';')

print(f"Los datos se guardaron en: {nombre_archivo}")
