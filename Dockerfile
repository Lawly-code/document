FROM python:3.12-alpine
ENV TZ "Europe/Moscow"
WORKDIR /home/api
RUN apk update
RUN apk add git
RUN python -m pip install --upgrade pip
ADD requirements.txt .
RUN pip install -U -r requirements.txt
ADD .. .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
