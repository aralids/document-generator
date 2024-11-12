# document-generator

## To run doc-gen on Linux:
- Open terminal in a directory chosen for the project.
- Enter `git clone https://github.com/aralids/document-generator.git`
- Enter `cd document-generator`
- Enter `docker build -t doc-gen .`
- Enter `docker run -p 8000:8000 doc-gen`
- You can now generate PDF files by using the user interface at `http://localhost:8000/` or by making POST requests to `http://localhost:8000/process_json` or `http://localhost:8000/process_json_with_preview`
