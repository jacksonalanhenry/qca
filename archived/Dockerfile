 FROM ubuntu:22.04
 RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
 RUN apt-get update && apt-get install -y python3-tk python3-pip libx11-dev
 RUN pip3 install matplotlib pytest
 COPY ./ /qca
 WORKDIR /qca
 CMD /bin/bash
