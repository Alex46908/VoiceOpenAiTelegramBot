FROM python:3.12-slim

WORKDIR /app

COPY src/ ./src

COPY requirements.txt .
COPY alembic.ini .

RUN pip install -r requirements.txt

CMD ["alembic upgrade head"]

CMD ["python", "./src/main.py"]