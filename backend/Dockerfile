FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY cfp /app/cfp

ENV FLASK_CONFIG "docker"

RUN ls

EXPOSE 5000


CMD ["python", "-m", "cfp.wsgi"]
