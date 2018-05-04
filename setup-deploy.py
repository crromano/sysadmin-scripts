#!/usr/bin/python3
from string import Template
import sys
import io
import os
import json
import pip
import virtualenv
import runpy

def deploy_site(nombre_dns, archivo_sitio, nombre_proyecto, carpeta_proyecto):
    # FICHERO APACHE2 SITE
    APACHE_SITE = archivo_sitio
    CONFIG_APACHE_SITE = open(APACHE_SITE, 'w')
    
    # DECLARO EL FICHERO TEMPLATE
    filein = open( '/home/ubuntu/sysadmin-scripts/template-site.conf' )
    
    # LEO EL FICHERO TEMPLATE
    src = Template( filein.read() )
    
    # RECOJO LAS VARIABLES Y LAS DECLARO
    PROJECT_NAME = nombre_proyecto
    PROJECT_FOLDER = carpeta_proyecto
    SERVER_NAME = nombre_dns
    ERROR_LOG = PROJECT_NAME+"_error.log"
    ACCESS_LOG = PROJECT_NAME+"_access.log combined"
    FILES_MATCH='<FilesMatch "\.(cgi|shtml|phtml|php)$">'
    
    d={ 'PROJECT_NAME': PROJECT_NAME, 'PROJECT_FOLDER': PROJECT_FOLDER, 'SERVER_NAME': SERVER_NAME, 'ERROR_LOG': ERROR_LOG, 'ACCESS_LOG': ACCESS_LOG, 'FILES_MATCH': FILES_MATCH }
    
    result = src.substitute(d)
    CONFIG_APACHE_SITE.write(result)
    CONFIG_APACHE_SITE.close()


#COMPRUEBO SI EL SITIO YA EXISTE O NO
if __name__ == '__main__':
    
    GIT_URL=sys.argv[1]
    CARPETA_PROYECTO=GIT_URL[::-1][(GIT_URL[::-1].find("/")) - 1 ::-1]
    if os.path.isdir("/var/www/"+CARPETA_PROYECTO):
        os.system("sudo rm -r /var/www/" + CARPETA_PROYECTO)

    os.system("git clone " + GIT_URL + " /var/www/" + CARPETA_PROYECTO)
    os.system("sudo chmod -R 777 /var/www/" + CARPETA_PROYECTO)
    virtualenv.create_environment("/var/www/" + CARPETA_PROYECTO + "/.")
    runpy.run_path('/var/www/' + CARPETA_PROYECTO + '/bin/activate_this.py')
    os.system("pip3 install -r /var/www/" + CARPETA_PROYECTO + "/requirements.txt")

    with open('/var/www/' + CARPETA_PROYECTO + '/params.json') as file:
        data=json.load(file)
    
    DNS=data.get('DNS')
    SITE_APACHE=data.get('SITE_APACHE')
    NOMBRE_PROYECTO=data.get('NOMBRE_PROYECTO')
    DB_NAME=data.get('DB_NAME')
    DB_PASSWORD=data.get('DB_PASSWORD')
    P_NAME = NOMBRE_PROYECTO[:NOMBRE_PROYECTO.find("_")+1] + "project"
    PYTHON_V = "python{0}.{1}".format(sys.version_info.major, sys.version_info.minor)
    os.system("cp -R /var/www/" + CARPETA_PROYECTO + "/lib/" + PYTHON_V + "/site-packages/django/contrib/admin/static/admin/ /var/www/" + CARPETA_PROYECTO + "/" + P_NAME + "/static/")
    if not os.path.isfile("/etc/apache2/sites-available/"+SITE_APACHE):
        deploy_site(DNS, SITE_APACHE, NOMBRE_PROYECTO, CARPETA_PROYECTO)
        os.system("sudo mv " + SITE_APACHE + " /etc/apache2/sites-available/")
     
    if DB_NAME != 0:
        os.system('mysql -uroot  -e "CREATE DATABASE ' + DB_NAME + '"' + ' -p"'+DB_PASSWORD+'";')
        os.system("mysql -uroot -p"+DB_PASSWORD + " " + DB_NAME + " < /var/www/" + CARPETA_PROYECTO + "/scripts/initial_inserts.sql")	
    os.system("sudo a2ensite " + SITE_APACHE)
    os.system("sudo service apache2 restart")

