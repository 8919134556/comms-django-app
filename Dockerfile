FROM python:3.9.10
WORKDIR /djnago/comms
COPY . /djnago/comms/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]