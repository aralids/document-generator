from fastapi import FastAPI, Response, Request, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

import json
from io import BytesIO
import math
from datetime import datetime
import base64

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


from drawing_functions import draw_front_page, draw_3_slip_prints
from config import use_mapping

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post("/process_json_with_preview")
async def process_json(request: Request, background_tasks: BackgroundTasks):
    form = await request.form()
    #filename = form['json_file'].filename 
    
    # Load the JSON file.
    f = await form['json_file'].read()
    data = json.loads(f)
    
    # Generate an empty PDF file in the "output" folder with 
    # the same name as the JSON file in the "input" folder.
    bfr = BytesIO()
    c = canvas.Canvas(bfr, pagesize=A4, bottomup=0)
    
    # Draw the front page.
    group = data[0]["print_group_name"]
    service_point = use_mapping["service_points"][group]
    layout = use_mapping["layouts"][group]
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M")
    draw_front_page(c, " ".join(group.split(" ")[1:]), timestamp)
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
    	    
    	draw_3_slip_prints(c, service_point, layout, json_obj1, json_obj2, json_obj3)
    	c.showPage()
    	
    c.save()
    
    background_tasks.add_task(bfr.close)
    pdf = bfr.getvalue()
    
    pdf_b64 = base64.b64encode(pdf).decode("utf-8")
  
    return templates.TemplateResponse('preview.html', {'request': request, "pdf_file": pdf_b64})
    #headers = {'Content-Disposition': 'attachment; filename="output.pdf"'}
    #return Response(pdf, headers=headers, media_type='application/pdf')

@app.post("/process_json")
async def process_json(request: Request, background_tasks: BackgroundTasks):
    form = await request.form()
    #filename = form['json_file'].filename 
    
    # Load the JSON file.
    f = await form['json_file'].read()
    data = json.loads(f)
    
    # Generate an empty PDF file in the "output" folder with 
    # the same name as the JSON file in the "input" folder.
    bfr = BytesIO()
    c = canvas.Canvas(bfr, pagesize=A4, bottomup=0)
    
    # Draw the front page.
    group = data[0]["print_group_name"]
    service_point = use_mapping["service_points"][group]
    layout = use_mapping["layouts"][group]
    now = datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M")
    draw_front_page(c, " ".join(group.split(" ")[1:]), timestamp)
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
    	    
    	draw_3_slip_prints(c, service_point, layout, json_obj1, json_obj2, json_obj3)
    	c.showPage()
    	
    c.save()
    
    background_tasks.add_task(bfr.close)
    pdf = bfr.getvalue()
  
    headers = {'Content-Disposition': 'inline; filename="output.pdf"'}
    return Response(pdf, headers=headers, media_type='application/pdf')
