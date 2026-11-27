format:
	@echo "Starting autoflake format"
	uv run autoflake --recursive api apps config
	@echo "Starting isort format..."
	uv run isort api apps config --skip __init__.py
	@echo "Starting black format..."
	uv run black api apps config
	@echo "Starting pylint "
	uv run pylint api apps config

test:
	@echo "Starting tests..."
	uv run python manage.py test


test-unit:
	@echo "Starting unit tests..."
	uv run python manage.py test tests.unit

test-integration:
	@echo "Starting integration tests (docker compose stack required for redis)..."
	docker compose exec backend python manage.py test tests.integration api

test-e2e:
	@echo "Starting end to end tests against the running stack..."
	docker compose exec -e E2E_BASE_URL=http://localhost:8000 backend python -m unittest tests.e2e.test_stack -v
