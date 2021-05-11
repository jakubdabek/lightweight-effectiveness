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

# universal ctags, used by OpenGrok
RUN ./apt-install-all-clean.sh \
    gcc make \
    pkg-config autoconf automake \
    python3-docutils \
    libseccomp-dev \
    libjansson-dev \
    libyaml-dev \
    libxml2-dev \
    mercurial cssc cvs brz
RUN git clone https://github.com/universal-ctags/ctags.git && \
    cd ctags && git checkout 0d87063f3ee55198c1d29e1aa1da7c5fded393d5 && \
    ./autogen.sh  && \
    ./configure && \
    make -j4 && \
    make install

ARG USER=ubuntu
ARG UID=1000

RUN useradd --uid ${UID} --gid root --groups sudo --create-home --shell /bin/bash ${USER}
RUN ./apt-install-all-clean.sh sudo
RUN echo "#${UID}     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER ${UID}
WORKDIR /home/${USER}/experiments

COPY --chown=${UID} requirements.txt ./
RUN python3 -m pip install --user --upgrade pip setuptools
RUN python3 -m pip install --user -r requirements.txt

# dev debug packages
RUN sudo /apt-install-all-clean.sh tmux tree less file

# copy dir with stats and code for metrics
COPY --chown=${UID} metrics/ ./metrics
COPY --chown=${UID} projects.csv ./

COPY --chown=${UID} patches/ ./patches
COPY --chown=${UID} get-project.sh for-each-project.sh run-everything.sh create-classifier.sh ./

# copy scripts
COPY --chown=${UID} effectiveness/ ./effectiveness

RUN echo 'export JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")' >> ~/.bashrc
RUN echo 'export PYTHONPATH="${HOME}/experiments:${PYTHONPATH}"' >> ~/.bashrc

# only 4 first projects for testing
RUN sed -i 5q projects.csv

CMD ["bash", "--login"]
