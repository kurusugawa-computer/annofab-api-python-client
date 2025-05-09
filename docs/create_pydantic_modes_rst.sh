#!/bin/bash -uex

# pydantic_modelsの全モジュールが記載されたrstファイルを生成します。

# プロジェクトのルートディレクトリに移動
SCRIPT_DIR=$(cd $(dirname $0); pwd)
pushd ${SCRIPT_DIR}/../

tempdir=$(mktemp -d)

uv run sphinx-apidoc annofabapi -o docs/api_reference/foo --output-dir ${tempdir}
cp ${tempdir}/annofabapi.pydantic_models.rst docs/api_reference/pydantic_models.rst

rm -rf ${tempdir}

popd
