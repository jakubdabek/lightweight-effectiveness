FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y --no-install-recommends locales && \
    locale-gen en_US.UTF-8 && \
    apt install -y --no-install-recommends \
        openjdk-8-jdk openjdk-11-jdk maven \
        python3-pip \
        git ruby vim \
        && \
    apt clean && apt autoclean && apt autoremove && rm -rf /var/lib/apt/lists/*

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
# RUN echo 2 | python3 ./effectiveness/runner.py projects.csv clone && chmod +x get_projects.sh
COPY get-project.sh for-each-project.sh ./
RUN echo 'echo 2 | python3 ./effectiveness/runner.py projects.csv && chmod +x run_experiment*.sh' > make_runner.sh && chmod +x make_runner.sh

RUN echo 'export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")' >> ~/.bashrc

# only 3 first projects for testing
RUN sed -i 4q projects.csv

CMD ["bash"]