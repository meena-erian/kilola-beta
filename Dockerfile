FROM python:3
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
CMD python /kilola/manage.py makemigrations && python /kilola/manage.py migrate && python /kilola/manage.py runserver 0.0.0.0:84