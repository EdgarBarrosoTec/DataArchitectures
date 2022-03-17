import sys
import os
sys.path.append(os.path.abspath("../shared/"))

import colors
from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.blank import Blank
from diagrams.gcp.ml import VisionAPI, VideoIntelligenceAPI, TextToSpeech, SpeechToText, TranslationAPI
from diagrams.gcp.api import APIGateway
from diagrams.gcp.network import CDN
from diagrams.gcp.storage import Storage
from diagrams.gcp.compute import Run, Functions, KubernetesEngine
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.database import SQL, Memorystore
from diagrams.gcp.analytics import Bigquery, PubSub, Dataflow
from diagrams.onprem.analytics import Tableau, PowerBI
from diagrams.firebase.develop import Authentication
from diagrams.generic.device import Mobile, Tablet
from diagrams.elastic.elasticsearch import Elasticsearch, Kibana, Logstash, Beats

graph_attr = {
    "splines": "spline",
    "concentrate":"true",
}

with Diagram(name="Arquitectura de Datos Multimedia", graph_attr=graph_attr, show=False, filename="multimedia-architecture"):  
  web = Custom("Web", "../assets/internet.png")

  with Cluster("Visualización"):    
    smartphone = Mobile("Smartphone")
    tablet = Tablet("Tablet")
    computer = Custom("Computadora", "../assets/computer.png")
    tableau = Tableau("Tableau")
    powerbi = PowerBI("Power BI")
    gds = Custom("Google Data Studio", "../assets/google-data-studio.png")  

  with Cluster("Servicios Externos"):
    with Cluster("Redes sociales"):
      facebook = Custom("Facebook", "../assets/facebook.png")
      instagram = Custom("Instagram", "../assets/instagram.png")
      twitter = Custom("Twitter", "../assets/twitter.png")
      linkedin = Custom("LinkedIn", "../assets/linkedin.png")

    with Cluster("Archivos"):
      drive = Custom("Google Drive", "../assets/google-drive.png")
      csv = Custom("CSV", "../assets/file.png")
      image = Custom("Imagen", "../assets/image.png")
      video = Custom("Video", "../assets/video.png")
      audio = Custom("Audio", "../assets/audio.png")
      texto = Custom("Texto / Transcripción", "../assets/text.png")

    with Cluster("Formularios"):
      kobotoolbox = Custom("Kobotoolbox", "../assets/kobotoolbox.png")

    with Cluster("ERP"):
      erp = Blank("")

  with Cluster("Google Cloud Platform"):
    firebase_auth = Authentication("Firebase Authentication")
    cdn = CDN("Cloud CDN\n(Distribución de contenido)")    

    with Cluster("Procesamiento de imágenes"):
      vision_api = VisionAPI("Vision API")
      image_processing = Functions("Cloud Function\n(Procesar al subir imagen)")
      image_storage = Storage("Almacenamiento de imágenes")
      store_image_metadata = Functions("Cloud Function\n(Guardar metadata de imagen)")
      media_storage_connector = Blank("", height="0.0", width="0.0")
      Blank("")

    with Cluster("Procesamiento de video"):
      video_intelligence_api = VideoIntelligenceAPI("Video AI")
      video_storage = Storage("Almacenamiento de video")
      video_processing = Functions("Cloud Function\n(Procesar al subir video)")
      video_metadata = Functions("Cloud Function\n(Guardar metadata de video)")
      Blank("")

    with Cluster("Procesamiento de audio"):
      translation = TranslationAPI("Google Translate API")
      speach_to_text = SpeechToText("Speach to Text")
      text_to_speach = TextToSpeech("Text to Speach")
      audio_storage = Storage("Almacenamiento de audio")
      text_storage = Storage("Almacenamiento de texto")
      audio_speech_processing = Functions("Cloud Function\n(Procesar al subir audio)")
      text_processing = Functions("Cloud Function\n(Procesar al subir texto)")

    with Cluster("Almacenamiento de datos"):
      bigquery = Bigquery("BigQuery\n(Almacen de datos)")
      base_datos = SQL("SQL\n(Historico, BD Core)")
      cache = Memorystore("Memorystore\n(Cache)")

    with Cluster("Backend"):
      contenedor = Run("Cloud Run\n(Aplicación)")
      bucket = Storage("Storage\n(Archivos Estáticos)")

    with Cluster("Servicios Externos"):
      function1 = Functions("Cloud Function\n(Entrada)")
      api_gateway = APIGateway("API Gateway")
      socialmedia_func = Functions("Cloud Function\n(Extract Post, Likes, Comments,\nVideo, Image, etc)")

    with Cluster("Registros y monitoreo"):
      elasticsearch = Elasticsearch("Elasticsearch\n(Registro de eventos/errores)")      
      logstash = Logstash("Logstash\n(Procesamiento de logs)")
      beats = Beats("Beats\n(Ingesta)")
      kibana = Kibana("Kibana\n(Monitorización y Debugging)")

  # Conexiones GCP - Almacenamiento de datos
  base_datos << Edge(color=colors.black, style="dotted") >> cache
  bigquery << Edge(color=colors.black, style="dotted") >> cache
  cache << Edge(color=colors.black, style="dotted") >> contenedor
  [ speach_to_text, video_metadata, store_image_metadata ] - Edge(color=colors.black, style="dotted,bold", tailport="e", headport="w", minlen="1") - media_storage_connector  
  media_storage_connector >> Edge(color=colors.black, style="dotted,bold") >> bigquery

  # Conexiones GCP - Backend
  contenedor << Edge(color=colors.black, style="dotted") >> bucket
  firebase_auth << Edge(color=colors.black, style="dotted") >> contenedor
  cdn << Edge(color=colors.black, style="dotted") >> firebase_auth

  # Conexiones GCP - Visualización
  web_connector = Blank("", height="0.0", width="0.0")
  [ smartphone, tablet, computer ] << Edge(color=colors.orange, tailport="e", headport="w", minlen="1") << web_connector
  web_connector >> Edge(color=colors.orange, tailport="e", headport="w", minlen="1") >> web
  web << Edge(color=colors.orange) >> cdn
  gds << Edge(color=colors.dark_blue) >> bigquery
  [ tableau, powerbi ] << Edge(color=colors.dark_blue) >> cache

  # Conexiones GCP - Registros y monitoreo
  beats >> Edge(color=colors.black, style="dotted") >> logstash
  logstash >> Edge(color=colors.black, style="dotted") >> elasticsearch
  elasticsearch << Edge(color=colors.black, style="dotted") >> kibana
  beats << Edge(color=colors.light_blue, style="dashed") << [ contenedor, function1 ]

  # GCP - Servicios Externos
  api_gateway >> Edge(color=colors.black, style="dotted") >> function1
  function1 >> Edge(color=colors.black, style="dotted,bold", tailport="n", headport="n", minlen="1") >> contenedor
  kobotoolbox >> Edge(color=colors.dark_blue, tailport="e", headport="w", minlen="1") >> api_gateway
  erp >> Edge(color=colors.black) >> [ api_gateway, bigquery ]
  csv >> Edge(color=colors.dark_blue, tailport="n", headport="w", minlen="3") >> bucket
  socialmedia_connector = Blank("", height="0.0", width="0.0")
  [ facebook, instagram, twitter, linkedin ] - Edge(color=colors.purple, tailport="e", headport="w", minlen="1") - socialmedia_connector
  socialmedia_connector >> Edge(color=colors.purple, tailport="e", headport="n", minlen="5") >> api_gateway
  api_gateway >> Edge(color=colors.black, style="dotted", tailport="e", headport="w", minlen="1") >> socialmedia_func
  socialmedia_func >> Edge(color=colors.black, style="dotted", tailport="e", headport="w", minlen="1") >> [ video_storage, image_storage, text_storage ]

  # GCP - Procesamiento de imágenes
  image >> Edge(color=colors.dark_blue, tailport="e", headport="w", minlen="1") >> image_storage
  image_storage >> Edge(color=colors.black, style="dotted") >> image_processing
  image_processing >> Edge(color=colors.black, style="dotted") >> vision_api
  vision_api >> Edge(color=colors.black, style="dotted") >> store_image_metadata  

  # GCP - Procesamiento de video
  video >> Edge(color=colors.dark_blue) >> video_storage
  video_storage >> Edge(color=colors.black, style="dotted") >> video_processing
  video_processing >> Edge(color=colors.black, style="dotted") >> video_intelligence_api
  video_intelligence_api >> Edge(color=colors.black, style="dotted") >> video_metadata  

  # GCP - Procesamiento de audio
  audio >> Edge(color=colors.dark_blue) >> audio_storage
  texto >> Edge(color=colors.dark_blue) >> text_storage
  audio_storage >> Edge(color=colors.black, style="dotted") >> audio_speech_processing
  text_storage >> Edge(color=colors.black, style="dotted") >> text_processing
  audio_speech_processing >> Edge(color=colors.black, style="dotted") >> speach_to_text
  speach_to_text >> Edge(color=colors.black, style="dotted") >> translation  
  text_processing >> Edge(color=colors.black, style="dotted") >> text_to_speach
  text_to_speach >> Edge(color=colors.black, style="dotted") >> translation