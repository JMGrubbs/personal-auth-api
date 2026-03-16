FROM python:3.13-slim

WORKDIR /app

COPY . /app

EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
