FROM python:3
ENV PYTHONUNBUFFERED=1

RUN mkdir pg_data

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

#COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "entrypoint.sh"]