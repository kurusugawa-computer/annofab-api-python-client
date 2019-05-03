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

# swagger.yamlの不備による暫定対応（2019/05/03版）
#sed -i -e 's/get_instruction_image_url_for_put(self, project_id, image_id, )/get_instruction_image_url_for_put(self, project_id, image_id, header_params)/g' ../annofabapi/api.py
# kwargsも修正する必要あり

rm out/openapi_client/api/*_api.py

popd

