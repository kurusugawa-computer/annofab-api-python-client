GITLEAKS_VERSION := v8.30.1
GITLEAKS_DOCKER_CONFIG ?= /tmp/annofab-api-python-client-gitleaks-docker-config

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


.PHONY: gitleaks

gitleaks:
	@if command -v gitleaks >/dev/null 2>&1; then \
		gitleaks git --redact=100 --verbose --log-opts=HEAD .; \
	elif command -v docker >/dev/null 2>&1; then \
		mkdir -p "${GITLEAKS_DOCKER_CONFIG}"; \
		DOCKER_CONFIG="${GITLEAKS_DOCKER_CONFIG}" docker run --rm \
			-v "$$(pwd):$$(pwd):ro" \
			-v "$$(git rev-parse --path-format=absolute --git-common-dir):$$(git rev-parse --path-format=absolute --git-common-dir):ro" \
			-w "$$(pwd)" ghcr.io/gitleaks/gitleaks:${GITLEAKS_VERSION} git --redact=100 --verbose --log-opts=HEAD .; \
	else \
		echo "gitleaksまたはdockerをインストールしてください。" >&2; \
		exit 127; \
	fi
