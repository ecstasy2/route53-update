FROM ubuntu:14.04
MAINTAINER Daniel Schonfeld <downwindabeam@gmail.com>

RUN apt-get -q update && apt-get install -y python-boto curl nano

ADD bin/presence.py /bin/presence.py

RUN chmod u+x /bin/presence.py

ENTRYPOINT ["/bin/presence.py"]
CMD ["-h"]
