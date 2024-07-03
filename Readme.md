# Informe del Proyecto

## Comandos de `Makefile`

Este proyecto utiliza un `Makefile` para facilitar la construcción del contenedor Docker, ejecutar pruebas y manejar la infraestructura con Docker Compose. Aquí están los comandos definidos en el `Makefile`:

```makefile
# Define la imagen de Docker y el puerto de la aplicación
DOCKER_IMAGE := matimane90/challenge-n5
DOCKER_COMPOSE_FILE := docker-compose.yml

# Construir la imagen de Docker
build:
	docker build -f docker/Dockerfile -t $(DOCKER_IMAGE) .

# Ejecutar pruebas con pytest
test:
	pytest

# Levantar la infraestructura con Docker Compose
up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

# Detener y eliminar la infraestructura con Docker Compose
down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down
```
## Conexión con PostgreSQL

El proyecto utiliza PostgreSQL como sistema de gestión de bases de datos. La configuración de la conexión se realiza a través de variables de entorno que se cargan desde un archivo .env o variables del sistema.

## Componentes Infraestructura AWS
### Proxy (API Gateway):
El API Gateway actúa como un proxy que expone las APIs del servicio. Se encarga de recibir las solicitudes HTTP y dirigirlas a la función Lambda.

### AWS Lambda:
Haciendo uso de la libreria mangum(https://pypi.org/project/mangum/?ref=deadbear.io) nos permite encapsular la API con un controlador que empaquetaremos e implementaremos como una función Lambda en AWS 

### PostgreSQL:
La base de datos PostgreSQL se encuentra en una instancia de Amazon RDS

### AWS Secrets Manager
AWS Secrets Manager se configura para almacenar las claves secretas y proporcionar acceso seguro a ellas desde la función Lambda y otros servicios que las requieran.