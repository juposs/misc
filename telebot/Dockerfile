FROM python
COPY requirements.txt /
COPY telebot.py /
COPY bistro_class.py /
#RUN apk add --update musl-dev gcc
RUN pip install -r /requirements.txt
CMD ["python3", "telebot.py"]