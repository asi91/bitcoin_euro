FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]