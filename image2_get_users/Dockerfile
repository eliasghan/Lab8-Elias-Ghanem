# Image 2: get_users API (GET) that returns the names of all users, on port 3000
# Build: docker image build -t esg07/lab8-elias_ghanem:0.0.2-RELEASE .
# Run:   docker run -p 3000:3000 -d --name lab8-get-users esg07/lab8-elias_ghanem:0.0.2-RELEASE

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

# the Flask API listens on port 3000 inside the container
EXPOSE 3000

CMD ["python3", "app.py"]
