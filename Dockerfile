FROM ubuntu:20.04@sha256:5403064f94b617f7975a19ba4d1a1299fd584397f6ee4393d0e16744ed11aab1

ARG DEBIAN_FRONTEND=noninteractive

COPY apt-install-all-clean.sh ./
RUN apt update && \
    apt install -y --no-install-recommends locales && \
    locale-gen en_US.UTF-8 && \
    ./apt-install-all-clean.sh \
        openjdk-8-jdk openjdk-11-jdk maven \
        python3-pip python3-venv \
        git subversion ruby vim

RUN update-java-alternatives --set java-1.8.0-openjdk-amd64

WORKDIR /root/experiments

COPY requirements.txt ./
RUN python3 -m pip install --upgrade pip setuptools

RUN python3 -m pip install -r requirements.txt

# copy scripts
COPY effectiveness/ ./effectiveness
# copy dir with stats and code for metrics
COPY metrics/ ./metrics
COPY projects.csv ./

ENV PYTHONPATH="$PWD:$PYTHONPATH"
COPY get-project.sh for-each-project.sh make-runner.sh ./

RUN echo 'export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")' >> ~/.bashrc

# only 4 first projects for testing
RUN sed -i 5q projects.csv

CMD ["bash"]
