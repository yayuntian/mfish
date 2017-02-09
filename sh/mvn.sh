#!/bin/sh
mvn dependency:resolve -Dclassifier=javadoc
mvn dependency:sources
mvn clean compile
