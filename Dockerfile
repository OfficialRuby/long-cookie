FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SUPERUSER_PASSWORD ruby
ENV DJANGO_SUPERUSER_USERNAME Ruby
RUN mkdir app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
COPY . /app/

