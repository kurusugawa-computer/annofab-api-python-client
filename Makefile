.PHONY: docs lint test format test publish

init:
	pip install poetry --upgrade
	poetry install

format:
	poetry run autoflake  --in-place --remove-all-unused-imports  --ignore-init-module-imports --recursive annofabapi tests
	poetry run isort --verbose  annofabapi tests
	poetry run black annofabapi tests

lint:
	poetry run mypy annofabapi tests
	poetry run flake8 annofabapi tests/create_test_project.py
	poetry run pylint --jobs=0 annofabapi tests/create_test_project.py

test:
	poetry run pytest -n auto  --cov=annofabapi --cov-report=html tests

publish:
	poetry publish --build

docs:
	cd docs && poetry run make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

