FROM python:3.10

COPY . /usr/src/app/
WORKDIR /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]