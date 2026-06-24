docker run --rm -it -p 8080:80 -v "${PWD}:/app" ubuntu:24.04 bash /app/setup_www.sh
docker run --rm -it -p 2525:25 -v "${PWD}:/app" ubuntu:24.04 bash /app/setup_smtp.sh
docker run --rm -it -p 53:53/tcp -p 53:53/udp -v "${PWD}:/app" ubuntu:24.04 bash