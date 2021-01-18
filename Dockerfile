FROM python:3

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./download_ntlk.py /app/download_ntlk.py
RUN python download_ntlk.py
COPY . /app
ENTRYPOINT ["python", "app.py"]
