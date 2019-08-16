.PHONY: docs lint test format test publish_test publish

init:
	pip install pipenv --upgrade
	pipenv install --dev

test:
	pipenv run pytest tests -v --cov=annofabapi --cov-report=html

publish_test:
	rm -fr build/ dist/ annofabapi.egg-info
	pipenv run python setup.py check --strict
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --repository-url https://test.pypi.org/legacy/ --verbose
	rm -fr build/ dist/ annofabapi.egg-info

publish:
	rm -fr build/ dist/ annofabapi.egg-info
	pipenv run python setup.py check --strict
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --repository-url https://upload.pypi.org/legacy/ --verbose
	rm -fr build/ dist/ annofabapi.egg-info

