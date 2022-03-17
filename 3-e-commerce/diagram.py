import sys
import os
sys.path.append(os.path.abspath("../shared/"))

import colors
from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.generic.blank import Blank
from diagrams.gcp.ml import NaturalLanguageAPI, TranslationAPI, DialogFlowEnterpriseEdition, RecommendationsAI
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

with Diagram(name="", graph_attr=graph_attr, show=False, filename="ecommerce-architecture"):  
  web = Custom("Web", "../assets/internet.png")
  ecommerce = Blank("", height="0.0", width="0.0")
  web_connector = Blank("", height="0.0", width="0.0")

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

    with Cluster("ERP"):
      erp = Blank("")

    with Cluster("Comercio Electrónico"):      
      shopify = Custom("", "../assets/shopify.png")
      woocommerce = Custom("", "../assets/woocommerce.png")
      prestashop = Custom("", "../assets/prestashop.png")
      magento = Custom("", "../assets/magento.png")

    with Cluster("Pasarelas de Pago"):
      stripe = Custom("Stripe", "../assets/stripe.png")
      paypal = Custom("PayPal", "../assets/paypal.png")
      mercadopago = Custom("MercadoPago", "../assets/mercado-pago.png")
      amazon_pay = Custom("Amazon Pay", "../assets/amazon-pay.png")

  with Cluster("Google Cloud Platform"):
    scheduler = Scheduler("Scheduler\n(Programador de tareas)")
    firebase_auth = Authentication("Firebase Authentication")
    cdn = CDN("Cloud CDN\n(Distribución de contenido)")    
    beats_connector = Blank("", height="0.0", width="0.0")

    with Cluster("Recomendaciones, Perfil de usuario y Análisis"):
      google_analytics = Custom("Google Analytics", "../assets/google-analytics.png")
      tag_manager = Custom("Tag Manager", "../assets/google-tag-manager.png")
      recommendations_ai = RecommendationsAI("Recommendations AI")
      dv360 = Custom("Display & Video 360\n(Campañas Publicitarias)", "../assets/google-dv360.png")

    with Cluster("Almacenamiento de datos"):
      bigquery = Bigquery("BigQuery\n(Almacen de datos)")
      base_datos = SQL("SQL\n(Historico, BD Core)")
      cache = Memorystore("Memorystore\n(Cache)")

    with Cluster("Backend"):
      contenedor = Run("Cloud Run\n(Aplicación)")
      bucket = Storage("Storage\n(Multimedia, Archivos)")
      event_bus = PubSub("PubSub\n(Bus de Eventos)")

      with Cluster("Servicios"):
        order_service = KubernetesEngine("Servicio de pedidos")
        product_service = KubernetesEngine("Servicio de productos")
        user_service = KubernetesEngine("Servicio de usuarios")
        payment_service = KubernetesEngine("Servicio de pagos")
        shipping_service = KubernetesEngine("Servicio de envíos")      
        recommendations_service = KubernetesEngine("Servicio de recomendaciones")

    with Cluster("Procesamiento"):
      dataflow = Dataflow("Dataflow\n(Perfilamiento de usuarios)")          
      ad_function = Functions("Cloud Function")

    with Cluster("Servicios Externos"):
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
  contenedor << Edge(color=colors.black, style="dotted") >> event_bus
  firebase_auth << Edge(color=colors.black, style="dotted") >> contenedor
  cdn << Edge(color=colors.black, style="dotted") >> firebase_auth
  event_bus << Edge(color=colors.black, style="dotted") >> [ order_service, product_service, user_service, payment_service, shipping_service, recommendations_service ]
  recommendations_ai << Edge(color=colors.black, style="dotted") >> recommendations_service

  # Conexiones GCP - Visualización
  [ smartphone, tablet, computer ] << Edge(color=colors.orange, tailport="e", headport="w", minlen="1") <<  web_connector
  web_connector >> Edge(color=colors.orange, tailport="e", headport="w", minlen="1") >> web
  web << Edge(color=colors.orange) >> cdn
  gds << Edge(color=colors.dark_blue) << bigquery
  [ tableau, powerbi ] << Edge(color=colors.dark_blue) >> cache

  # Conexiones GCP - Registros y monitoreo
  beats >> Edge(color=colors.black, style="dotted") >> logstash
  logstash >> Edge(color=colors.black, style="dotted") >> elasticsearch
  elasticsearch << Edge(color=colors.black, style="dotted") >> kibana  
  beats_connector - Edge(color=colors.light_blue, style="dashed") - [ function1, contenedor ]
  beats << Edge(color=colors.light_blue, style="dashed", tailport="e", headport="w", minlen="1") << beats_connector

  # GCP - Flujo Ecommerce
  tag_manager >> Edge(color=colors.black, style="dotted") >> google_analytics
  [ google_analytics, recommendations_ai ] >> Edge(color=colors.black, style="dotted", tailport="e", headport="w", minlen="1") >> bigquery

  # GCP - Servicios Externos
  api_gateway >> Edge(color=colors.black, style="dotted") >> function1
  function1 >> Edge(color=colors.black, style="dotted") >> contenedor
  csv >> Edge(color=colors.dark_blue) >> bucket
  kobotoolbox >> Edge(color=colors.dark_blue) >> api_gateway
  erp >> Edge(color=colors.dark_blue) >> [ api_gateway, bigquery ]
  [ shopify, woocommerce, prestashop, magento ] - Edge(color=colors.purple, style="bold", tailport="e", headport="w", minlen="1") - ecommerce
  ecommerce - Edge(color=colors.purple, style="bold", tailport="e", headport="w", minlen="1") - contenedor
  payment_connector = Blank("", height="0.0", width="0.0")
  [ paypal, mercadopago, stripe, amazon_pay ] - Edge(color=colors.dark_blue, tailport="e", headport="w", minlen="1") - payment_connector
  payment_connector >> Edge(color=colors.dark_blue, tailport="e", headport="n", minlen="1") >> payment_service

  # GCP - Procesamiento
  dataflow << Edge(color=colors.black, style="dotted") << bigquery
  dataflow >> Edge(color=colors.black, style="dotted") >> ad_function
  ad_function >> Edge(color=colors.black, style="dotted") >> dv360
  scheduler >> Edge(color=colors.black, style="dotted") >> dataflow
