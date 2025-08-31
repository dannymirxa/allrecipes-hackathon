FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY allrecipes.com_database_12042020000000.json .
COPY models/*.py models/
COPY modules/*.py modules/
COPY router/*.py router/
COPY schemas/*.py schemas/
COPY *.py .

EXPOSE 8001

CMD ["python", "server.py"]