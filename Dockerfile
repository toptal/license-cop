FROM python:3.8-slim

RUN pip3 install pipenv

USER root
WORKDIR /license-cop

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
COPY ./app ./app
COPY ./fixtures ./fixtures
COPY ./test ./test
COPY ./test.sh ./test.sh
COPY ./lint.sh ./lint.sh
COPY ./license-cop ./license-cop

ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN pipenv install
RUN pipenv install -d

ENV GITHUB_TOKEN "FAKE_TOKEN"

ENTRYPOINT ["./license-cop"]
