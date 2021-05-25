FROM python:3

RUN pip install secure-smtplib requests pytz

ADD vaccine.py /
ADD config.py /

ENTRYPOINT python3 vaccine.py os.environ['DISTRICT'] os.environ['EMAIL']