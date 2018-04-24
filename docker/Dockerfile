# https://hub.docker.com/_/debian/
FROM debian:stretch

ENV DEBIAN_FRONTEND noninteractive

# update repository info and data and configure locales
RUN sed -i "s/stretch main/stretch main contrib non-free/" /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends locales \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen \
    && update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 \
    && localedef -c -i ru_RU -f UTF-8 ru \
    && localedef -c -i ru_RU -f UTF-8 ru_RU \
    && localedef -c -i en_US -f UTF-8 en \
    && localedef -c -i en_US -f UTF-8 en_US

# change default locale in environment
ENV LANG=en_US.UTF-8 LANGUAGE=en_US:en LC_ALL=en_US.UTF-8

# install system packages required by snitch
RUN apt-get install -y --no-install-recommends \
    python3 \
    python3-venv \
    python3-pip \
    python3-setuptools \
    python3-dev \
    postgresql-client-9.6 \
    && apt-get clean autoclean \
    && apt-get autoremove --yes

RUN pyvenv-3.5 /srv/snitch/.env \
    && /srv/snitch/.env/bin/pip install --upgrade pip \
    && /srv/snitch/.env/bin/pip install --upgrade setuptools wheel \
    && chmod 777 /srv/snitch \
    && find /srv/snitch/ -type d -exec chmod 777 {} \; \
    && find /srv/snitch/ -type f -exec chmod 777 {} \; \
    && ls -laR /srv/snitch > /tmp/output

ENV DEBIAN_FRONTEND teletype

CMD ["sleep infinity & wait"]
