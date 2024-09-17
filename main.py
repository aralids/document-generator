from flask import Flask, render_template, request, Response
import json

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route("/process_json", methods=["POST"])
def process_json():
    f = request.files["json_file"].read()
    data = json.loads(f)
    print("request: ", request.files["json_file"].filename)
    return Response("Successful", status=201, mimetype='text/plain')

if __name__ == '__main__':
  app.run(port=5000)
