#!/bin/bash

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
if [ ! -d $JAVA_HOME ]
then
    export JAVA_HOME=/usr/lib/jvm/java-8-oracle
fi
export PATH=$JAVA_HOME/bin:$PATH

if [ ! -f stanford-postagger-full-2015-12-09.zip ]
then
    echo "Downloading POS Tagger…"
    wget http://nlp.stanford.edu/software/stanford-postagger-full-2015-12-09.zip
fi
echo "Installing POS Tagger"
unzip stanford-postagger-full-2015-12-09.zip

if [ ! -d CoreNLP ]
then
    echo "Cloning and installing CoreNLP…"
    git clone https://github.com/stanfordnlp/CoreNLP.git
    cd CoreNLP
    ant compile
    ant jar
    cd ..
fi
if ! ls stanford-english-corenlp-*models.jar 1> /dev/null 2>&1
then
    echo "Downloading English model for CoreNLP…"
    wget http://nlp.stanford.edu/software/stanford-english-corenlp-2016-01-10-models.jar
fi
yes | cp -l stanford-english-corenlp-*models.jar CoreNLP
echo "All seemed to work. Hold tight while we test it on a simple example (might take some time)."
cd CoreNLP
export CLASSPATH="`find . -name '*.jar'`"
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer &
sleep 1 # Let the server some time to start...
echo "CoreNLP server launched in background: PID $! "
