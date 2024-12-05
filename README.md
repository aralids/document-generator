# document-generator

## To run doc-gen on Linux:
- Enter `docker build -t doc-gen .`
- Enter `docker run -p 9000:9000 doc-gen`
- You can now generate PDF files by using the user interface at `http://localhost:9000/` or by making POST requests to `http://localhost:9000/pdf`
