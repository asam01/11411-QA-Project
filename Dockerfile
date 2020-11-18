# Ubuntu Linux as the base image
FROM ubuntu:18.04

# Set UTF-8 encoding
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install Python
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install python3-pip python3-dev

# Install everything
RUN pip3 install --upgrade pip
RUN pip3 install spacy==2.3.0
RUN pip3 install tensorboard==1.14.0
RUN pip3 install tensorboard-plugin-wit==1.7.0
RUN pip3 install tensorflow==1.14.0
RUN pip3 install tensorflow-estimator==1.14.0
RUN pip3 install nltk==3.5
RUN pip3 install beautifulsoup4==4.9.3
RUN pip3 install cymem==2.0.4
RUN pip3 install Cython==0.29.21
RUN pip3 install preshed==3.0.2
RUN pip3 install thinc==7.4.1
RUN pip3 install benepar==0.1.2
RUN python3 -m spacy download en_core_web_lg
RUN python3 -m spacy download en_core_web_sm
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader stopwords  

# Add the files into container, under QA folder, modify this based on your need
ADD asking /QA
ADD answering /QA
ADD preprocess /QA
ADD neuralcoref /QA
ADD __init__.py /QA
ADD requirements.txt /QA

# Change the permissions of programs
CMD ["chmod 777 /QA/*"]

# Set working dir as /QA
WORKDIR /QA
ENTRYPOINT ["/bin/bash", "-c"]