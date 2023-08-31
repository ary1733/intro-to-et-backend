gunicorn --workers=3 --bind=0.0.0.0:8000 app:app --daemon
source venv/bin/activate
sudo nano /etc/nginx/sites-enabled/flask-app
sudo nginx -t
sudo nginx -s reload
pkill -f gunicorn