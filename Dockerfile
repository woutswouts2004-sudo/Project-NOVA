FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NOVA_HOME=/app \
    NOVA_ENABLE_EXTERNAL_MODEL=NO
WORKDIR /app
RUN groupadd -g 10001 nova && useradd -u 10001 -g nova -M nova
COPY --chown=nova:nova . /app
RUN mkdir -p /app/data /app/workspace && chown -R nova:nova /app
USER nova
CMD ["python", "-m", "project_nova", "--loop", "--interval", "3600"]
