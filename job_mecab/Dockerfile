FROM centos
MAINTAINER Masa <dev.roomsso.net@gmail.com>
USER root
ENV LC_ALL C
ENV LANG ja_JP.UTF-8
ENV PYTHONIOENCODING utf-8
RUN yum install -y bzip2 zip git gcc-c++ make python-devel && \
    yum localinstall -y http://mirror.centos.org/centos/6/os/x86_64/Packages/nkf-2.0.8b-6.2.el6.x86_64.rpm && \
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv && \
    curl -kL https://bootstrap.pypa.io/get-pip.py | python
ENV PATH /root/.pyenv/shims:/root/.pyenv/bin:$PATH
RUN eval "$(pyenv init -)"
RUN mkdir /root/.ssh/ && mkdir /root/.aws/
ADD .ssh /root/.ssh/
ADD .aws /root/.aws/
RUN chmod 600 /root/.ssh/id_rsa
COPY dict /root/dict
COPY ja-tokenizer /root/ja-tokenizer
ADD mecab-0.996.tar.gz /root/
ADD mecab-ipadic-2.7.0-20070801.tar.gz /root/
ADD init.sh /usr/local/
WORKDIR /root/ja-tokenizer
RUN pip install virtualenv
RUN virtualenv env && /bin/bash -c "source env/bin/activate" && pip install -r requirements/local.txt
