FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY wait-for-it.sh /usr/src/app/
RUN chmod +x /usr/src/app/wait-for-it.sh

CMD ["/bin/sh", "-c", "./wait-for-it.sh neo4j_db:7687 -- python main.py"]
