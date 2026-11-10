# Image 1: Lab 5 user management REST API (Postman and APIs) on port 5000
# Build: docker image build -t esg07/lab8-elias_ghanem:0.0.1-RELEASE .
# Run:   docker run -p 5000:5000 -d --name lab8-user-api esg07/lab8-elias_ghanem:0.0.1-RELEASE

# start by pulling the python image
FROM python:3.12-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# the Flask API listens on port 5000 inside the container
EXPOSE 5000

CMD ["python3", "app.py"]
