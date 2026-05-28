# Importamos librerías
## Importamos Groq para acceder a SLMs mediante APIs, la elección sigue criterios económicos al tener límites gratuitos altos.
import pandas as pd
from groq import Groq
import json
import time
import os
from tqdm import tqdm

# CONFIGURACIÓN
client = Groq(api_key=os.environ.get("GROQ_API_KEY")) # Completar API personal desde https://console.groq.com/keys .
MODEL_ID = "llama-3.1-8b-instant"
ARCHIVO_IN = "oraciones_para_clasificar.csv"
ARCHIVO_OUT = "analisis_valencia_final.csv"

# Definimos prompt base según el caso.
## Se da contexto al modelo en búsqueda de refinar el resultado, se otorgan las categorías posibles y se pide un score de confianza.
PROMPT_SISTEMA = """
Actuá como clasificador de datos JSON experto en Sociología Computacional y Tecnologías Digitales. Tu tarea es analizar la valencia de oraciones sobre tecnología.
Categorías: "positiva", "negativa", "no se identifica valencia".
REGLAS:
- 'score' debe ser un NÚMERO flotante (0.0 a 1.0). NUNCA uses palabras.
- Si la oración es publicidad o ruido, usá "no se identifica valencia" y score 0.0.
JSON format: {"resultados": [{"id": 0, "clase": "...", "score": 0.0}]}
"""

# Definimos función clasificadora.
def clasificar_con_groq(bloque_oraciones):
    texto_input = "\n".join([f"ID {i}: {txt}" for i, txt in enumerate(bloque_oraciones)])
    try:
        completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": texto_input}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        return json.loads(completion.choices[0].message.content).get('resultados', [])
    except Exception:
        return "REINTENTAR"

# Definimos función de ejecución.
def ejecutar():
    df = pd.read_csv(ARCHIVO_IN, sep=';', encoding='utf-8-sig')

    if os.path.exists(ARCHIVO_OUT):
        df_ya_hecho = pd.read_csv(ARCHIVO_OUT, sep=';')
        procesados = set(df_ya_hecho['indice_global'].dropna().astype(int).tolist())
        resultados = df_ya_hecho.to_dict('records')
        print(f"Reanudando. Ya hay {len(procesados)} oraciones clasificadas...")
    else:
        resultados = []
        procesados = set()

    tamaño_batch = 20

    for i in tqdm(range(0, len(df), tamaño_batch)):
        batch_df = df.iloc[i:i + tamaño_batch]

        batch_a_procesar = batch_df[~batch_df.index.isin(procesados)]
        if batch_a_procesar.empty:
            continue

        batch = batch_a_procesar['texto_oracion'].tolist()

        intentos = 0
        res_bloque = "REINTENTAR"
        while res_bloque == "REINTENTAR" and intentos < 5:
            res_bloque = clasificar_con_groq(batch)
            if res_bloque == "REINTENTAR":
                intentos += 1
                time.sleep(10)

        if res_bloque == "REINTENTAR":
            continue

        if res_bloque:
            for r in res_bloque:
                try:
                    llm_id = int(r.get('id'))
                    if 0 <= llm_id < len(batch_a_procesar):
                        fila_original = batch_a_procesar.iloc[llm_id]
                        # Guardamos el índice real del DataFrame original (indentación corregida)
                        r['indice_global'] = int(batch_a_procesar.index[llm_id])
                        r['url_origen'] = fila_original['url_origen']
                        r['texto_original'] = fila_original['texto_oracion']
                        resultados.append(r)
                except (ValueError, TypeError, IndexError):
                    continue
            
            # Guardado inmediato
            pd.DataFrame(resultados).to_csv(ARCHIVO_OUT, index=False, sep=';', encoding='utf-8-sig')

        time.sleep(1.5)

if __name__ == "__main__":
    ejecutar()
