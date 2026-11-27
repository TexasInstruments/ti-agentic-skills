# Behind a corporate proxy or mirror, override at build time:
#   docker build --build-arg BASE_IMAGE=<mirror>/python:3.11-slim \
#                --build-arg HTTP_PROXY=http://<proxy>:<port> --build-arg HTTPS_PROXY=http://<proxy>:<port> .
ARG BASE_IMAGE=python:3.11-slim
FROM ${BASE_IMAGE}

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

ENV TI_PROCESSOR_SDK_DEFAULT_DEVICE=AM62X
ENV TI_PROCESSOR_SDK_DEFAULT_OS=linux
ENV TI_PROCESSOR_SDK_MCP_PORT=7471

EXPOSE 7471

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python3 -c "import socket; socket.create_connection(('localhost', 7471), 2).close()" || exit 1

CMD ["python3", "server.py", "--http", "7471"]
