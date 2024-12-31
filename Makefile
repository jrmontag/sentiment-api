.PHONY: all local-dev local-run test docker-build docker-run

# Default target
all: list

# hack to list all make targets
list:
	@echo "Available targets:"
	@grep '^[^#[:space:]].*:' Makefile

## local targets ##

# Run the FastAPI app in hot-reload dev mode
local-dev:
	uv run fastapi dev src/main.py 

# Run the FastAPI app in production mode
local-run: 
	uv run fastapi run src/main.py

# Run tests
test:
	cd test; \
	uv run pytest

## docker targets ##
CONTAINER_NAME=sentiment-api

# build image
docker-build:
	docker build -t ${CONTAINER_NAME} .

# run container 
docker-run: docker-build
	docker run -d -p 8000:8080 ${CONTAINER_NAME}

# build / push to hub
DOCKERHUB_USER=replaceme

docker-build-hub:
	docker build --platform linux/amd64,linux/arm64 -t ${DOCKERHUB_USER}/${CONTAINER_NAME} .

docker-push-hub: docker-build-hub
	docker push ${DOCKERHUB_USER}/${CONTAINER_NAME}
