FROM iron/base

MAINTAINER Mamadou Bobo Diallo <bobo.diaraye@gmail.com>

RUN echo "@testing \http://dl-4.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk update && apk upgrade \
  && apk add py-boto curl \
  && rm -rf /var/cache/apk/*

ADD bin/presence.py /bin/presence.py

RUN chmod u+x /bin/presence.py

ENTRYPOINT ["/bin/presence.py"]
CMD ["-h"]
