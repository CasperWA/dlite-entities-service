FROM python:3.10 as base

WORKDIR /app

COPY dlite_entities_service dlite_entities_service/
COPY pyproject.toml LICENSE README.md ./

# Install dependencies
RUN python -m pip install -U pip && \
  pip install -U pip setuptools wheel flit && \
  pip install -U -e . && \
  # Create log directory and file (if not existing already)
  mkdir -p logs && \
  touch -a logs/dlite_entities_service.log

FROM base as development

ENV PORT=80
EXPOSE ${PORT}

ENV ENTITY_SERVICE_DEBUG=1

ENTRYPOINT uvicorn --host 0.0.0.0 --port ${PORT} --log-level debug --no-server-header --header "Server:DLiteEntitiesService" --reload dlite_entities_service.main:APP

FROM base as production

RUN pip install -U --upgrade-strategy=eager -e .[production]

ENV PORT=80
EXPOSE ${PORT}

ENV ENTITY_SERVICE_DEBUG=0

ENTRYPOINT gunicorn --bind "0.0.0.0:${PORT}" --workers 1 --worker-class dlite_entities_service.uvicorn.UvicornWorker dlite_entities_service.main:APP
