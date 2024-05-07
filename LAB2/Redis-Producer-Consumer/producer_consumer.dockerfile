FROM python:3

COPY main.py ./main.py

RUN pip install redis
ENTRYPOINT [ "python3", "-u", "./main.py" ]
