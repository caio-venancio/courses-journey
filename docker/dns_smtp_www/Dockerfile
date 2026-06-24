FROM ubuntu:24.04

COPY setup_smtp.sh /setup_smtp.sh

RUN chmod +x /setup_smtp.sh

EXPOSE 25

CMD ["/setup_smtp.sh"]
