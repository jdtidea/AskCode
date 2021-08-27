FROM docker.repo1.uhc.com/tiangolo/uvicorn-gunicorn:python3.8

# Azure AppServices SSH Stuff
ENV SSH_PORT 2222

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openssh-server \
        vim \
        curl \
        wget \
        tcptraceroute

# setup SSH
RUN mkdir -p /home/LogFiles \
     && echo "root:Docker!" | chpasswd \
     && echo "cd /home" >> /etc/bash.bashrc

COPY sshd_config /etc/ssh/
RUN mkdir -p /opt/startup
# End Azure BS

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV MODULE_NAME "app"
ENV APP_MODULE "app.main:app"
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV PRE_START_PATH="/backend/prestart.sh"
ENV LOG_LEVEL="debug"
#ENV ACCESS_LOG="access.log"
#ENV ERROR_LOG="error.log"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./prestart.sh ./pyproject.toml ./poetry.lock* /backend/

RUN poetry install --no-root --no-dev
COPY . /backend
