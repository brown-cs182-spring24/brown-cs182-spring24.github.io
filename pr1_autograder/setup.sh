#!/usr/bin/env bash

apt-get install -y graphviz libgraphviz-dev

apt-get install -y python python-pip
apt-get install -y python3 python3-pip

pip install -r /autograder/source/requirements.txt
pip3 install -r /autograder/source/requirements.txt

apt-get -y install openjdk-11-jdk

apt-get install -y libxml2-dev libcurl4-openssl-dev libssl-dev
apt-get install -y r-base

wget https://julialang-s3.julialang.org/bin/linux/x64/1.5/julia-1.5.1-linux-x86_64.tar.gz
tar xvf julia-1.5.1-linux-x86_64.tar.gz
export PATH=$PATH:/julia-1.5.1/bin