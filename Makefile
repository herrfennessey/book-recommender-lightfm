.PHONY: install
install:
	poetry install --no-interaction

.PHONY: test
test:
	poetry run pytest

.PHONY: build
build:
	poetry build

.PHONY: build-image
build-image:
	docker build -t lightfm --progress=plain .

.PHONY: run-gunicorn
run-gunicorn:
	poetry run gunicorn lightfm.main:app --bind 0.0.0.0:8080 --workers 1


.PHONY: run-flask
run-flask:
	poetry run flask --app lightfm/main:app run --host=0.0.0.0 --port=8080 --debug


.PHONY: run-docker
run-docker:
	docker run -p 8080:8080 lightfm:latest