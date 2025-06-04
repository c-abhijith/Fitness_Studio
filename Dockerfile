FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /fitness_studio

COPY requirements.txt /fitness_studio/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /fitness_studio/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
