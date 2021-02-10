FROM centos
MAINTAINER Masa <dev.roomsso.net@gmail.com>
USER root
ENV LC_ALL C
ENV LANG ja_JP.UTF-8
ENV PYTHONIOENCODING utf-8
RUN yum install -y bzip2 git && git clone https://github.com/yyuu/pyenv.git ~/.pyenv
ENV PATH /root/.pyenv/shims:/root/.pyenv/bin:$PATH
RUN eval "$(pyenv init -)" && pyenv install miniconda3-4.3.30 && pyenv global miniconda3-4.3.30 && pyenv rehash
RUN mkdir /root/.ssh/ && mkdir /root/.aws/
ADD .ssh /root/.ssh/
ADD .aws /root/.aws/
RUN chmod 600 /root/.ssh/id_rsa
ADD init.sh /usr/local/
RUN pip install --upgrade pip && \
    pip install awscli boto3 tzlocal attrdict requests logutils emoji jsm bs4 lxml requests_oauthlib \
    pandas xlrd more-itertools dill zenhan
ADD reduction.py /root/.pyenv/versions/miniconda3-4.3.30/lib/python3.6/multiprocessing

