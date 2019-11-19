FROM yhub.ssl.ysten.com/library/tomcat-custom:8-jdk8

MAINTAINER tianyayun@ysten.com

ENV LC_ALL en_US.UTF-8
ENV JAVA_OPTIONS="-Duser.timezone=Asia/Shanghai"

COPY target/demo-*.jar demo.jar
COPY run.sh run.sh
CMD sh /tomcat/run.sh