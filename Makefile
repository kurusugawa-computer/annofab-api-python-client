.PHONY: docs lint test format

init:
	pip install pipenv --upgrade
	pipenv install --dev

format:
	pipenv run isort --verbose --recursive annofabapi tests
	pipenv run yapf --verbose --in-place --recursive annofabapi tests

lint:
	pipenv run flake8 sample_project tests
	pipenv run mypy sample_project tests
	pipenv run pylint sample_project tests --rcfile setup.cfg

test:
	pipenv run python -m unittest discover tests
