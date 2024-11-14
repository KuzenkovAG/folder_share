FROM python:3.12-alpine

RUN pip install pipenv

COPY Pipfile /opt/app/
COPY Pipfile.lock /opt/app/

WORKDIR /opt/app/
RUN pipenv install --ignore-pipfile

COPY /src /opt/app/

CMD ["pipenv", "run", "python", "main.py"]
