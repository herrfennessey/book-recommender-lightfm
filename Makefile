.PHONY: test
test:
	pytest

.PHONY: build-image
build-image:
	docker build --build-arg MODEL_VERSION=1705168040 -t lightapi --progress=plain .

.PHONY: run-gunicorn
run-gunicorn:
	gunicorn "src.main:create_app()" --bind 0.0.0.0:8080 --workers 1 --timeout 300 --log-config src/logging.conf


.PHONY: run-flask
run-flask:
	flask --app "src/main:create_app()" run --host=0.0.0.0 --port=8080 --debug


.PHONY: run-docker
run-docker:
	docker run -p 8080:8080 lightapi:latest
