from flask import Flask, render_template, request, Response
import json
import sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from drawing_functions import draw_front_page, draw_3_slip_prints

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route("/process_json", methods=["POST"])
def process_json():

    # Load the JSON file.
    f = request.files["json_file"].read()
    data = json.loads(f)
    
    # Generate an empty PDF file in the "output" folder with 
    # the same name as the JSON file in the "input" folder.
    c = canvas.Canvas("./output/" + request.files["json_file"].filename[:-5] + ".pdf", pagesize=A4, bottomup=0)
    
    # Draw the front page.
    draw_front_page(c, "zbbskwug2", "06-08-2024 12:05")
    c.showPage()
    
    # Draw the slip prints, placing 3 per page.
    # (Or less on the last page, if len(data) % 3 != 0).
    for i in range(0, len(data), 3):
    	json_obj1 = data[i]
    	
    	json_obj2 = None
    	if (i + 1) <= (len(data) - 1):
    	    json_obj2 = data[i+1]
    	    
    	json_obj3 = None
    	if (i + 2) <= (len(data) - 1):
    	    json_obj3 = data[i+2]
    	    
    	draw_3_slip_prints(c, json_obj1, json_obj2, json_obj3)
    	c.showPage()
    	
    c.save()
    
    return Response("Successful", status=201, mimetype='text/plain')

if __name__ == '__main__':
  app.run(port=5000)
