#!/bin/bash -uex

usage_exit() {
        echo "Usage: $0 [--notdownload]" 1>&2
        exit 1
}

FLAG_DOWNLOAD=true

if [ $# -gt 0 ]; then
    case ${1} in
        --notdownload)
            echo "flag"
            FLAG_DOWNLOAD=false
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

fi

OPENAPI_GENERATOR_CLI_COMMON_OPTION="-g python \
    -o /local/out \
    -t /local/template \
    -Dapis   -DapiTests=false -DapiDocs=false"

# v1 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local openapitools/openapi-generator-cli generate \
    -i /local/swagger.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --ignore-file-override=/local/.openapi-generator-ignore_v1

cat generated_api_template_v1.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api.py

rm out/openapi_client/api/*_api.py


# v2 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local openapitools/openapi-generator-cli generate \
    -i /local/swagger.v2.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --ignore-file-override=/local/.openapi-generator-ignore_v2

cat generated_api_template_v2.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api2.py

rm out/openapi_client/api/*_api.py

cd ../

# Format
pipenv run isort --verbose annofabapi/generated_api.py
pipenv run yapf --verbose --in-place annofabapi/generated_api.py


popd

