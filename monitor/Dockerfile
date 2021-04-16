FROM python:3.7

EXPOSE 5000

COPY ./requirements.txt /scraper/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /monitor
WORKDIR /monitor




CMD python monitor.py
