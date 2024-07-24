FROM python:3.12.4-alpine

RUN apk add --no-cache python3-dev \
  && pip3 install --upgrade pip

WORKDIR /restful-organizer

COPY . /restful-organizer

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python", "src/app.py"]