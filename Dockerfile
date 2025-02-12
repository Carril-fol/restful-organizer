FROM python:3.13.2-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

WORKDIR /backend

COPY requirements.txt /backend/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /backend

EXPOSE 8000

CMD ["python", "src/app.py"]