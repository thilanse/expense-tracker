FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN mkdir pg_data
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/