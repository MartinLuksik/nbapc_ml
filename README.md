# Machine Learning REST server
This repository contains Machine Learning model development and a containerized micro-service - Python REST server which makes the model predictions accessible for other applications. 

# Docker build

The microservice will serve the model passed during the build time.
```bash
docker build -t <repo:tag> --build-arg model=<model_name>.pkl .
```

# Run application
```bash
docker run -d --name mlserver -p 8000:8000 <repo:tag>
```
