FROM python:3.10.6

WORKDIR /code


ADD ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

CMD ["uvicorn","app.main:app", "--host", "0.0.0.0","--port","8000"]