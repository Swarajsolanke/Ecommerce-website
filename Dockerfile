FROM python:3.11-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=1
#set working directory
WORKDIR /app

# copy requirements file
COPY requirements.txt .
# install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
#copy project files
COPY . .
#expose the port
EXPOSE 8000
#set the entrypoint
ENTRYPOINT ["python", "manage.py", "runserver","0.0.0:8000"]
