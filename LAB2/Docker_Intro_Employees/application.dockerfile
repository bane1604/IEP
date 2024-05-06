FROM python:3

COPY config.py /config.py
COPY model.py /model.py
COPY main.py /main.py
COPY requirements.txt /requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT [ "python", "main.py" ]