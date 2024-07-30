# FastAPI Mock Server
- Based on FastAPI production template: https://github.com/teamhide/fastapi-boilerplate.git
- FastAPI + Poetry setup Dockerized
- Run with single docker-compose command

# Features
- Async SQLAlchemy session
- Custom user class
- Dependencies for specific permissions
- Celery
- Dockerize(Hot reload)
- Event dispatcher
- Cache

# Run with Docker Compose

## Install Docker and Docker Compose
```shell
sudo apt-get update
sudo apt-get install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose version
```

## Run 
```shell
docker-compose up
```
