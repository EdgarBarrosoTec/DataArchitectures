import sys
import os
sys.path.append(os.path.abspath("../shared/"))

import colors
from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.blank import Blank
from diagrams.gcp.ml import NaturalLanguageAPI, TranslationAPI, DialogFlowEnterpriseEdition
from diagrams.gcp.api import APIGateway
from diagrams.gcp.network import CDN
from diagrams.gcp.storage import Storage
from diagrams.gcp.compute import Run, Functions
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.database import SQL, Memorystore
from diagrams.gcp.analytics import Bigquery
from diagrams.onprem.analytics import Tableau, PowerBI
from diagrams.firebase.develop import Authentication
from diagrams.generic.device import Mobile, Tablet
from diagrams.elastic.elasticsearch import Elasticsearch, Kibana, Logstash, Beats

with Diagram(name="Arquitectura Quiosco turístico", show=False, filename="tourist-kiosk-architecture"):  
  web = Custom("Web", "../assets/internet.png")  

  with Cluster("Ingesta de datos"):
    with Cluster("Archivos"):
      drive = Custom("Google Drive", "../assets/google-drive.png")
      csv = Custom("CSV", "../assets/file.png")

    with Cluster("Formularios"):
      kobotoolbox = Custom("Kobotoolbox", "../assets/kobotoolbox.png")
      google_docs = Custom("Google Docs", "../assets/google-docs.png")

  with Cluster("Visualización"):    
    smartphone = Mobile("Smartphone")
    tablet = Tablet("Tablet")
    computer = Custom("Computadora", "../assets/computer.png")
    tableau = Tableau("Tableau")
    powerbi = PowerBI("Power BI")
    gds = Custom("Google Data Studio", "../assets/google-data-studio.png")  

  with Cluster("Google Cloud Platform"):
    google_assistant = Custom("Google Assistant", "../assets/google-assistant.png")
    scheduler = Scheduler("Scheduler\n(Programador de tareas)")
    firebase_auth = Authentication("Firebase Authentication")
    cdn = CDN("Cloud CDN\n(Distribución de contenido)")

    with Cluster("Almacenamiento de datos"):
      bigquery = Bigquery("BigQuery\n(Almacen de datos)")
      base_datos = SQL("SQL\n(Historico, BD Core)")
      cache = Memorystore("Memorystore\n(Cache)")

    with Cluster("Backend"):
      contenedor = Run("Cloud Run\n(Aplicación)")
      bucket = Storage("Storage\n(Multimedia, Archivos)")

    with Cluster("Procesamiento de lenguaje natural"):
      nlp = NaturalLanguageAPI("Natural Language API\n(Análisis de lenguaje natural)")
      nlp_in = Storage("Storage\nFormularios")
      nlp_function = Functions("Functions\n(Rutina de procesamiento)")      
      translations = TranslationAPI("Translation API\n(Traducción de idiomas)")
      dialogflow = DialogFlowEnterpriseEdition("DialogFlow\n(IA de Converssación)")

    with Cluster("Entrada de datos"):
      function1 = Functions("Cloud Function")
      api_gateway = APIGateway("API Gateway")

    with Cluster("Registros y monitoreo"):
      elasticsearch = Elasticsearch("Elasticsearch\n(Registro de eventos/errores)")      
      logstash = Logstash("Logstash\n(Procesamiento de logs)")
      beats = Beats("Beats\n(Ingesta)")
      kibana = Kibana("Kibana\n(Monitorización y Debugging)")

  # Conexiones GCP - Almacenamiento de datos
  base_datos << Edge(color=colors.black, style="dotted") >> cache
  bigquery << Edge(color=colors.black, style="dotted") >> cache
  cache << Edge(color=colors.black, style="dotted") >> contenedor

  # Conexiones GCP - Backend
  contenedor << Edge(color=colors.black, style="dotted") >> bucket
  firebase_auth << Edge(color=colors.black, style="dotted") >> contenedor
  cdn << Edge(color=colors.black, style="dotted") >> firebase_auth

  # Conexiones GCP - Entrada de datos
  function1 << Edge(color=colors.black, style="dotted") << api_gateway
  function1 >> Edge(color=colors.black, style="dotted") >> nlp_in
  csv >> Edge(color=colors.dark_blue) >> nlp_in
  kobotoolbox >> Edge(color=colors.dark_blue) >> api_gateway
  google_docs >> Edge(color=colors.dark_blue) >> api_gateway

  # Conexiones GCP - Visualización
  [ smartphone, tablet, computer ] << Edge(color=colors.orange) >> web
  web << Edge(color=colors.orange) >> cdn
  gds << Edge(color=colors.dark_blue) >> bigquery
  [ tableau, powerbi ] << Edge(color=colors.dark_blue) >> cache
  smartphone >> Edge(color=colors.black) >> google_assistant

  # Conexiones GCP - Registros y monitoreo
  beats >> Edge(color=colors.black, style="dotted") >> logstash
  logstash >> Edge(color=colors.black, style="dotted") >> elasticsearch
  elasticsearch << Edge(color=colors.black, style="dotted") >> kibana
  beats << Edge(color=colors.light_blue, style="dashed") << contenedor
  beats << Edge(color=colors.light_blue, style="dashed") << function1
  nlp_function >> Edge(color=colors.light_blue, style="dashed") >> beats

  # Procesamiento de lenguaje natural
  nlp_function << Edge(color=colors.black, style="dotted") << nlp_in
  nlp_function >> Edge(color=colors.black, style="dotted") >> nlp  
  scheduler >> Edge(color=colors.black, style="dotted", label="iniciar procesamiento") >> nlp_function  
  nlp >> Edge(color=colors.black, style="dotted") >> translations
  translations >> Edge(color=colors.black, style="dotted") >> bigquery
  web >> Edge(color=colors.dark_blue) >> dialogflow  
  google_assistant >> Edge(color=colors.black, style="dotted") >> dialogflow
  dialogflow << Edge(color=colors.black, style="dotted") >> contenedor
