FROM python:latest

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

ENTRYPOINT ["python3","-m","uvicorn","main:app","--host","0.0.0.0","--port","8000"]