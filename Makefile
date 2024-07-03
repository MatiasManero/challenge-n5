# Variables
DOCKERFILE_PATH=docker/Dockerfile
DOCKER_COMPOSE_PATH=docker/docker-compose.yml
IMAGE_NAME=matimane90/challenge-n5
IMAGE_TAG=v1
FULL_IMAGE_NAME=$(IMAGE_NAME):$(IMAGE_TAG)

# Comando para construir la imagen Docker
build:
	@echo "Building Docker image..."
	docker build -f $(DOCKERFILE_PATH) -t $(FULL_IMAGE_NAME) .

# Comando para ejecutar contenedores con Docker Compose
up:
	@echo "Starting services with Docker Compose..."
	docker-compose -f $(DOCKER_COMPOSE_PATH) up -d

# Comando para detener los contenedores con Docker Compose
down:
	@echo "Stopping services with Docker Compose..."
	docker-compose -f $(DOCKER_COMPOSE_PATH) down

# Comando para ejecutar pruebas con pytest
test:
	@echo "Running tests..."
	pytest

# Comando para construir la imagen Docker y luego ejecutar pruebas
all: build test

# Comando para construir la imagen Docker, levantar los contenedores y ejecutar pruebas
compose-test: build up test down

# Comando para limpiar imágenes Docker (opcional)
clean:
	@echo "Cleaning up Docker images..."
	docker rmi $(FULL_IMAGE_NAME) || true
