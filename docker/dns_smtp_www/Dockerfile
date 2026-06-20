FROM ubuntu:24.04

RUN apt-get update \
	&& apt-get upgrade -y \
	&& rm -rf /var/lib/apt/lists/*

COPY setup_[www.sh](http://www.sh) /setup_[www.sh](http://www.sh)

RUN chmod +x /setup_[www.sh](http://www.sh)

EXPOSE 80

CMD ["/setup_[www.sh](http://www.sh)"]
