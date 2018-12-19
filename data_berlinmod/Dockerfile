FROM ubuntu:16.04

RUN apt-get update && \
    apt-get -y install sudo
ADD http://dna.fernuni-hagen.de/secondo/files/Installation/Ubuntu/InstallSDK_Ubuntu_16_04.bash /InstallSDK_Ubuntu_16_04.bash
RUN bash /InstallSDK_Ubuntu_16_04.bash
RUN rm /InstallSDK_Ubuntu_16_04.bash
RUN echo "source $HOME/.secondorc $HOME/secondo" >> $HOME/.bashrc
ADD http://dna.fernuni-hagen.de/Secondo.html/files/Sources/secondo-v412-LAT1.tgz /secondo-v412-LAT1.tgz
RUN tar xzf /secondo-v412-LAT1.tgz -C $HOME
RUN rm /secondo-v412-LAT1.tgz
RUN cd $HOME/secondo/ && \
    cat makefile
