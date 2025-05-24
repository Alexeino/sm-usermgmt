.PHONY: run migrations migrate format compose-up

run/devserver:
	poetry run uvicorn main:server --reload

migrations:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head

format:
	poetry run ruff check . --fix

compose-up:
	docker compose up