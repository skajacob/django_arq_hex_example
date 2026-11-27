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

