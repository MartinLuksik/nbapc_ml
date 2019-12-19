# Machine Learning REST server
This repository contains Machine Learning model development and a containerized micro-service - Python REST server which makes the model predictions accessible for other applications. 

[![Build Status](https://dev.azure.com/martinluksik/nbapc/_apis/build/status/Build%20ML%20Server?branchName=master)](https://dev.azure.com/martinluksik/nbapc/_build/latest?definitionId=5&branchName=master)

# Docker build

The microservice will serve the model passed during the build time.
```bash
docker build -t <repo:tag> --build-arg model=<model_name>.pkl .
```

# Run application
```bash
docker run -d --name mlserver -p 8000:8000 <repo:tag>
```
