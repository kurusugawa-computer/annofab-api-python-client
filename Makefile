.PHONY: docs lint test format test publish_test publish

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

publish_test:
	python setup.py bdist_wheel
	pipenv run twine upload dist/* --repository-url https://test.pypi.org/legacy/ --verbose
	rm -fr build/ dist/ annofabapi.egg

publish:
	python setup.py bdist_wheel
	pipenv run twine upload dist/* --repository-url https://upload.pypi.org/legacy/ --verbose
	rm -fr build/ dist/ annofabapi.egg

