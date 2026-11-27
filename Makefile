format:
	@echo "Starting autoflake format"
	uv run autoflake --recursive api apps configuracion
	@echo "Starting isort format..."
	uv run isort api apps configuracion --skip __init__.py
	@echo "Starting black format..."
	uv run black api apps configuracion
	@echo "Starting pylint "
	uv run pylint api apps configuracion

test:
	@echo "Starting tests..."
	uv run python manage.py test

