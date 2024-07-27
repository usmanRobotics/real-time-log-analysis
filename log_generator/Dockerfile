FROM python:3.8-slim
WORKDIR /app
COPY log_generator.py /app/
RUN mkdir -p /app/logs
CMD ["python", "log_generator.py"]