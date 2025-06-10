FROM openjdk:8-jdk-alpine
RUN apk add --no-cache bash wget
WORKDIR /tez
RUN wget https://downloads.apache.org/tez/0.10.2/apache-tez-0.10.2-bin.tar.gz \
    && tar -xzf apache-tez-0.10.2-bin.tar.gz \
    && mv apache-tez-0.10.2/* .
ENV TEZ_HOME=/tez
ENV PATH=$PATH:$TEZ_HOME/bin