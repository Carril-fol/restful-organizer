FROM python:3.10-alpine

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev python3-dev

RUN pip3 install --upgrade pip

WORKDIR /backend

COPY . /backend

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "src/app.py"]
