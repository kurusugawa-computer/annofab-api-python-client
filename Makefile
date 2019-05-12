.PHONY: docs lint test format

init:
	pip install pipenv --upgrade
	pipenv install --dev

format:
	pipenv run isort --verbose --recursive annofabapi tests
	pipenv run yapf --verbose --in-place --recursive annofabapi tests

lint:
	pipenv run flake8 annofabapi tests
	pipenv run mypy annofabapi tests
	pipenv run pylint sample_project tests --rcfile setup.cfg

test:
	pipenv run pytest tests -v --cov=annofabapi --cov-report=html
