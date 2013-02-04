news-digest
===========

*Script para recibir por correo electronico nuevos números de publicaciones en PDF, enlaces de noticias de sitios sin feed RSS, etc.*

**Introducción**

¿Has visto alguna vez una publicación mensual de una revista o dossier en PDF que te interesa y no puedes suscribirte por RSS?
¿Alguna web con artículos sin feed RSS?

O simplemente, quieres recibir ciertos contenidos en un correo de toda la vida para leerlos tranquilamente.

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

## Instalación

    $ git clone https://github.com/rubenmartinm/news-digest.git
    
## Configuracion

**Configuración de las fuentes de datos**

Abrimos `contenidos.txt` con nuestro editor habitual para añadir/modificar nuestras fuentes. Cada fuente esta definida en una línea del archivo en formato CSV.

Los parámetros necesarios son los siguientes:
    
    fuente            : nombre identificador de la fuente
    url               : url del html

La ´fuente´ es el nombre identificador que aparecerá como título seguido de sus enlaces (si ha habido cambios en la fuente al generar el correo), p.e.: *web de revista*

La 'url' es la dirección de la página p.e. *http://url.a.mirevista.es/ArchivoRevista/Hemeroteca*

    sw_rama           : 1 = buscar desde rama, 0 = buscar en todo el html
    
    etiqueta_rama     : tag para buscar la rama a partir de la cual buscar
    atributo_rama     : atributo para filtrar = title, class, etc
    valor_rama        : cadena a buscar
    
Este bloque de parametros marca si necesitamos circunscribir la búsqueda a una rama concreta dentro del *html*.

El valor de 'sw_rama' definirá esta opción.

Si 'sw_rama' es '1':

La 'etiqueta_rama' es el tag de la rama raiz, 'atributo_rama' es el atributo y 'valor_rama' el valor a buscar p.e. div;class;columna_principal -> < div class="columna_principal" >

Para encontrar los valores adecuados es recomendable usar el [Firebug](https://addons.mozilla.org/en-US/firefox/addon/firebug/) para Firefox o en Chrome Menu -> Tools -> Developer Tools.

    etiqueta_elemento : tag html a buscar para los enlaces
    atributo_elemento : atributo para filtrar = title, class, etc
    valor_elemento    : cadena a buscar
    
Idem que para la rama pero esta vez para los enlaces concretos a las noticias.

    no_deseados       : cadena expresion regular no deseados
    lineas_a_truncar  : cualquier linea antes del <html> que hace fallar el script

Por último dos parámetros adicionales que me han resultado necesarios:

'no_deseados' es una cadena para descartar enlaces no deseados mediante una expresion regular.

'lineas_a_truncar' es un contador de líneas a descartar antes de < html > que en alguna página es necesario :-?

**Configuración necesaria para el envío de correo electrónico**

    # Envio de correo por smtp.google.com
    gmail_user = "USUARIO_GMAIL"
    gmail_pwd = "PASSWORD_GMAIL"

    # Correo destinatario
    mail_to = "CORREO"

**Configuración adicional para la ejecución desde un cron (opcional)**

    # Para la ejecucion del script desde un cron
    ruta = "RUTA COMPLETA"

## Dependencias

- [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/)
- urllib2
- smtplib
- MIMEMultipart
- MIMEText
- defaultdict
