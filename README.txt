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

./venv/bin/activate # activate virtual env
gunicorn --workers=3 app:app --daemon # start 3 gunicorn wokers in background






https://www.digitalocean.com/community/tutorials/install-tomcat-9-ubuntu-1804
after installing tomcat copy the WAR file in CATALINA_HOME/webapps folder
check ports with netstat -tulpen
