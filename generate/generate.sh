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

  # インデントを１つ深くする
  sed -e "s/#\/schemas/#\/components\/schemas/g" -e "s/^/  /g" swagger-api-components.yaml --in-place

  sed '/swagger-api-components.yaml/d' swagger.yaml > swagger-tmp.yaml
  cat swagger-tmp.yaml  swagger-api-components.yaml > swagger.yaml

  sed '/swagger-api-components.yaml/d' swagger.v2.yaml > swagger-tmp.v2.yaml
  cat swagger-tmp.v2.yaml swagger-api-components.yaml > swagger.v2.yaml

  rm swagger-tmp.yaml swagger-tmp.v2.yaml
fi

JAVA_OPTS="-Dlog.level=info"

OPENAPI_GENERATOR_CLI_COMMON_OPTION="--generator-name python \
    --output /local/out \
    --type-mappings array=List,DateTime=str,date=str"

# v1 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local  -e JAVA_OPTS=${JAVA_OPTS} openapitools/openapi-generator-cli generate \
    --input-spec swagger.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template \
    -Dapis -DapiTests=false -DapiDocs=false \
    -Dmodels -DmodelTests=false -DmodelDocs=false \
    --ignore-file-override=/local/.openapi-generator-ignore_v1

cat generated_api_partial_header_v1.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api.py

cat models_partial_header_v1.py out/openapi_client/models/*.py > ../annofabapi/models.py

rm -Rf out/openapi_client

# v2 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local -e JAVA_OPTS=${JAVA_OPTS} openapitools/openapi-generator-cli generate \
    --input-spec swagger.v2.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template \
    -Dapis -DapiTests=false -DapiDocs=false \
    --ignore-file-override=/local/.openapi-generator-ignore_v2

cat generated_api_partial_header_v2.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api2.py

rm -Rf out/openapi_client

# v1 apiのmodelからDataClass用のpythonファイルを生成する。
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local  -e JAVA_OPTS=${JAVA_OPTS} \
    openapitools/openapi-generator-cli generate \
    --input-spec swagger.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template_dataclass \
    -Dmodels -DmodelTests=false -DmodelDocs=false \

MODELS_DIR=out/openapi_client/models

# Annotation Specs
declare -a model_files=(${MODELS_DIR}/keybind.py \
 ${MODELS_DIR}/label_bounding_box_metadata.py \
 ${MODELS_DIR}/label_segmentation_metadata.py \
 ${MODELS_DIR}/internationalization_message_messages.py \
 ${MODELS_DIR}/internationalization_message.py \
 ${MODELS_DIR}/inspection_phrase.py \
 ${MODELS_DIR}/annotation_specs_history.py \
 ${MODELS_DIR}/color.py \
 ${MODELS_DIR}/additional_data_definition_choices.py \
 ${MODELS_DIR}/additional_data_definition.py \
 ${MODELS_DIR}/annotation_editor_feature.py \
 ${MODELS_DIR}/label.py \
 ${MODELS_DIR}/annotation_specs.py)
cat partial-header/dataclass/common.py partial-header/dataclass/annotation_specs.py  \
 ${model_files[@]} > ../annofabapi/dataclass/annotation_specs.py

# Input
declare -a model_files=(${MODELS_DIR}/resolution.py ${MODELS_DIR}/input_data.py)
cat partial-header/dataclass/common.py partial-header/dataclass/input.py  \
 ${model_files[@]} > ../annofabapi/dataclass/input.py

declare -a model_files=(${MODELS_DIR}/inspection.py)
cat partial-header/dataclass/common.py partial-header/dataclass/inspection.py  \
 ${model_files[@]} > ../annofabapi/dataclass/inspection.py

# Organization
declare -a model_files=(${MODELS_DIR}/organization_activity.py ${MODELS_DIR}/organization_summary.py ${MODELS_DIR}/organization.py)
cat partial-header/dataclass/common.py partial-header/dataclass/organization.py  \
 ${model_files[@]} > ../annofabapi/dataclass/organization.py

# Organization Member
declare -a model_files=(${MODELS_DIR}/organization_member.py)
cat partial-header/dataclass/common.py partial-header/dataclass/organization_member.py  \
 ${model_files[@]} > ../annofabapi/dataclass/organization_member.py

# Project
declare -a model_files=(${MODELS_DIR}/project_summary.py ${MODELS_DIR}/project_configuration.py ${MODELS_DIR}/project.py)
cat partial-header/dataclass/common.py partial-header/dataclass/project.py  \
 ${model_files[@]} > ../annofabapi/dataclass/project.py
# swagger.yamlの間違いに対する暫定対応
sed -e "s/status: ProjectStatus/project_status: ProjectStatus/" ../annofabapi/dataclass/project.py --in-place

# Project Member
declare -a model_files=(${MODELS_DIR}/project_member.py)
cat partial-header/dataclass/common.py partial-header/dataclass/project_member.py  \
 ${model_files[@]} > ../annofabapi/dataclass/project_member.py

# Supplementary
declare -a model_files=(${MODELS_DIR}/supplementary_data.py)
cat partial-header/dataclass/common.py partial-header/dataclass/supplementary.py  \
 ${model_files[@]} > ../annofabapi/dataclass/supplementary.py

# Task
declare -a model_files=(${MODELS_DIR}/task_history.py ${MODELS_DIR}/task_history_short.py ${MODELS_DIR}/task.py)
cat partial-header/dataclass/common.py partial-header/dataclass/task.py  \
 ${model_files[@]} > ../annofabapi/dataclass/task.py
# swagger.yamlの間違いに対する暫定対応
sed -e "s/work_timespan/work_time_span/" ../annofabapi/dataclass/task.py --in-place


rm -Rf out/openapi_client


cd ../

# Format
FORMATTED_FILE="annofabapi/generated_api.py annofabapi/generated_api2.py annofabapi/models.py annofabapi/dataclass/*.py"
pipenv run isort --verbose ${FORMATTED_FILE}
pipenv run yapf --verbose --in-place ${FORMATTED_FILE}

popd
