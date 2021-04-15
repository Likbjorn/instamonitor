FROM python:3.7

EXPOSE 5000

RUN mkdir /instamonitor
WORKDIR /instamonitor

COPY . /instamonitor
RUN pip install --no-cache-dir -r requirements.txt

CMD python monitor.py