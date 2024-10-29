FROM python:3.11

WORKDIR /code

COPY . /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

WORKDIR /code
ENV PYTHONPATH=/usr/:/code

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]
