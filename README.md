Proyecto enfocado en la automatizacion de obtención e ingreso de datos de recetas de comida provenientes de diversas fuentes, especialmente de páginas web centradas en recetas de comida con un enfoque nutricional, incluyendo recetas típicas chilenas y de diferentes tipos. 

Se implementó un proceso ETL (Extracción, Transformación y Carga) que comenzó con un web scraping en cuatro fuentes principales: Dietdoctor, Comidas Típicas Chilenas, Nutrium y Guiding Stars. 
El repositorio del web scraping está disponible en https://github.com/EduardoPalma/WebScrappingRecipes.

Para la construcción del sistema, se aplicó el patrón de diseño "Pipes and Filters", donde cada filtro representa una transformación en el proceso ETL. 
El proyecto se destacó por la utilización de un modelo de machine learning llamado CRF (Conditional Random Field), comúnmente empleado en problemas de etiquetado NER o POST en el procesamiento del lenguaje natural. 
En este caso, el CRF se empleó para la detección de ingredientes, unidades de medida y las cantidades asociadas. 

Por ejemplo, el modelo CRF se utilizó específicamente para reconocer unidades de medida, ingredientes y cantidades en el texto contenidos en los ingredientes de las recetas.

    1 cucharada de sal
      - 1, cantidad
      - cucharada, unidad
      - sal, ingrediente
      
    2 zanahorias
      - 2, cantidad
      - None, unidad
      - zanahorias, ingrediente

    1/2 taza de arroz
      - 1/2, cantidad
      - taza, unidad
      - arroz, ingrediente

    pimienta a gusto
      - None, cantidad
      - None, unidad
      - pimienta, ingrediente

Para llevar a cabo el proceso, se recurrió a una fuente que abordó este problema: https://archive.nytimes.com/open.blogs.nytimes.com/2015/04/09/extracting-structured-data-from-recipes-using-conditional-random-fields/. 
En este recurso se describe la utilización del modelo CRF para resolver este tipo de problemas.

Con el objetivo de evitar la necesidad de realizar el entrenamiento del modelo y centrarse en el propósito del proyecto, se optó por utilizar una librería preimplementada llamada "ingredient-parser",
la cual incorpora el mismo modelo con la limitación de ser en inglés. Para superar esta barrera idiomática con las recetas obtenidas, se empleó un traductor (cabe destacar que 
la mejor solución sería entrenar un modelo propio, considerando las diferencias entre los idiomas inglés y español; si el software se destinara a producción, se debería implementar un modelo propio).

Además de todo esto, se utilizaron métricas de calidad, registros, normalización, transformación, 
limpieza y atributos de calidad de datos para ofrecer recetas de la mayor calidad posible en la plataforma de gestión nutricional "Nutrifoods".

Tecnologias de soporte fueron ElasticSearch para el almacenamiento de las recetas de comida, registros de errores y metricas de calidad, la visualizacion se realiza mediante el mismo stack de desarrollo especificamente "KIBANA".
