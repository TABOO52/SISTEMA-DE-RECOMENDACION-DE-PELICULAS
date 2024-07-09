### **DESCRIPCION**
Sistema de recomendacion de peliculas deployando una API en RENDER junto a otras 6 funciones utiles para la consulta y analisis de datos.
### **TABLA DE CONTENIDO**
## Tabla de contenido
1. [Introducción](#introducción)
2. [Instalación y Requisitos](#instalación-y-requisitos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Uso y Ejecución](#uso-y-ejecución)
5. [Datos y Fuentes](#datos-y-fuentes)
6. [Metodología](#metodología)
7. [Resultados y Conclusiones](#resultados-y-conclusiones)
8. [Contribución y Colaboración](#contribución-y-colaboracion)
9. [Autores](#autores)
### **INTRODUCCIÓN**
La capacidad que las maquinas que tienen para aprender hoy en dia son impresionantes, variando sus usos desde el uso en vias para poder analizar el estado de la carretera hasta la comodidad de tu casa en donde a diario encontrarás decenas peliculas basadas en tus gustos recomendadas por tu plataforma de confianza. Esto ultimo lo trabajaremos en este proyecto, generando un MVP y observando sus resultados. Dicho esto ¿Por donde empezamos?

![Plataformas](images/plataformas.jpeg)

### **INSTALACIÓN Y REQUISITOS**
- Python 3.7 o superior
- Todas las librerias usadas las encuentras en el archivo "requirements.txt"
### **ESTRUCTURA DEL PROYECTO**
![FLOWCHART PROYECTO"](images/flowchart.gif)
### **USO Y EJECUCIÓN**
 1. Abrir link https://movies-and-credits.onrender.com y presionar boton de 'Comienzo' (Si la pagina no carga intentar de nuevo en 5 min)
 2. Encontraras 8 diferentes recuadros identificados con la palabra 'GET' ignoraremos el primero, vamos a trabajar con los 7 siguientes.
 3. Al desplegar cada recuadro encontraremos el boton 'try it out' donde se nos permitirá escribir el dato de entrada.
 4. Al ejecutar la salida deberia verse de la siguiente manera (caso de ejemplo):
    ![Response body](images/responsebody.png)
    
 Para una explicación mas a detalle visitar el siguiente link.
### **DATOS Y FUENTES**
- [FastAPI-Render](https://github.com/orestes-victor/Repositorio_guia_para_fastAPI_y_RENDER)
- (S/f). Unirioja.es. Recuperado el 8 de julio de 2024, de [https://dialnet.unirioja.es/servlet/articulo?codigo=7242764](https://dialnet.unirioja.es/servlet/articulo?codigo=7242764)
- [Exploratory Data Analysis with Pandas Python](https://www.youtube.com/watch?v=xi0vhXFPegw)
### **METODOLOGÍA**
Para dar comienzo a nuestro proyecto nos vamos a basar en las principales fases que componen el mismo, tomando asi como eje de guia la estructura del prroyecto.

1. #### **Ingesta de datos**
   A la hora de trabajar con la ingesta de datos deberemos analizar el tipo de archivo que estaremos analizando, su fuente de ingreso y su contexto, adicional a ello deberemos analizar el tipo de codificacion en el que se enccuentra el mismo. Para esta ingesta de datos usaremos pandas.
2. #### **EDA**
   - **Chequeo de nulos:** En esa seccion definimos todos los valores nulos que no aportan mayor informacion o los que podemos reemplazar otro valor.
   - **Valores duplicados:** En esta seccion identificamos los valores duplicados, analizamos sus causas y se evalua la decision de dejarlos o no.
   - **Valores faltantes:** En esta seccion revisamos valores que tienen algun problema de tipado o en su celda está identificado como Nan, para posteriormente analizar de que manera completar estos valores o eliminarlos del dataset
   - **Tipos de datos:** Se chequea de manera especifica cada columna del dataset en busca de alguna discrepancia que nos indique el cambio de tipo de datos que este maneja por defecto.
   - **Analisis outlier:** En este seccion revisamos normalmente de las columnas numericas de gran relevancia los valores que estan fuera de lo común, revisando la decision de eliminar o mantener dichos datos y el como puede afectar el dataset.
   - **Analisis estadistico de datos** En esta seccion finalmente logramos ver mediante unas columnas de datos especificas como se han comportado los datos, ya sea a lo largo de los años, su tendencia y popularidad de los mismos.
   - **Analisis de correlaciones bi y multivariado:** En esta seccion vamos a revisar aquellas columnas con algun tipo de relacion, y encontrar a lo largo de las filas que valores pueden tener mayor incidencia a estar repetidos o relacionados.
3. #### **ETL**
4. #### **API**
5. #### **Machine Learning**
6. #### **Modelo Final**


### **RESULTADOS Y CONCLUSIONES**
### **CONTRIBUCIÓN Y COLABORACION**
### **AUTORES**




