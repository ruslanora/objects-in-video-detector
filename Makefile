venv:
	python3 -m venv venv

lint:
	python3 -m pylint .

test:
	python3 -m pytest .

format:
	python3 -m black .

formatcheck:
	python3 -m black . --check --diff --color

typecheck:
	python3 -m mypy --config-file mypy.ini . --explicit-package-bases

hooks:
	pre-commit install --hook-type pre-commit; \
	pre-commit install --hook-type pre-push

build:
	docker build -t object-detector .

dev:
	python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

run:
	docker run -p 8000:8000 object-detector

serve:
	make build; \
	make run