FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get clean 

COPY ./server .
COPY ./ui/dist /app/static

EXPOSE 8000

RUN pip install -r requirements.txt

CMD uvicorn api.ws:app --host 0.0.0.0 --port 8000 --reload
