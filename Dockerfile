# Lightweight Docker container for hosting files: mirrors the contents of a ZIP
# file in your Dropbox or Google Drive (or anywhere else, for that matter).

FROM phusion/baseimage:0.9.16
MAINTAINER olegv

RUN apt-get update
RUN apt-get -y install python
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /var/www
RUN mkdir -p /etc/service/simplefiledrop

COPY ./cloudzipproxyhost.py /usr/local/bin/cloudzipproxyhost.py
COPY ./simplefiledrop /etc/service/simplefiledrop/run

EXPOSE 80

CMD ["/sbin/my_init"]

