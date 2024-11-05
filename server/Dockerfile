FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y curl gnupg2 ca-certificates lsb-release && apt-get clean 
RUN curl -sSL https://install.python-poetry.org | python3 - 

COPY ./server .
COPY ./ui/dist /app/static

RUN poetry install --no-root

EXPOSE 8000

CMD poetry run uvicorn api.ws:app --host 0.0.0.0 --port 8000 --reload
