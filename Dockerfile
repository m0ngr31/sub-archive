FROM python:3.8-alpine

RUN mkdir /app
WORKDIR /app

COPY . .

RUN \
  cd /app && \
  pip install gunicorn && \
  pip install -r requirements.txt && \
  chmod +x serve.sh

EXPOSE 5000
ENTRYPOINT "./serve.sh"