.PHONY: install
install:
	poetry install --no-interaction

.PHONY: test
test:
	pytest

.PHONY: build
build:
	poetry build

.PHONY: build-image
build-image:
	docker build -t lightapi --progress=plain .

.PHONY: run-gunicorn
run-gunicorn:
	gunicorn src.lightapi.main:app --bind 0.0.0.0:8080 --workers 1


.PHONY: run-flask
run-flask:
	flask --app src/lightapi/main:app run --host=0.0.0.0 --port=8080 --debug


.PHONY: run-docker
run-docker:
	docker run -p 8080:8080 lightapi:latest
