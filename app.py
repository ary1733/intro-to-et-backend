from src import init_app
import os

app = init_app()

if __name__ == "__main__":
    # this port 8080 will not be used if you run through gunicorn
    # use --bind=0.0.0.0:8080 as defualt port is 8000
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0')