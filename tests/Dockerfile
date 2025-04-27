FROM python:3.12-alpine
ENV TZ "Europe/Moscow"
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev zbar zbar-dev postgresql-client
RUN python -m pip install --upgrade pip
ADD api/requirements.txt api/
RUN pip install -U -r api/requirements.txt
ADD tests/requirements.txt tests/
RUN pip install -U -r tests/requirements.txt
ADD . .
CMD ["pytest", "-v", "tests/"]
