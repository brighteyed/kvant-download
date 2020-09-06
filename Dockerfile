FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV SCRAPY_SETTINGS_MODULE spiders.settings

COPY . .

CMD [ "python", "./main.py" ]
