FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NOVA_BIND=0.0.0.0 \
    NOVA_PORT=8080
WORKDIR /app
RUN groupadd -g 10001 nova && useradd -u 10001 -g nova -M nova
COPY --chown=nova:nova project_nova /app/project_nova
COPY --chown=nova:nova policy /app/policy
USER nova
EXPOSE 8080
CMD ["python", "-m", "project_nova.public_api"]
