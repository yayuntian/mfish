#!/bin/bash

mvn clean && mvn package
docker build -t yhub-public.ssl.ysten.com:8880/inf-dev/net-fuck:dev .
docker push yhub-public.ssl.ysten.com:8880/inf-dev/net-fuck:dev