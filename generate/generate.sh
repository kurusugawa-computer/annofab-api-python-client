#!/bin/bash -ue

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
fi

# openapi-generatorでpython scriptを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local openapitools/openapi-generator-cli generate \
    -i /local/swagger.yaml \
    -g python \
    -o /local/out \
    -t /local/template \
    -Dapis   -DapiTests=false -DapiDocs=false


# 連結
cat api_template.py out/openapi_client/api/*_api.py > ../annofabapi/api.py

# swagger.yamlの不備による暫定対応（2019/05/03版）
#sed -i -e 's/get_instruction_image_url_for_put(self, project_id, image_id, )/get_instruction_image_url_for_put(self, project_id, image_id, header_params)/g' ../annofabapi/api.py
# kwargsも修正する必要あり

rm out/openapi_client/api/*_api.py

popd

