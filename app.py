from src import init_app
import os

if __name__ == "__main__":
    app = init_app()
    app.run(port=int(os.environ.get("PORT", 5000)),host='0.0.0.0')