FROM python:3

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python3 -m venv --system-site-packages env/ && . env/bin/activate
RUN pip3 install -r requirements.txt
COPY . /app
CMD ["python3", "app.py", "0.0.0.0:5000"]
