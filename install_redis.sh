#!/bin/bash
# This script downloads redis-server
# if redis has not already been downloaded
if [ ! -d redis-5.0.4/src ]; then
    wget http://download.redis.io/releases/redis-5.0.4.tar.gz
    tar xzf redis-5.0.4.tar.gz
    rm redis-5.0.4.tar.gz
    cd redis-5.0.4
    make
else
    cd redis-5.0.4
fi