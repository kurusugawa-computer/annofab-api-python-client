ifndef SOURCE_FILES
	export SOURCE_FILES:=annofabapi
endif
ifndef TEST_FILES
	export TEST_FILES:=tests
endif

.PHONY: docs lint test format test publish

format:
	poetry run ruff format ${SOURCE_FILES} ${TEST_FILES}
	poetry run ruff check ${SOURCE_FILES} ${TEST_FILES} --fix-only --exit-zero

lint:
	poetry run ruff check ${SOURCE_FILES}
	# テストコードはチェックを緩和する
	# pygrep-hooks, flake8-datetimez, line-too-long, flake8-annotations, unused-noqa
	poetry run ruff check ${TEST_FILES} --ignore PGH,DTZ,E501,ANN,RUF100
	poetry run mypy ${SOURCE_FILES} ${TEST_FILES}
	# テストコードはチェックを緩和するためpylintは実行しない
	poetry run pylint --jobs=0 ${SOURCE_FILES}


test:
	# 並列で実行するとエラーになるので、シーケンシャルで実行する
	poetry run pytest --cov=${SOURCE_FILES} --cov-report=html ${TEST_FILES}

publish:
	poetry publish --build

docs:
	cd docs && poetry run make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

