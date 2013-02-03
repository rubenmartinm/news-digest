#############################################
# HTML scraping with Python and BeautifulSoup
#############################################

#----------------------------------------------------------------------------------------------------------
# Variables a personalizar
#----------------------------------------------------------------------------------------------------------

# Envio de correo por smtp.google.com
gmail_user = "USUARIO_GMAIL"
gmail_pwd = "PASSWORD_GMAIL"

# Correo destinatario
mail_to = "CORREO"

# Para la ejecucion del script desde un cron
ruta = "RUTA COMPLETA"

#----------------------------------------------------------------------------------------------------------
# Librerias
#----------------------------------------------------------------------------------------------------------

import urllib
import urllib2
import string
import sys
import codecs
import smtplib
import datetime
import re

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import defaultdict
from datetime import date, timedelta

#----------------------------------------------------------------------------------------------------------
# Definiciones comunes
#----------------------------------------------------------------------------------------------------------

arch_fuentes = ruta+"contenidos.txt"
arch_ultimos = ruta+"ultimos.txt"

dias = { 'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miercoles', 'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sabado', 'Sunday': 'Domingo' }

invalid_tags = ['b', 'i', 'em']
 
#####
# Url
#####

headers = { 'User-Agent' : 'User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
            'Accept-Charset' : 'utf-8' }

####################################################
# Fuentes especiales con url dependiente de la fecha
####################################################

#now = datetime.datetime.now()

yesterday = date.today() - timedelta(1)

lista_fuentes_especiales = [ { "fuente": "global voices EN",
                               "url": "http://globalvoicesonline.org/"+yesterday.strftime("%Y/%m/%d/"),
                               "sw_rama": "1",
                               "etiqueta_rama": "div",
                               "atributo_rama": "class",
                               "valor_rama": "dategroup",
                               "etiqueta_elemento": "a",
                               "atributo_elemento": "rel",
                               "valor_elemento": "bookmark",
                               "no_deseados": "read",
                               "lineas_a_truncar": "0" 
                             }, 
                            { "fuente": "global voices ES",
                               "url": "http://es.globalvoicesonline.org/"+yesterday.strftime("%Y/%m/%d/"),
                               "sw_rama": "1",
                               "etiqueta_rama": "div",
                               "atributo_rama": "class",
                               "valor_rama": "dategroup",
                               "etiqueta_elemento": "a",
                               "atributo_elemento": "rel",
                               "valor_elemento": "bookmark",
                               "no_deseados": "leer",
                               "lineas_a_truncar": "0"
                            } ]


#----------------------------------------------------------------------------------------------------------
# Funciones
#----------------------------------------------------------------------------------------------------------

##############
# Leer fuentes
##############

def get_sources():
    f = open(arch_fuentes)
    lista_archivo = f.readlines()
    f.close()

    lista_fuentes = []

    for item in lista_archivo:
        item = item.rstrip()
	if ( item.startswith("#") == 0 ):
            lista_fuente = item.split(";")
        
            lista_fuentes.append( {"fuente": lista_fuente[0], 
                                   "url": lista_fuente[1], 
                                   "sw_rama": lista_fuente[2], 
                                   "etiqueta_rama": lista_fuente[3],
                                   "atributo_rama": lista_fuente[4],
                                   "valor_rama": lista_fuente[5],
                                   "etiqueta_elemento": lista_fuente[6],
                                   "atributo_elemento": lista_fuente[7],
                                   "valor_elemento": lista_fuente[8],
                                   "no_deseados": lista_fuente[9],
                                   "lineas_a_truncar": lista_fuente[10]
                                  } )

    lista_fuentes = anadir_fuentes_especiales(lista_fuentes)

    return lista_fuentes

###############################################
# Anadir lista_fuentes otras Fuentes especiales
###############################################

def anadir_fuentes_especiales(lf):
    for f in lista_fuentes_especiales:
        lf.append(f)

    return lf


##########################
# Leer utilmos enlaces
##########################

