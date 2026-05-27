import trafilatura
import pandas as pd
import json

def ejecutar_escrapeo_senior(lista_urls):
    dataset = []

    for url in lista_urls:
        print(f"🔍 Procesando: {url}")
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
            print(f"❌ Error en {url}: {e}")

    return pd.DataFrame(dataset)

mis_urls = ["https://www.infobae.com/movant/2025/09/11/puertos-en-transformacion-lo-que-la-ia-puede-y-no-puede-hacer/",
            "https://www.infobae.com/tecno/2025/09/07/warner-bros-demanda-a-midjourney-por-imagenes-ia-de-superman-batman-y-otros-personajes/",
            "https://www.infobae.com/tecno/2025/09/08/la-ia-ya-esta-cambiando-el-empleo-empresa-elimino-4000-puestos-para-darle-trabajo-a-esta-tecnologia/",
            "https://www.clarin.com/viva/nuevo-redes-sociales-cuidar-ancianos-mostrar_0_w3yZtXbnmF.html",
            "https://www.clarin.com/opinion/inteligencia-artificial-revolucion-conductas-predictivas_0_BlX2Z2Hv4z.html",
            "https://www.pagina12.com.ar/743345-el-no-volvio-a-ser-el-pibe-que-estaba-en-casa",
            "https://www.infobae.com/salud/2024/06/11/los-riesgos-y-los-desafios-del-uso-de-la-inteligencia-artificial-en-salud-mental/",
            "https://www.lanacion.com.ar/tecnologia/x-extiende-la-opcion-de-ocultar-la-pestana-de-me-gusta-del-perfil-para-todos-los-usuarios-ya-no-sera-nid13062024/",
            "https://www.infobae.com/wapo/2024/06/19/los-empleados-de-la-generacion-z-estan-redescubriendo-las-habilidades-interpersonales-en-la-era-de-la-ia/",
            "https://www.infobae.com/salud/2024/06/18/las-redes-sociales-moldean-la-salud-mental-en-la-infancia-8-recomendaciones-para-padres/",
            "https://www.lanacion.com.ar/tecnologia/estados-unidos-prohibio-en-su-pais-a-la-empresa-de-ciberseguridad-kaspersky-de-origen-ruso-nid21062024/",
            "https://www.eldiarioar.com/sociedad/juicio-sharenting-familias-enfrentadas-compartir-fotos-infantiles-internet_1_11471773.html",
            "https://www.eldiarioar.com/sociedad/tipos-problema-democracia-influencers-informacion-sean-hombres_129_11470679.html",
            "https://www.infobae.com/estados-unidos/2024/06/21/nueva-york-firmo-ley-para-que-padres-controlen-contenido-de-redes-sociales-de-sus-hijos/",
            "https://www.clarin.com/tecnologia/apagon-informatico-grande-historia-sabe-caida-mundial-microsoft_0_RjCF2paDlE.html",
            "https://www.clarin.com/tecnologia/hace-crowdstrike-empresa-software-detras-caida-mundial-microsoft_0_I7GekkFzG7.html",
            "https://www.clarin.com/tecnologia/caida-microsoft-solucion-temporal-evitar-pantalla-azul-muerte_0_q0XqvfDT9S.html",
            "https://www.clarin.com/tecnologia/crowdstrike-caida-global-microsoft-impacto-forma-masiva-argentina_0_OvUfUM3xiz.html",
            "https://www.clarin.com/viva/inteligencia-artificial-puede-peligro-democracia_0_7gyRVNs3Ui.html",
            "https://www.clarin.com/opinion/desafios-superinteligencia-artificial_0_Siwyrt1Tsk.html",
            "https://www.clarin.com/buena-vida/filtros-agujas-inteligencia-artificial-disena-cara_0_JmJrjmw0A8.html",
            "https://www.clarin.com/economia/ahora-compartimos-noticias-whatsapp_0_q8AbR2xTL3.html",
            "https://www.clarin.com/informacion-general/buscar-ayuda-caso-ciberbullying_0_d3NBTgfCRg.html",
            "https://www.clarin.com/tecnologia/crowdstrike-revelan-causa-error-provoco-caida-mundial-microsoft_0_gFYlmuIC3Y.html",
            "https://www.clarin.com/cultura/inteligencia-artificial-ayuda-escribir-mejor-adormece-creatividad-humana_0_lsXifxqVEa.html",
            "https://www.eldiarioar.com/sociedad/ibai-llanos-cinco-anos-veo-vida-tranquila-fuera-foco-mediatico_1_11512295.html",
            "https://www.eldiarioar.com/sociedad/acciones-forzadas-sentimiento-culpa-promueven-adicciones-digitales-extraer-datos-personales_1_11515373.html",
            "https://www.ambito.com/tecnologia/la-union-europea-considera-que-x-engana-sus-usuarios-y-elon-musk-podria-enfrentarse-una-multa-millonaria-n6030557",
            "https://www.lanacion.com.ar/economia/negocios/la-revolucion-de-la-ia-generativa-en-la-gestion-del-talento-nid15072024/",
            "https://www.clarin.com/tecnologia/def-32-ia-alimenta-incertidumbre-laboral-sector-tech-envenena-gente-sinsentidos_0_NmeXjRqikF.html",
            "https://www.clarin.com/internacional/puede-uso-tablets-provocar-rabietas-ninos-dice-nuevo-estudio_0_qkqss5QyxU.html",
            "https://www.infobae.com/tecno/2024/08/23/cual-es-el-futuro-de-los-programadores-con-la-ia-ceo-de-aws-lo-revela/",
            "https://www.infobae.com/tendencias/2024/08/20/el-fuerte-impacto-de-la-ia-en-la-vida-emocional-y-las-relaciones/",
            "https://www.infobae.com/tecno/2024/08/16/aumentan-las-fotos-sexuales-de-ninos-manipuladas-por-ia-como-enfrentar-a-los-depredadores/",
            "https://www.clarin.com/cultura/ia-inmiscuye-publicaciones-cientificas-resultado-catastrofico_0_arsvgbbbuv.html",
            "https://www.lanacion.com.ar/tecnologia/como-ocultar-meta-ia-y-las-cinco-razones-por-las-que-hay-que-hacerlo-nid27082024/",
            "https://www.lanacion.com.ar/tecnologia/por-que-recomiendan-desactivar-meta-ai-de-whatsapp-y-como-hacerlo-nid23082024/",
            "https://www.lanacion.com.ar/tecnologia/logran-usar-adn-como-si-fuera-una-computadora-para-almacenar-y-editar-datos-nid23082024/",
            "https://www.lanacion.com.ar/el-mundo/en-guerra-con-un-juez-de-la-corte-elon-musk-anuncia-el-cierre-de-las-operaciones-de-x-en-brasil-nid17082024/",
            "https://www.ambito.com/tecnologia/la-infancia-como-usarla-aprender-que-se-vuelva-adictiva-n6050262",
            "https://www.lanacion.com.ar/tecnologia/por-que-la-inteligencia-artificial-nos-podria-llevar-a-un-colapso-energetico-nid18082024/",
            "https://www.lanacion.com.ar/estados-unidos/illinois/nueva-ley-de-illinois-regula-el-uso-de-inteligencia-artificial-en-las-busquedas-laborales-en-que-nid16082024/",
            "https://www.lanacion.com.ar/agencias/x-edita-chatbot-de-inteligencia-artificial-tras-advertencias-de-que-propaga-desinformacion-electoral-nid26082024/",
            "https://www.infobae.com/tecno/2024/09/03/que-son-las-redes-sociales-blancas-y-por-que-es-la-opcion-privada-de-instagram-y-facebook/",
            "https://www.tiempoar.com.ar/ta_article/para-que-lado-sopla-el-viento/",
            "https://www.eldiarioar.com/sociedad/oms-advirtio-fuerte-aumento-problematico-redes-sociales-adolescentes_1_11679851.html",
            "https://www.eldiarioar.com/tecnologia/abandonar-twitter-x-elon-musk_1_11656638.html",
            "https://www.infobae.com/tecno/2025/09/03/tecnologia-al-rescate-de-padres-las-mejores-aplicaciones-para-ayudar-a-dormir-a-los-bebes/",
            "https://www.infobae.com/tecno/2025/09/04/navegadores-con-ia-el-nuevo-blanco-de-ciberataques-invisibles/",
            "https://www.infobae.com/tecno/2025/09/05/trabajos-ante-la-pantalla-en-jaque-la-inteligencia-artificial-acelera-los-cambios-pero-el-valor-humano-persiste/",
            "https://www.infobae.com/espana/2025/09/05/el-silencio-digital-lo-que-la-psicologia-revela-de-quienes-no-publican-en-redes-sociales-ni-responden-en-grupos-de-whatsapp/",
            "https://www.infobae.com/salud/2025/09/16/el-futuro-de-la-medicina-ante-la-inteligencia-artificial-mitos-y-realidades/",
            "https://www.infobae.com/salud/2025/09/11/la-inteligencia-artificial-redefine-el-diagnostico-medico-pero-expertos-alertan-sobre-riesgos/",
            "https://www.infobae.com/tecno/2025/09/13/la-brecha-entre-la-promesa-de-la-inteligencia-artificial-y-la-realidad-empresarial-en-estados-unidos/",
            "https://www.infobae.com/peru/2025/09/10/el-estado-de-la-adopcion-de-la-ia-en-los-negocios-oportunidades-obstaculos-y-proximos-pasos/",
            "https://www.infobae.com/opinion/2025/09/10/declaracion-de-uso-de-iagen-necesidad-o-formalidad-sin-sentido/",
            "https://www.infobae.com/tecno/2025/09/10/esta-es-la-primera-pelicula-animada-hecha-100-con-ia-y-respaldada-por-openai/",
            "https://www.infobae.com/opinion/2025/09/11/humanidad-e-inteligencia-artificial-futuros-posibles/",
            "https://www.infobae.com/tecno/2025/09/11/el-trafico-de-bots-supera-al-humano-en-internet-por-primera-vez/",
            "https://www.infobae.com/tecno/2025/09/12/como-la-inteligencia-artificial-se-convirtio-en-uno-de-los-mayores-auges-de-capital-de-la-historia-moderna/",
            "https://www.infobae.com/mexico/2025/09/14/buscan-regular-el-uso-de-ia-en-la-industria-artistica-y-de-entretenimiento-en-la-cdmx/",
            "https://www.infobae.com/tecno/2025/09/09/el-nuevo-informe-de-openai-revela-por-que-las-alucinaciones-en-chatgpt-persisten-incluso-en-sus-versiones-mas-avanzadas/",
            "https://www.infobae.com/tecno/2025/09/14/inteligencia-artificial-revoluciona-la-educacion-y-desafia-la-integridad-academica/",
            "https://www.eldiarioar.com/politica/circularon-videos-milei-kicillof-hechos-ia-identificarlos-cuidarse-desinformaciones_1_12587811.html",
            "https://www.lanacion.com.ar/sociedad/la-ia-el-periodismo-y-un-equilibrio-que-no-debe-perderse-nid10092025/",
            "https://www.lanacion.com.ar/economia/IA/navegando-oportunidades-una-dosis-saludable-de-realismo-sobre-la-ia-nid08092025/",
            "https://www.lanacion.com.ar/economia/IA/la-pelicula-her-ya-es-real-expertos-anticipan-el-impacto-de-la-inteligencia-artificial-en-la-salud-nid10092025/",
            "https://www.lanacion.com.ar/economia/IA/se-abren-mas-con-las-maquinas-un-informe-revelo-el-porcentaje-de-adolescentes-que-usa-la-ia-como-nid11092025/",
            "https://www.pagina12.com.ar/855330-una-sociologa-argentina-entre-las-100-personas-mas-influyent",
            "https://www.pagina12.com.ar/856450-que-hay-detras-del-estallido-juvenil-en-nepal-muertos-renunc",
            "https://www.clarin.com/opinion/nuevas-oportunidades-prosperidad-precaria-caras-economia-gig-america-latina_0_Yqs6BLWah9.html",
            "https://www.clarin.com/tecnologia/juez-estados-unidos-fallo-favor-google-deshacerse-chrome_0_lHIeLOI3fw.html",
            "https://www.clarin.com/viva/pasa-chatbots-convierten-gurues-destruyen-matrimonios-amistades_0_lqJMt2LUNN.html",
            "https://www.clarin.com/buena-vida/agrede-cuestiona-juzga-riesgos-contarle-problemas-chatgpt-tendencia-crece_0_Uhv4ffBUy1.html",
            "https://www.clarin.com/mundo/union-europea-impone-google-multa-3000-millones-dolares-pese-amenazas-donald-trump_0_V5L6UzVAK7.html"
            "https://www.clarin.com/tecnologia/inteligencia-artificial-vez-expertos-advierten-burbuja-punto-estallar_0_KNYBBOL52Y.html",
            "https://www.clarin.com/sociedad/moda-anti-shein-festival-propone-forma-vestirse-buenos-aires_0_hoXvYpDuZC.html",
            "https://www.clarin.com/tecnologia/condenan-google-pagar-425-millones-dolares-quedarse-datos-privados-usuarios_0_2CCFEtysqT.html",
            "https://www.clarin.com/opinion/inteligencia-artificial-alucina_0_nGi1Qs9oEO.html",
            "https://www.clarin.com/familias/pantallas-cena-desafio-apagar-dispositivos-charlar-familia_0_70vSAwAAi7.html",
            "https://www.clarin.com/autos/fabricante-autos-suv-lujo-perdio-rastro-40000-autos-0-km-ciberataque_0_SzVz2SXgWy.html",
            "https://www.clarin.com/familias/pebbling-memes-stickers-puente-afectivo-comunicacion-padres-hijos_0_MnlGfeEt4n.html",
            "https://www.clarin.com/cultura/ia-puede-amplificar-creatividad-humana-vision-curador-catalan-lluis-nacenta_0_JZUhRpNZJF.html",
            "https://www.clarin.com/tecnologia/fortinet-alerta-correo-electronico-sigue-clave-ciberataques-ia-amplifica-phishing_0_hzir1e8DIO.html",
            "https://www.clarin.com/tecnologia/sam-altman-reconoce-teoria-internet-muerto-convirtiendo-realidad_0_VrodiOn26J.html",
            "https://www.clarin.com/tecnologia/andrew-tanenbaum-windows-lleno-errores-microsoft-entiende-manera-completa_0_ErIx448H0t.html",
            "https://www.clarin.com/viva/espacios-anti-meme-necesitamos-pensar_0_RX18qj9QrB.html",
            "https://www.eldiarioar.com/sociedad/modelo-ia-capaz-predecir-riesgo-millar-enfermedades-decadas-antelacion_1_12611418.html",
            "https://www.infobae.com/tecno/2025/09/08/ftc-investigara-impacto-de-chatbots-en-la-salud-mental-de-ninos/",
            "https://www.lanacion.com.ar/tecnologia/instagram-prueba-una-funcion-que-permite-a-creadores-de-contenido-tener-sus-propios-chatbots-nid01072024/",
            "https://www.lanacion.com.ar/tecnologia/el-otro-lado-de-la-ia-la-contaminacion-que-genera-google-crecio-un-48-en-cinco-anos-por-el-mayor-nid03072024/",
            "https://www.ambito.com/tecnologia/eeuu-un-candidato-alcalde-prometio-que-dejara-gobernar-unrobotdeia-n6050644",
            "https://www.ambito.com/tecnologia/mark-zuckerberg-lamento-que-el-gobierno-biden-haya-censurado-contenido-la-pandemia-n6053435",
            "https://www.infobae.com/tecno/2024/09/10/reemplazan-profesores-por-inteligencia-artificial-la-educacion-de-los-ninos-con-realidad-virtual-y-mucho-mas/",
            "https://www.lanacion.com.ar/tecnologia/openai-suma-controles-parentales-chatgpt-avisara-cuando-los-menores-tengan-charlas-riesgosas-con-la-nid03092025/",
            "https://www.infobae.com/tecno/2025/09/04/crisis-de-empleo-y-automatizacion-experto-alertan-sobre-el-futuro-incierto-de-los-jovenes-ante-la-ia/",
            "https://www.lanacion.com.ar/editoriales/dilemas-que-provoca-la-inteligencia-artificial-nid13092025/",
            "https://www.infobae.com/tecno/2025/09/08/que-consecuencias-tiene-tratar-la-inteligencia-artificial-como-una-tecnologia-comun-y-no-como-una-revolucion-inedita/"]
df_articulos = ejecutar_escrapeo_senior(mis_urls)

nombre_archivo = "articulos_scrapeados.csv"

df_articulos.to_csv(nombre_archivo, index=False, encoding='utf-8-sig', sep=';')

print(f"✅ ¡Listo! Los datos se guardaron en: {nombre_archivo}")