FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install numpy

EXPOSE 65432

CMD ["python", "slave_server.py"]
