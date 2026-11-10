# Lab 8 - Docker Containers and Images

EECE 435L Software Tools Lab, Fall 2026-2027
Author: Elias Ghanem (AUB username: `esg07`)

This lab packages Flask apps as Docker images and runs them as containers:

1. **Tutorial:** a "hello world" Flask app in its own image.
2. **Activity 1:** the `docker ps -a`, `docker stop` and `docker logs` commands (see the report).
3. **Activity 2:** two images:
   - `esg07/lab8-elias_ghanem:0.0.1-RELEASE`: the Lab 5 user management API (Postman and APIs) on port **5000**
   - `esg07/lab8-elias_ghanem:0.0.2-RELEASE`: a `get_users` API (GET) on port **3000** that returns the names of all users in the database

## Project structure

```
lab8-elias-ghanem/
├── hello_flask/            Tutorial: hello world Flask app
│   ├── app.py
│   ├── requirements.txt    Generated with pip freeze
│   └── Dockerfile
├── image1_user_api/        Image 0.0.1-RELEASE: Lab 5 user API, port 5000
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── postman/            Lab 5 Postman collection and environment
├── image2_get_users/       Image 0.0.2-RELEASE: get_users API, port 3000
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── postman/            Postman request for GET /get_users
├── screenshots/            Command outputs
└── report/                 Word report with snapshots and explanations
```

## Image names and tags

The handout asks for `username/lab8-FirstName_LastName` with tags `0.0.1:RELEASE`
and `0.0.2:RELEASE`. Docker does not accept either form as written:

- Repository names must be lowercase, so `lab8-Elias_Ghanem` becomes `lab8-elias_ghanem`.
- A tag cannot contain `:` (the colon separates the repository from the tag), so
  `0.0.1:RELEASE` becomes `0.0.1-RELEASE`.

## Tutorial: hello world

```bash
cd hello_flask
pip freeze > requirements.txt        # in the venv where Flask is installed
docker image build -t flask_docker .
docker run -p 5000:5000 -d --name flask_docker flask_docker
```

Open http://localhost:5000.

## Activity 2, image 1: user API on port 5000 (tag 0.0.1-RELEASE)

```bash
cd image1_user_api
docker image build -t esg07/lab8-elias_ghanem:0.0.1-RELEASE .
docker run -p 5000:5000 -d --name lab8-user-api esg07/lab8-elias_ghanem:0.0.1-RELEASE
```

Endpoints (same as Lab 5):

| Method | URL | Description |
|--------|-----|-------------|
| GET    | `/api/users` | All users |
| GET    | `/api/users/<id>` | One user |
| POST   | `/api/users/add` | Add a user (JSON body) |
| PUT    | `/api/users/update` | Update a user (JSON body with `user_id`) |
| DELETE | `/api/users/delete/<id>` | Delete a user |

Import `image1_user_api/postman/` into Postman. The environment points at
`http://127.0.0.1:5000`, which is the container's published port.

## Activity 2, image 2: get_users on port 3000 (tag 0.0.2-RELEASE)

```bash
cd image2_get_users
docker image build -t esg07/lab8-elias_ghanem:0.0.2-RELEASE .
docker run -p 3000:3000 -d --name lab8-get-users esg07/lab8-elias_ghanem:0.0.2-RELEASE
curl http://localhost:3000/get_users
```

`GET /get_users` (also available as `/api/get_users`) returns:

```json
["John Doe", "Jane Smith", "Mary James"]
```

On first start, the app creates the SQLite `users` table and inserts the default users.

## Changes from the handout

- **Base image:** `python:3.12-alpine` instead of `python:3.8-alpine`. Python 3.8
  is end-of-life, and Flask 3.1 requires Python 3.9 or newer.
- **`host="0.0.0.0"`:** each app calls `app.run(host="0.0.0.0", ...)`. Flask's default,
  `127.0.0.1`, only accepts connections from inside the container, so
  `-p 5000:5000` would forward to a port nothing is listening on.
- **`.dockerignore`:** keeps `venv/`, `__pycache__/` and any local `database.db`
  out of the image, so `COPY . /app` copies only the source.

## Useful commands

```bash
docker ps -a                    # list all containers, running and stopped
docker images                   # list images
docker logs lab8-user-api       # print a container's output
docker stop lab8-user-api       # stop a running container
docker start lab8-user-api      # start it again
docker rm lab8-user-api         # remove a stopped container
```
