# Importamos librerías
## Importamos Groq para acceder a SLMs mediante APIs, la elección sigue criterios económicos al tener límites gratuitos altos.
import pandas as pd
from groq import Groq
import json
import time
import os
from tqdm import tqdm

# CONFIGURACIÓN
client = Groq(api_key="") # Completar API personal desde https://console.groq.com/keys . Esto puede ser reemplazado por el LLM de esu conveniencia.
MODEL_ID = "llama-3.1-8b-instant"
ARCHIVO_IN = "oraciones_para_clasificar.csv"
ARCHIVO_OUT = "analisis_valencia_final.csv"

# LIMPIEZA
BASURA = ['newsletter', 'suscribite', 'seguinos en', 'clarín', 'la nación', 'infobae', 'leer más', 'registrate']

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

    # Lógica de reanudación en caso de interrupción
    if os.path.exists(ARCHIVO_OUT):
        df_ya_hecho = pd.read_csv(ARCHIVO_OUT, sep=';')
        ultimo_indice = len(df_ya_hecho)
        resultados = df_ya_hecho.to_dict('records')
        print(f"Reanudando desde la oración {ultimo_indice}...")
    else:
        resultados = []
        ultimo_indice = 0

    tamaño_batch = 20
    for i in tqdm(range(ultimo_indice, len(df), tamaño_batch)):
        batch = df['texto_oracion'].iloc[i:i + tamaño_batch].tolist()

        # Limpieza rápida
        res_bloque = clasificar_con_groq(batch)

        if res_bloque == "REINTENTAR":
            time.sleep(10)
            continue

        if res_bloque:
            for idx, r in enumerate(res_bloque):
                if idx < len(batch):
                    r['url_origen'] = df.iloc[i + idx]['url_origen']
                    r['texto_original'] = df.iloc[i + idx]['texto_oracion']
                    resultados.append(r)

            # Guardado
            pd.DataFrame(resultados).to_csv(ARCHIVO_OUT, index=False, sep=';', encoding='utf-8-sig')

        time.sleep(1.5)
        
if __name__ == "__main__":
    ejecutar()

