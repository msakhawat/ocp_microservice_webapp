FROM centos:centos8

RUN yum -y update && yum -y install python3

COPY . /app
WORKDIR /app
RUN pip3 install -r requirments.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000

CMD ["flask", "run"]

# FROM mypython
# COPY ./src .
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# CMD ["flask", "run"]