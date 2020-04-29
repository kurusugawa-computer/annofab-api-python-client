.PHONY: docs lint test format test publish_test publish

init:
	pip install pipenv --upgrade
    # blackをpipenvでなくpipでインストールする理由：
	# 2020/04時点でblackはベータ版で、pipenvでblackを利用するにはPipfileに`allow_prereleases=true`を記載する必要がある。
	# Pipfileに`allow_prereleases=true`を設定すると、black以外のプレリリース版（ベータ版）もインストールされてしまうが、これは避けたいのでblackはpipでインストールする
	pip install black --upgrade
	pipenv install --dev

format:
	pipenv run autoflake  --in-place --remove-all-unused-imports  --ignore-init-module-imports --recursive annofabapi tests
    # balckは正式版がリリースされるまでは、pipenv上で実行しない。事前にpipでblackをインストールすること。
	pipenv run isort --verbose --recursive annofabapi tests
	black annofabapi tests

lint:
	pipenv run mypy annofabapi --config-file setup.cfg
	pipenv run flake8 annofabapi
	pipenv run pylint annofabapi --rcfile setup.cfg

test:
	pipenv run pytest -n auto  --cov=annofabapi --cov-report=html tests

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

docs:
	cd docs && pipenv run make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

