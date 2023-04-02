from src import init_app
import os
from flask_cors import CORS

app = init_app()
CORS(app,resources={r'*':{'origins':'*','supports_credentials':True}})
if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0')