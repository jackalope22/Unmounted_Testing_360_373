
FROM ubuntu:22.04
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt-get -y update && apt-get -y install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y install python3.10 && apt-get -y install pip 
RUN apt-get -y install libqt5network5
RUN pip install -r requirements.txt
RUN mkdir /storage
COPY . /app
ENTRYPOINT ["python3"]
CMD ["app.py"]
EXPOSE 0.0.0.0:5000:5000
EXPOSE 192.168.1.148:20481:20481
EXPOSE 192.168.1.148:20483:20483/udp
