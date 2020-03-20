FROM python:3.8

EXPOSE 80

WORKDIR /app
COPY . .

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["gunicorn", "main:app"]