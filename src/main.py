from fastapi import FastAPI, Response, Request, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from drawing_functions import create_pdf

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post("/process_json_with_preview")
async def process_json(request: Request, background_tasks: BackgroundTasks):
    form = await request.form()
    f = await form['json_file'].read()
    data = json.loads(f)
    
    pdf = create_pdf(data, background_tasks)
    pdf_b64 = base64.b64encode(pdf).decode("utf-8")
    return templates.TemplateResponse('preview.html', {'request': request, "pdf_file": pdf_b64})

@app.post("/")
@app.post("/pdf")
@app.post("/process_json")
async def process_json(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    pdf = create_pdf(data, background_tasks)
    return Response(pdf, headers={'Content-Disposition': 'inline; filename="output.pdf"'}, media_type='application/pdf')
