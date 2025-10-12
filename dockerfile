#use lightweight python image
FROM python:slim

#set enivornment variables to precent python from writing pyc files to disc and to buffer stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1\
    PYTHONUNBUFFERED=1

# set work directory
WORKDIR /app

#install dependencies by lightbgm
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#copy the  application code to the container
COPY . .

#install the package in editable mode
RUN pip install --no-cache-dir -e .

#Train the model before runnning the app
RUN python pipeline/training_pipeline.py

#expose the port the app runs on
EXPOSE 5000

#command to run the app
CMD ["python", "application.py"]

