news-digest
===========

*Script para recibir por correo electronico nuevos números de publicaciones en PDF, enlaces de noticias de sitios sin feed RSS, etc.*

**Introducción**

¿Has visto alguna vez una publicación mensual de una revista o dossier en PDF que te interesa y no puedes suscribirte por RSS?
¿Alguna web con artículos sin feed RSS?

O simplemente, quieres recibir ciertos contenidos en un correo de toda la vida para leerlos tranquilamente

La motivación de hacer este *script* nace de esa necesidad.

A grandes rasgos, se trata de disponer de un equipo con conexión continua a internet (EC2 de Amazon, Raspberry Pi, DD-WRT, Tomato, SnakeOS, etc.) con un pequeño *script* que nos envíe un resumen diario o semanal con los cambios en ciertas páginas.

**Alternativas**

Existen varios sitios en internet que pueden dar un servicio análogo pero un *script* personalizado siempre se ajusta mas a nuestro gusto. Algunos ejemplos son:

- [feed43.com](http://feed43.com/)
- [specificfeeds.com](http://www.specificfeeds.com/)
- [ifttt.com](http://ifttt.com)
- [blogtrottr.com](http://blogtrottr.com/)
- [feedmyinbox.com](http://www.feedmyinbox.com/) - *descontinuado*

Si no encuentras nada que te guste siempre puedes empezar a usar `news-digest` ;-)

## Configuracion de fuentes

    Archivo de definicion de los origenes de datos y localizadores
    Parametros:
    
    fuente            : nombre identificador de la fuente
    url               : url del html
    sw_rama           : 1 = buscar desde rama, 0 = buscar en todo el html
    etiqueta_rama     : tag para buscar la rama a partir de la cual buscar
    atributo_rama     : atributo para filtrar = title, class, etc
    valor_rama        : cadena a buscar
    etiqueta_elemento : tag html a buscar para los enlaces
    atributo_elemento : atributo para filtrar = title, class, etc
    valor_elemento    : cadena a buscar
    no_deseados       : cadena expresion regular no deseados
    lineas_a_truncar  : cualquier linea antes del <html> que hace fallar el script

## Dependencias

- [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)

