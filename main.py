from flask import Flask, render_template, request, Response
import json
import sys
import math
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
    
    # Sorting.
    # If the JSON file contains 5 objects numbered 0 to 4,
    # these are sorted as 4,2,0 - EMPTY,3,1 on 2 pages.
    page_num = math.ceil(len(data) / 3)
    for i in range(0, page_num):
    	json_obj1 = data[i]
    	
    	json_obj2 = None
    	if (i + page_num) <= (len(data) - 1):
    	    json_obj2 = data[i+page_num]
    	    
    	json_obj3 = None
    	if (i + 2*page_num) <= (len(data) - 1):
    	    json_obj3 = data[i+2*page_num]
    	    
    	draw_3_slip_prints(c, json_obj1, json_obj2, json_obj3)
    	c.showPage()
    	
    c.save()
    
    return Response("Successful", status=201, mimetype='text/plain')

if __name__ == '__main__':
  app.run(port=5000)
