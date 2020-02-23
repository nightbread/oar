FROM python:alpine
WORKDIR /server
COPY . .
EXPOSE 8443
ENTRYPOINT python paddleapi_server.py --port 8443
