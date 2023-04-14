.PHONY: docs lint test format test publish

format:
	poetry run autoflake  --in-place --remove-all-unused-imports  --ignore-init-module-imports --recursive annofabapi tests
	poetry run isort annofabapi tests
	poetry run black annofabapi tests

lint:
	poetry run mypy annofabapi tests
	poetry run flake8 annofabapi tests
	poetry run pylint --jobs=0 annofabapi

test:
	# 並列で実行するとエラーになるので、シーケンシャルで実行する
	poetry run pytest --cov=annofabapi --cov-report=html tests

publish:
	poetry publish --build

docs:
	cd docs && poetry run make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

