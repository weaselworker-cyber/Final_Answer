FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    python3.8 \
    python3-pip \
    mysql-server && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]