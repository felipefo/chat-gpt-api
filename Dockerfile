FROM python:3.8


COPY . /app
WORKDIR /app


RUN mkdir __logger


# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "./askgpt_firefox.py"]