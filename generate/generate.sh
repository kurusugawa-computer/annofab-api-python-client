#!/bin/bash -uex

usage_exit() {
        echo "Usage: $0 [--ownload]" 1>&2
        exit 1
}

FLAG_DOWNLOAD=false

if [ $# -gt 0 ]; then
    case ${1} in
        --download)
            echo "flag"
            FLAG_DOWNLOAD=true
        ;;

        --help|-h)
            usage_exit
        ;;

        *)
            usage_exit
        ;;
    esac
fi

# このスクリプトの存在するディレクトリに移動する
SCRIPT_DIR=$(cd $(dirname $0); pwd)
pushd ${SCRIPT_DIR}

# swagger.yamlを修正したいときがあるので、
if "${FLAG_DOWNLOAD}"; then
    curl https://annofab.com/docs/api/swagger.yaml --output swagger.yaml
    curl https://annofab.com/docs/api/swagger.v2.yaml --output swagger.v2.yaml
    curl https://annofab.com/docs/api/swagger-api-components.yaml  --output swagger-api-components.yaml
fi

OPENAPI_GENERATOR_CLI_COMMON_OPTION="--generator-name python \
    --output /local/out \
    --template-dir /local/template \
    --type-mappings array=List \
    -Dapis   -DapiTests=false -DapiDocs=false \
    -Dmodels   -DmodelTests=false -DmodelDocs=false"

# v1 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local openapitools/openapi-generator-cli generate \
    --input-spec swagger.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --ignore-file-override=/local/.openapi-generator-ignore_v1

cat generated_api_partial_header_v1.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api.py

cat models_partial_header_v1.py out/openapi_client/models/*.py > ../annofabapi/models.py

rm -Rf out/openapi_client

# v2 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local openapitools/openapi-generator-cli generate \
    --input-spec swagger.v2.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --ignore-file-override=/local/.openapi-generator-ignore_v2

cat generated_api_partial_header_v2.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api2.py

rm -Rf out/openapi_client

cd ../

# Format
FORMATTED_FILE="annofabapi/generated_api.py annofabapi/generated_api2.py annofabapi/models.py"
pipenv run isort --verbose ${FORMATTED_FILE}
pipenv run yapf --verbose --in-place ${FORMATTED_FILE}

popd
