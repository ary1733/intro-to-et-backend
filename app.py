from src import init_app
import os
from flask_cors import cross_origin

app = init_app()

@app.route("/")
@cross_origin()
def helloWorld():
  return "Hello, cross-origin-world!"

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0')