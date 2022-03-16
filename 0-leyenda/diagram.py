import sys
import os
sys.path.append(os.path.abspath("../shared/"))

import colors
from diagrams import Cluster, Diagram, Edge
from diagrams.generic.blank import Blank

with Diagram(show=False, filename="leyenda"):
  with Cluster("Leyenda"):
    with Cluster("Tipo de conexión"):
      Blank() - Edge(label="Conexión Local", color=colors.black, style="dotted") - Blank()
      Blank() - Edge(label="Conexión Remota", color=colors.black) - Blank()
    
    with Cluster("Dirección del flujo"):
      a_unidirectional, b_unidirectional = Blank(), Blank()
      a_unidirectional >> Edge(label="Flujo unidireccional", color=colors.black) >> b_unidirectional
      a_unidirectional << Edge(label="", color=colors.black) << b_unidirectional      
      Blank() << Edge(label="Flujo bidireccional", color=colors.black) >> Blank()

    with Cluster("Colores"):
      Blank() - Edge(label="Proposito general", color=colors.black) - Blank()
      Blank() - Edge(label="Tráfico web", color=colors.orange) - Blank()
      Blank() - Edge(label="Entrada (servicios externos), Salida (Visualización)", color=colors.dark_blue) - Blank()
      Blank() - Edge(label="Depuración, captura de errores, métricas", color=colors.light_blue) - Blank()