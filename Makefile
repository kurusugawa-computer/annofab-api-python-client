.PHONY: docs lint test format test publish_test publish

init:
	pip install pipenv --upgrade
	pipenv install --dev

format:
	pipenv run isort --verbose --recursive annofabapi tests examples setup.py
	pipenv run yapf --verbose --in-place --recursive annofabapi tests examples setup.py

lint:
	pipenv run flake8 annofabapi tests
	pipenv run mypy annofabapi tests
	pipenv run pylint annofabapi tests --rcfile tox.cfg

test:
	pipenv run pytest tests -v --cov=annofabapi --cov-report=html

publish_test:
	pipenv run python setup.py check --strict
	pipenv run python setup.py bdist_wheel
	pipenv run twine upload dist/* --repository-url https://test.pypi.org/legacy/ --verbose
	rm -fr build/ dist/ annofabapi.egg-info

publish:
	pipenv run python setup.py check --strict
	pipenv run python setup.py bdist_wheel
	pipenv run twine upload dist/* --repository-url https://upload.pypi.org/legacy/ --verbose
	rm -fr build/ dist/ annofabapi.egg-info

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"