def get_ultimos():
    f = open(arch_ultimos)
    lista_archivo = f.readlines()
    f.close()

    lista_ultimos = {}

    for item in lista_archivo:
        item = item.rstrip()
        if ( item.startswith("#") == 0 ):
            lista_ultimo = item.split(";")

            #fuente;titulo
            lista_ultimos[lista_ultimo[0]] = lista_ultimo[1]

    return lista_ultimos

##########################
# Escribir utilmos enlaces
##########################

def set_ultimos(lista_texto):
    f = open(arch_ultimos, 'w')

    f.write("#fuente;titulo\n")

    for item in lista_texto:
        for key in item:
           #print key+";"+item[key]
           f.write(key+";"+item[key]+"\n")
    f.close()

###################################################################################################
# strip_tags() para quitar italicas, negritas, etc.
# http://stackoverflow.com/questions/1765848/remove-a-tag-using-beautifulsoup-but-keep-its-contents
###################################################################################################

def strip_tags(html_string, invalid_tags):
    html_soup = BeautifulSoup(html_string)

    for html_tag in html_soup.findAll(True):
        if html_tag.name in invalid_tags:
            s = ""

            for c in html_tag.contents:
                if not isinstance(c, NavigableString):
                    c = strip_tags(c, invalid_tags)
                s += c

    return s

##########
# Peticion
##########

def get_page(web_url):
    request = urllib2.Request(web_url, None, headers)
    resp = urllib2.urlopen(request)
    response = resp.read()

    return response

####################
# Procesar respuesta
####################

def get_stories(lf):

    titulos = defaultdict(list)

    lista_primeros = []
    lista_ultimos = get_ultimos()

    for item_fuente in lf:
        web_fuente              = item_fuente['fuente']
        web_url                 = item_fuente['url']
        web_sw_rama             = item_fuente['sw_rama']
        web_etiqueta_rama       = item_fuente['etiqueta_rama']
        web_atributo_rama       = item_fuente['atributo_rama']
        web_valor_rama          = item_fuente['valor_rama']
        web_etiqueta_elemento   = item_fuente['etiqueta_elemento']
        web_atributo_elemento   = item_fuente['atributo_elemento']
        web_valor_elemento      = item_fuente['valor_elemento']
        web_no_deseados         = item_fuente['no_deseados']
        web_lineas_a_truncar    = item_fuente['lineas_a_truncar']

        content = get_page(web_url)
        
        content_list = content.split('\n')

        # para depurar htmls que tengan lineas al principio de basura
        for i in range(0,int(web_lineas_a_truncar)):
            del content_list[0]

        soup = BeautifulSoup(''.join(content_list))

        # para controlar la primera noticia y no repetir
        sw_primero = 0
        sw_ultimo = 0

        # decidir si hay que buscar solo en una rama
        if web_sw_rama=="1":
            etiquetas = soup.find(web_etiqueta_rama, attrs={web_atributo_rama : web_valor_rama} ).findAll(web_etiqueta_elemento, attrs={web_atributo_elemento : re.compile(web_valor_elemento) })
        else:
            etiquetas = soup.findAll(web_etiqueta_elemento, attrs={web_atributo_elemento : re.compile(web_valor_elemento) } )

        for etiqueta in etiquetas:
            # Para quitar italicas, negritas, etc..
            if not isinstance(etiqueta.string, NavigableString):
                etiqueta_texto = ''.join(str(etiqueta.contents))
                etiqueta_texto = strip_tags(etiqueta_texto, invalid_tags)
            else:
                etiqueta_texto = etiqueta.string

            etiqueta_texto = etiqueta_texto.lstrip()

            # Para quitar los textos no deseados
            if re.search(web_no_deseados, etiqueta_texto):
                continue

            # Comprobar si el href es relativo
            if not re.search("http", etiqueta['href']):
                lista_url = web_url.split('/')
                del lista_url[-1]
                web_url_relative = '/'.join(lista_url) 
                etiqueta['href'] = web_url_relative+"/"+etiqueta['href']

            # Incluir en historico el primer enlace para no repetir noticias en futuros correos
            if sw_primero == 0:
                sw_primero = 1
                lista_primeros.append( {web_fuente: etiqueta_texto.encode('latin-1') } )
                
            # comprobar si esta repetido
            if web_fuente in lista_ultimos:
                if etiqueta_texto.encode('latin-1') == lista_ultimos[web_fuente]:
                    sw_ultimo = 1

            if sw_ultimo==0:
                # Para quitar cualquier javascript
                url_href = re.search(r'(https?:[/\w\.\-\?\_\:]*)', etiqueta['href'])
                # Para coger la extension
                lista_url_href = url_href.group(1).split(".")
                extension_url = lista_url_href[-1].upper()
                if extension_url=="HTML":
                    titulos[web_fuente+" - <a href='"+web_url+"'>e</a>"].append( { "titulo": etiqueta_texto.encode('latin-1')+" [HTML]", "url": "http://www.instapaper.com/text?u=" + url_href.group(1).encode('latin-1') } )
                elif extension_url=="PDF":
                    titulos[web_fuente+" - <a href='"+web_url+"'>e</a>"].append( { "titulo": etiqueta_texto.encode('latin-1')+" [PDF]", "url": url_href.group(1).encode('latin-1') } )
                else:
                    titulos[web_fuente+" - <a href='"+web_url+"'>e</a>"].append( { "titulo": etiqueta_texto.encode('latin-1')+" [URL]", "url": url_href.group(1).encode('latin-1') } )

    # Y la aleatoria de Wikipedia
    titulos["wikipedia aleatoria"].append( {"titulo": "aleatoria [URL]", "url": "http://es.wikipedia.org/wiki/Especial:Aleatoria"} )

    # Y la aleatoria de Wikiquote
    titulos["wikiquote aleatoria"].append( {"titulo": "aleatoria [URL]", "url": "http://es.wikiquote.org/wiki/Especial:Aleatoria"} )

    set_ultimos(lista_primeros)
   
    return titulos       

