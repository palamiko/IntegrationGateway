FROM python:3.11.3-slim

WORKDIR /application

COPY ./requirements.txt /application/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /application/requirements.txt

EXPOSE 9991

COPY ./app /application/app

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "9991"]