ifndef SOURCE_FILES
	export SOURCE_FILES:=annofabapi
endif
ifndef TEST_FILES
	export TEST_FILES:=tests
endif

.PHONY: docs lint test format test

format:
	uv run ruff format ${SOURCE_FILES} ${TEST_FILES}
	uv run ruff check ${SOURCE_FILES} ${TEST_FILES} --fix-only --exit-zero

lint:
	uv run ruff format ${SOURCE_FILES} ${TEST_FILES} --check
	uv run ruff check ${SOURCE_FILES} ${TEST_FILES} 
	uv run mypy ${SOURCE_FILES} ${TEST_FILES}


test:
	# 並列で実行するとエラーになるので、シーケンシャルで実行する
	uv run pytest --cov=${SOURCE_FILES} --cov-report=html ${TEST_FILES}

docs:
	cd docs && uv run make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

