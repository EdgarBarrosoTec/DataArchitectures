import sys
import os
sys.path.append(os.path.abspath("../shared/"))

import colors
from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.blank import Blank
from diagrams.gcp.api import APIGateway
from diagrams.gcp.iot import IotCore
from diagrams.gcp.network import CDN
from diagrams.gcp.storage import Storage
from diagrams.gcp.compute import Run, Functions
from diagrams.gcp.devtools import Scheduler
from diagrams.gcp.database import SQL, Memorystore
from diagrams.gcp.analytics import PubSub, Dataflow, Bigquery
from diagrams.onprem.analytics import Tableau, PowerBI
from diagrams.firebase.develop import Authentication
from diagrams.generic.device import Mobile, Tablet
from diagrams.elastic.elasticsearch import Elasticsearch, Kibana, Logstash, Beats

graph_attr = {
    "splines": "spline",
    "concentrate":"true",
}

with Diagram(name="Arquitectura IoT (agricultura y ganadería)", graph_attr=graph_attr, show=False, filename="iot-architecture"):
  web = Custom("Web", "../assets/internet.png")

  with Cluster("Local"):    
    maquinaria = Custom("Maquinaria", "../assets/tractor.png")
    ganaderia = Custom("Ganadería", "../assets/ganado.png")    
    hub = Custom("Dispositivo IoT", "../assets/hub.png")
    sensor1 = Custom("sensor", "../assets/sensor.png")
    sensor2 = Custom("sensor", "../assets/sensor.png")
    sensor3 = Custom("sensor", "../assets/sensor.png")
    sensor4 = Custom("sensor", "../assets/sensor.png")
    sensor_connector = Blank("", height="0.0", width="0.0")

    with Cluster("Agricultura"):
      maiz= Custom("", "../assets/maiz.png")
      trigo = Custom("", "../assets/trigo.png")      

  with Cluster("Visualización"):    
    smartphone = Mobile("Smartphone")
    tablet = Tablet("Tablet")
    computer = Custom("Computadora", "../assets/computer.png")
    tableau = Tableau("Tableau")
    powerbi = PowerBI("Power BI")
    gds = Custom("Google Data Studio", "../assets/google-data-studio.png")

  with Cluster("Servicios Externos"):
    with Cluster("Archivos"):
      drive = Custom("Google Drive", "../assets/google-drive.png")
      csv = Custom("CSV", "../assets/file.png")

    with Cluster("Formularios"):
      kobotoolbox = Custom("Kobotoolbox", "../assets/kobotoolbox.png")

  with Cluster("Google Cloud Platform"):    
    scheduler = Scheduler("Scheduler\n(Programador de Tareas)")
    firebase_auth = Authentication("Firebase Authentication")
    cdn = CDN("Cloud CDN\n(Distribución de contenido)")

    with Cluster("Ingesta de datos"):
      iot_core = IotCore("IoT Core\n(Administrar dispositivos IoT )")
      pubsub = PubSub("PubSub\n(Cola de mensajes)")

    with Cluster("Procesamiento"):
      agregacion = Dataflow("Dataflow\n(Agregación)")
      decodificacion = Dataflow("Dataflow\n(Decodificación)")

    with Cluster("Almacenamiento de datos"):
      bigquery = Bigquery("BigQuery\n(Almacen de datos)")
      base_datos = SQL("SQL\n(Historico, BD Core)")
      cache = Memorystore("Memorystore\n(Cache)")

    with Cluster("Backend"):
      contenedor = Run("Cloud Run\n(Aplicación)")
      bucket = Storage("Storage\n(Multimedia, Archivos)")

    with Cluster("Integración externa"):
      function1 = Functions("Cloud Function\n(Salida)")
      functions = Functions("Cloud Function\n(Entrada)")
      api_gateway = APIGateway("API Gateway")

    with Cluster("Registros y monitoreo"):
      elasticsearch = Elasticsearch("Elasticsearch\n(Registro de eventos/errores)")      
      logstash = Logstash("Logstash\n(Procesamiento de logs)")
      beats = Beats("Beats\n(Ingesta)")
      kibana = Kibana("Kibana\n(Monitorización y Debugging)")  

  # Conexiones Local
  maiz >> Edge(color=colors.black, style="dotted") >> sensor1
  trigo >> Edge(color=colors.black, style="dotted") >> sensor2
  maquinaria >> Edge(color=colors.black, style="dotted") >> sensor3
  ganaderia >> Edge(color=colors.black, style="dotted") >> sensor4  
  [sensor1, sensor2, sensor3, sensor4] - Edge(color=colors.black, style="dotted", tailport="e", headport="w", minlen="1") - sensor_connector
  sensor_connector >> Edge(color=colors.black, style="dotted") >> hub
  hub >> Edge(color=colors.black) >> iot_core

  # Conexiones GCP - Ingesta de datos
  iot_core >> Edge(color=colors.black, style="dotted") >> pubsub
  pubsub >> Edge(color=colors.black, style="dotted") >> decodificacion

  # Conexiones GCP - Procesamiento
  decodificacion >> Edge(color=colors.black, style="dotted") >> bigquery
  agregacion << Edge(color=colors.black, style="dotted") >> bigquery
  agregacion >> Edge(color=colors.black, style="dotted") >> base_datos

  # Conexiones GCP - Almacenamiento de datos
  base_datos << Edge(color=colors.black, style="dotted") >> cache
  bigquery << Edge(color=colors.black, style="dotted") >> cache
  cache << Edge(color=colors.black, style="dotted") >> contenedor

  # Conexiones GCP - Backend
  contenedor << Edge(color=colors.black, style="dotted") >> bucket
  firebase_auth << Edge(color=colors.black, style="dotted") >> contenedor
  cdn << Edge(color=colors.black, style="dotted") >> firebase_auth

  # Conexiones GCP - Integración externa
  function1 >> Edge(color=colors.black, style="dotted") >> api_gateway
  functions << Edge(color=colors.black, style="dotted") >> api_gateway
  function1 << Edge(color=colors.black, style="dotted") << cache
  functions >> Edge(color=colors.black, style="dotted") >> bigquery

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
  beats << Edge(color=colors.light_blue, style="dashed") << contenedor
  beats << Edge(color=colors.light_blue, style="dashed") << [ function1, functions ]

  # Conexiones GCP - Servicios Externos
  csv >> Edge(color=colors.dark_blue) >> bucket
  kobotoolbox >> Edge(color=colors.dark_blue) >> api_gateway

  # GCP - Otros
  scheduler >> Edge(color=colors.black, style="dotted") >> agregacion