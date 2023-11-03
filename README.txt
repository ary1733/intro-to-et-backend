gunicorn --workers=3 --bind=0.0.0.0:8000 app:app --daemon
source venv/bin/activate
sudo nano /etc/nginx/sites-enabled/flask-app
sudo nginx -t
sudo nginx -s reload
pkill -f gunicorn
netstat -tulpen # tellls info about ports with PID




###### steps ######
video link : https://www.youtube.com/watch?v=BpcK5jON6Cg&list=PLAzYRZdu7iYkCCeX56bnh9vIyQSgVBxNK&index=4&t=410s

git pull

cp .env.example .env  #create .env file using .env.example
nano .env #and fill the correct values

mysql -u root -p # login in mysql and create database, drop tables etc. if required
USE todolist; # use db_name
show tables;
drop table users;

ps ax|grep gunicorn # get all gunicorn workers
pkill gunicorn # kill all the current gunicorn instances/workers

source ./venv/bin/activate # activate virtual env
pip install -r requirements.txt # if requried
gunicorn --workers=3 app:app --daemon # start 3 gunicorn wokers in background





####### install tomcat in ubuntu
https://www.digitalocean.com/community/tutorials/install-tomcat-9-ubuntu-1804
after installing tomcat copy the WAR file in CATALINA_HOME/webapps folder
check ports with netstat -tulpen


####### link to install postgis
https://gis.stackexchange.com/questions/71302/running-create-extension-postgis-gives-error-could-not-open-extension-control-fi
CREATE ROLE myuser LOGIN PASSWORD 'mypass';
CREATE DATABASE mydatabase WITH OWNER = myuser;
ALTER ROLE myuser SUPERUSER;
psql -h localhost -d mydatabase -U myuser -p 5432


####### disable csrf Geoserver
https://gis.stackexchange.com/questions/385106/unable-to-add-layer-to-geoserver-origin-does-not-correspond-to-request