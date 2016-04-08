FROM ubuntu:15.10
RUN apt-get -y update
RUN apt-get -y install curl
RUN apt-get -y install git pkg-config
RUN apt-get -y install python
RUN apt-get -y install wget
RUN apt-get -y install build-essential libmagickwand-dev libopencv-dev
RUN wget https://raw.githubusercontent.com/videorooter/test-routines/master/utility/docker-run-tests.sh
RUN chmod +x docker-run-tests.sh
RUN ./docker-run-tests.sh https://github.com/jonasob/blockhash master
