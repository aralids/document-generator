# document-generator

The instructions below assume that Python and pip are installed on the machine.

> [!IMPORTANT]  
> Please delete your document-generator folder if you have downloaded it before.

## To install on Windows:
- Open terminal in a directory chosen for the project.
- Make sure you have the virtualenv package installed by entering `pip install virtualenv`.
- Enter `git clone https://github.com/aralids/document-generator.git`.
- Enter `cd document-generator`.
- Enter `python -m venv venv` (to create a virtual environment).
- Enter `venv\scripts\activate.bat` (to activate the virtual environment).
- Enter `pip install -r requirements.txt` (to install all dependencies in the virtual environment only).

## To run on Windows:
- Open terminal in the document-generator folder.
- Enter `venv\scripts\activate.bat`.
- Enter `fastapi dev main.py`.
- Open `http://127.0.0.1:8000` in browser to try out the app. 

## To install on Linux:
- Open terminal in a directory chosen for the project.
- Make sure you have the virtualenv package installed by entering `pip install virtualenv`.
- Enter `git clone https://github.com/aralids/document-generator.git`.
- Enter `cd document-generator`.
- Enter `python -m venv venv` (to create a virtual environment).
- Enter `source venv/bin/activate` (to activate the virtual environment).
- Enter `pip install -r requirements.txt` (to install all dependencies in the virtual environment only).

## To run on Linux:
- Open terminal in the document-generator folder.
- Enter `source venv/bin/activate`.
- Enter `fastapi dev main.py`.
- Open `http://127.0.0.1:8000` in browser to try out the app. 

> [!NOTE]  
> Currently, the app is set up to respond to POST requests with an automatic download of the pdf output. To change this and receive the pdf as a regular API response, modify main.py by replacing line 89 with `headers = {'Content-Disposition': 'inline; filename="output.pdf"'}`. 
