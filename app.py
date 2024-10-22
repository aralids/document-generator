from fastapi import FastAPI, Response, Request, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
import json
import sys
from io import BytesIO
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from drawing_functions import draw_front_page, draw_3_slip_prints

app = FastAPI()

@app.get("/")
async def root():
    html_content = """
    	<!DOCTYPE html>
	<html>
	  <head>
	    <title>Hello World</title>
	  </head>
	  <body>
	    <h1>Hello World!</h1>
	    <form method="post" enctype="multipart/form-data" action="/process_json">
	    <p>
		<label>Add file (single): </label><br/>
		<input type="file" name="json_file"/>
	    </p>
	    <p>
		<input type="submit"/>
	    </p>
	</form>
	  </body>
	</html>
    """
    return HTMLResponse(content=html_content, status_code=200)

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
    
    background_tasks.add_task(bfr.close)
    pdf = bfr.getvalue()
    
    headers = {'Content-Disposition': 'inline; filename="out.pdf"'}
    return Response(pdf, headers=headers, media_type='application/pdf')
