FROM ubuntu:22.04

RUN apt-get update -y && \
    apt-get install -y python3-pip

COPY api /api
COPY requirements.txt /api/requirements.txt

ENV PYTHONPATH=.

RUN pip3 install -r /api/requirements.txt

RUN chmod +x /api/run.py

EXPOSE ${api_port:-8000}

CMD ["python3", "/api/run.py"]