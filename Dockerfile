FROM python:3.9-slim

RUN apt-get update && apt-get install -y make

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN make build
RUN make install

ENTRYPOINT ["tail", "-f", "/dev/null"]
