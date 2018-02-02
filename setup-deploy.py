#!/usr/env/python3
from string import Template
import sys
import io
import os

def deploy_site(nombre_dns, archivo_sitio, nombre_proyecto, carpeta_proyecto):
    # FICHERO APACHE2 SITE
    APACHE_SITE = archivo_sitio
    CONFIG_APACHE_SITE = open(APACHE_SITE, 'w')
    
    # DECLARO EL FICHERO TEMPLATE
    filein = open( 'template-site.conf' )
    
    # LEO EL FICHERO TEMPLATE
    src = Template( filein.read() )
    
    # RECOJO LAS VARIABLES Y LAS DECLARO
    PROJECT_NAME = nombre_proyecto
    PROJECT_FOLDER = carpeta_proyecto
    SERVER_NAME = nombre_dns
    ERROR_LOG = PROJECT_NAME+"_error.log combined"
    ACCESS_LOG = PROJECT_NAME+"_access.log"
    FILES_MATCH='<FilesMatch "\.(cgi|shtml|phtml|php)$">'
    
    d={ 'PROJECT_NAME': PROJECT_NAME, 'PROJECT_FOLDER': PROJECT_FOLDER, 'SERVER_NAME': SERVER_NAME, 'ERROR_LOG': ERROR_LOG, 'ACCESS_LOG': ACCESS_LOG, 'FILES_MATCH': FILES_MATCH }
    
    result = src.substitute(d)
    CONFIG_APACHE_SITE.write(result)
    CONFIG_APACHE_SITE.close()



#COMPRUEBO SI EL SITIO YA EXISTE O NO
if __name__ == '__main__':
    DNS=sys.argv[1]
    SITE_APACHE=sys.argv[2]
    NOMBRE_PROYECTO=sys.argv[3]
    CARPETA_PROYECTO=sys.argv[4]
    GIT_URL=sys.argv[5]
    if len(sys.argv) < 5:
        DB_NAME=sys.argv[6]
        DB_PASSWORD=sys.argv[7]

    if not os.path.isfile("/etc/apache2/sites-available/"+SITE_APACHE):
        deploy_site(DNS, SITE_APACHE, NOMBRE_PROYECTO, CARPETA_PROYECTO)
        os.system("sudo mv " + SITE_APACHE + " /etc/apache2/sites-available/")
        os.system("git clone " + GIT_URL + " /var/www/" + CARPETA_PROYECTO)
        os.system("virtualenv /var/www/" + CARPETA_PROYECTO)
    else:
        os.system("git --git-dir=/var/www/" + CARPETA_PROYECTO + "/.git --work-tree=/var/www/" + CARPETA_PROYECTO + "/.git pull") 

    os.system("source /var/www/" + CARPETA_PROYECTO + "/bin/activate") 
    os.system("pip3 install -r /var/www/" + CARPETA_PROYECTO + "/requirements.txt ")
    if DB_NAME && DB_PASSWORD:
        os.system("mysql -uroot -p"+DB_PASSWORD + " -e CREATE DATABASE " + DB_NAME + ";")
	os.system("sudo a2ensite" + SITE_APACHE)
    os.system("sudo service apache2 restart")


# EJEMPLO DE USO: python3 setup-deploy.py hole.wolfcrass.com hole mysite hola http://crromano:F_50613dkm@github.com/crromano/sysadminscripts/ 
