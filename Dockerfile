FROM python:3

WORKDIR /usr/local
COPY ./ MathQA
WORKDIR ./MathQA
RUN python3 -m venv --system-site-packages env/ && . env/bin/activate
RUN pip3 install -r requirements.txt
RUN wget http://nlp.stanford.edu/software/stanford-postagger-full-2015-12-09.zip
RUN wget http://nlp.stanford.edu/software/stanford-english-corenlp-2016-01-10-models.jar
RUN unzip stanford-postagger-full-2015-12-09.zip
RUN git clone https://github.com/stanfordnlp/CoreNLP.git
WORKDIR /CoreNLP
RUN java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 & SERVER_PID=$!
WORKDIR ./MathQA
RUN python3 app.py
EXPOSE 8000
CMD ["python3", "app.py", "0.0.0.0:8000"]