###################
# Crear cuerpo mail
###################

def crear_cuerpo_mail(tb):
    cuerpo_mail = BeautifulSoup()
    html = Tag(cuerpo_mail, "html")
    cuerpo_mail.append(html)

    cuerpo_mail.append("Enlaces:<br>\n")

    for fuente in tb:
        h3 = Tag(cuerpo_mail, "h3")
        cuerpo_mail.append(h3)
        h3.append(fuente)

        ul = Tag(cuerpo_mail, "ul")
        cuerpo_mail.append(ul)

        lista_titulos_fuente = tb[fuente]

        for i in lista_titulos_fuente:
            dict_enlace = i
            li = Tag(cuerpo_mail, "li")
            #li.append(fuente+","+dict_enlace['titulo'].decode('latin-1')+","+dict_enlace['url'].decode('latin-1'))
            li.append(dict_enlace['titulo'].decode('latin-1')+" - <a href='"+dict_enlace['url'].decode('latin-1')+"'>link</a>")
	    cuerpo_mail.append(li)

    return str(cuerpo_mail)

#################
# Envio de correo
#################

def send_mail(tb):
    now = datetime.datetime.now()
    # hoy = now.strftime("%Y-%m-%d %H:%M")
    dia = now.strftime("%A")
    hoy = dias[dia]+" "+now.strftime("%d/%m/%Y")

    
    subject = 'Resumen noticias ' + hoy
    to = mail_to

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to

    cuerpo = MIMEText(tb, 'html')
    msg.attach(cuerpo)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    smtpserver.sendmail(gmail_user, to, msg.as_string())
    smtpserver.close()

######
# Main
######

lista_fuentes = get_sources()
body = get_stories(lista_fuentes)
if body:
    html_body = crear_cuerpo_mail(body)
    send_mail(html_body)
else:
    print "Aqui no hay nada que ver...\n:(\n"
