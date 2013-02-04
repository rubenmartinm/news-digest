news-digest
===========

*Script para recibir por correo electronico nuevos números de publicaciones en PDF, enlaces de noticias de sitios sin RSS, etc.*

**Introducción**

¿has visto alguna vez una publicación de una revista o dossier en PDF que te interesa y no puedes suscribirte por RSS?

La motivación de hacer este *script* nace de esa necesidad. Hay varios sitios en internet que te dan la posibilidad de crear feeds RSS como [Feed43.com](http://feed43.com/).

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

