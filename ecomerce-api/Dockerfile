FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get install --no-install-recommends -y openjdk-17-jre-headless curl \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
ENV PYSPARK_PYTHON=/usr/local/bin/python
ENV PYSPARK_DRIVER_PYTHON=/usr/local/bin/python
ENV SPARK_LOCAL_IP=127.0.0.1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD curl --fail --silent "http://127.0.0.1:${PORT:-8000}/health" || exit 1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
