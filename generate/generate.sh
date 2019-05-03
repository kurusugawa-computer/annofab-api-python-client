#!/bin/bash -uvx

# このスクリプトの存在するディレクトリに移動する
SCRIPT_DIR=$(cd $(dirname $0); pwd)
pushd ${SCRIPT_DIR}

# openapi-generatorでpython scriptを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local openapitools/openapi-generator-cli generate \
    -i https://annofab.com/docs/api/swagger.yaml \
    -g python \
    -o /local/out \
    -t /local/template \
    -Dapis   -DapiTests=false -DapiDocs=false


# 連結
cat api_template.py out/openapi_client/api/*_api.py > ../annofabapi/api.py

rm out/openapi_client/api/*_api.py

popd

