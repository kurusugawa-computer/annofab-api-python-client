#!/bin/bash -uex

PROGNAME=$(basename $0)

usage_exit() {
        echo "Usage: ${PROGNAME} [--download] [--docker-pull]" 1>&2
        exit 1
}

FLAG_DOWNLOAD=false
FLAG_DOCKER_PULL=false

if [ $# -gt 0 ]; then
    for OPT in "$@"
    do
    case ${OPT} in
        "--download")
            FLAG_DOWNLOAD=true
            shift 1
        ;;
        "--docker-pull")
            FLAG_DOCKER_PULL=true
            shift 1
        ;;
        "-h" | "--help")
            usage_exit
        ;;
        -*)
            echo "${PROGNAME}: illegal option $1" 1>&2
            exit 1
        ;;
        *)
            if [ -n "$1" ] && [[ ! "$1" =~ ^-+ ]]; then
                echo "${PROGNAME}: illegal parameter $1" 1>&2
                exit 1
            fi
        ;;
    esac
    done
fi

# このスクリプトの存在するディレクトリに移動する
SCRIPT_DIR=$(cd $(dirname $0); pwd)
pushd ${SCRIPT_DIR}

if "${FLAG_DOCKER_PULL}"; then
    docker pull openapitools/openapi-generator-cli
fi

# swagger.yamlを修正したいときがあるので、
if "${FLAG_DOWNLOAD}"; then
    curl https://annofab.com/docs/api/swagger.yaml --output swagger/swagger.yaml
    curl https://annofab.com/docs/api/swagger.v2.yaml --output swagger/swagger.v2.yaml
    curl https://annofab.com/docs/api/swagger-api-components.yaml  --output swagger/swagger-api-components.yaml
#    curl https://annofab.com/docs/api/swagger.internal.yaml  --output swagger.internal.yaml

  # インデントを１つ深くする
  sed -e "s/#\/schemas/#\/components\/schemas/g" -e "s/^/  /g" swagger/swagger-api-components.yaml --in-place

  sed '/swagger-api-components.yaml/d' swagger/swagger.yaml > swagger/swagger-tmp.yaml
  cat swagger/swagger-tmp.yaml  swagger/swagger-api-components.yaml > swagger/swagger.yaml

  sed '/swagger-api-components.yaml/d' swagger/swagger.v2.yaml > swagger/swagger-tmp.v2.yaml
  cat swagger/swagger-tmp.v2.yaml swagger/swagger-api-components.yaml > swagger/swagger.v2.yaml

  rm swagger/swagger-tmp.yaml swagger/swagger-tmp.v2.yaml
fi

JAVA_OPTS="-Dlog.level=info"

OPENAPI_GENERATOR_CLI_COMMON_OPTION="--generator-name python \
    --output /local/out \
    --type-mappings array=List,DateTime=str,date=str,object=__DictStrKeyAnyValue__"

# v1 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local  -e JAVA_OPTS=${JAVA_OPTS} openapitools/openapi-generator-cli generate \
    --input-spec swagger/swagger.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template \
    -Dapis -DapiTests=false -DapiDocs=false \
    -Dmodels -DmodelTests=false -DmodelDocs=false \
    --ignore-file-override=/local/.openapi-generator-ignore_v1

cat partial-header/generated_api_partial_header_v1.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api.py

cat partial-header/models_partial_header_v1.py out/openapi_client/models/*.py > ../annofabapi/models.py

rm -Rf out/openapi_client

# v2 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local -e JAVA_OPTS=${JAVA_OPTS} openapitools/openapi-generator-cli generate \
    --input-spec swagger/swagger.v2.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template \
    -Dapis -DapiTests=false -DapiDocs=false \
    --ignore-file-override=/local/.openapi-generator-ignore_v2

cat partial-header/generated_api_partial_header_v2.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api2.py

rm -Rf out/openapi_client

# v1 apiのmodelからDataClass用のpythonファイルを生成する。
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local  -e JAVA_OPTS=${JAVA_OPTS} \
    openapitools/openapi-generator-cli generate \
    --input-spec swagger/swagger.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template_dataclass \
    -Dmodels -DmodelTests=false -DmodelDocs=false \

MODELS_DIR=out/openapi_client/models

############################
# DataClassを作成
############################


# Annotation
declare -a model_files=(${MODELS_DIR}/point.py \
 ${MODELS_DIR}/additional_data.py \
 ${MODELS_DIR}/full_annotation_additional_data.py \
 ${MODELS_DIR}/full_annotation_detail.py \
 ${MODELS_DIR}/full_annotation.py \
 ${MODELS_DIR}/simple_annotation_detail.py \
 ${MODELS_DIR}/simple_annotation.py \
 ${MODELS_DIR}/single_annotation_detail.py \
 ${MODELS_DIR}/single_annotation.py \
 ${MODELS_DIR}/annotation_detail.
 ${MODELS_DIR}/annotation.py \
)
cat partial-header/dataclass/common.py partial-header/dataclass/annotation.py  \
 ${model_files[@]} > ../annofabapi/dataclass/annotation.py

# Annotation Specs
declare -a model_files=(${MODELS_DIR}/keybind.py \
 ${MODELS_DIR}/position_for_minimum_bounding_box_insertion.py \
 ${MODELS_DIR}/label_v1_bounding_box_metadata.py \
 ${MODELS_DIR}/label_v1_segmentation_metadata.py \
 ${MODELS_DIR}/internationalization_message_messages.py \
 ${MODELS_DIR}/internationalization_message.py \
 ${MODELS_DIR}/inspection_phrase.py \
 ${MODELS_DIR}/annotation_specs_history.py \
 ${MODELS_DIR}/color.py \
 ${MODELS_DIR}/additional_data_definition_v1_choices.py \
 ${MODELS_DIR}/additional_data_definition_v1.py \
 ${MODELS_DIR}/additional_data_definition_v2.py \
 ${MODELS_DIR}/annotation_editor_feature.py \
 ${MODELS_DIR}/label_v1.py \
 ${MODELS_DIR}/label_v2.py \
 ${MODELS_DIR}/additional_data_restriction.py \
 ${MODELS_DIR}/annotation_specs_v1.py \
 ${MODELS_DIR}/annotation_specs_v2.py \
)
cat partial-header/dataclass/common.py partial-header/dataclass/annotation_specs.py  \
 ${model_files[@]} > ../annofabapi/dataclass/annotation_specs.py

# Input
declare -a model_files=(${MODELS_DIR}/resolution.py ${MODELS_DIR}/input_data.py)
cat partial-header/dataclass/common.py partial-header/dataclass/input.py  \
 ${model_files[@]} > ../annofabapi/dataclass/input.py

# Inspection
declare -a model_files=(${MODELS_DIR}/inspection.py)
cat partial-header/dataclass/common.py partial-header/dataclass/inspection.py  \
 ${model_files[@]} > ../annofabapi/dataclass/inspection.py

# Instruction
declare -a model_files=(${MODELS_DIR}/instruction.py ${MODELS_DIR}/instruction_history.py ${MODELS_DIR}/instruction_image.py)
cat partial-header/dataclass/common.py partial-header/dataclass/instruction.py  \
 ${model_files[@]} > ../annofabapi/dataclass/instruction.py

# Job
declare -a model_files=(${MODELS_DIR}/job_info.py)
cat partial-header/dataclass/common.py partial-header/dataclass/job.py  \
 ${model_files[@]} > ../annofabapi/dataclass/job.py

# My
declare -a model_files=(${MODELS_DIR}/my_organization.py ${MODELS_DIR}/my_account.py)
cat partial-header/dataclass/common.py partial-header/dataclass/my.py  \
 ${model_files[@]} > ../annofabapi/dataclass/my.py

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

# Project Member
declare -a model_files=(${MODELS_DIR}/project_member.py)
cat partial-header/dataclass/common.py partial-header/dataclass/project_member.py  \
 ${model_files[@]} > ../annofabapi/dataclass/project_member.py

# Statistics
declare -a model_files=(${MODELS_DIR}/project_task_statistics.py ${MODELS_DIR}/project_task_statistics_history.py \
 ${MODELS_DIR}/project_account_statistics_history.py ${MODELS_DIR}/project_account_statistics.py \
 ${MODELS_DIR}/inspection_statistics_phrases.py ${MODELS_DIR}/inspection_statistics_breakdown.py ${MODELS_DIR}/inspection_statistics.py \
 ${MODELS_DIR}/phase_statistics.py ${MODELS_DIR}/task_phase_statistics.py \
 ${MODELS_DIR}/label_statistics.py  \
 ${MODELS_DIR}/histogram_item.py ${MODELS_DIR}/worktime_statistics_item.py ${MODELS_DIR}/account_worktime_statistics.py ${MODELS_DIR}/worktime_statistics.py  \
 ${MODELS_DIR}/marker.py ${MODELS_DIR}/markers.py
)
cat partial-header/dataclass/common.py partial-header/dataclass/statistics.py  \
 ${model_files[@]} > ../annofabapi/dataclass/statistics.py

# Supplementary
declare -a model_files=(${MODELS_DIR}/supplementary_data.py)
cat partial-header/dataclass/common.py partial-header/dataclass/supplementary.py  \
 ${model_files[@]} > ../annofabapi/dataclass/supplementary.py

# Task
declare -a model_files=(${MODELS_DIR}/task_history.py ${MODELS_DIR}/task_history_short.py ${MODELS_DIR}/task.py)
cat partial-header/dataclass/common.py partial-header/dataclass/task.py  \
 ${model_files[@]} > ../annofabapi/dataclass/task.py

# Webhook
declare -a model_files=(${MODELS_DIR}/webhook_header.py ${MODELS_DIR}/webhook.py)
cat partial-header/dataclass/common.py partial-header/dataclass/webhook.py  \
 ${model_files[@]} > ../annofabapi/dataclass/webhook.py


sed  -e "s/__DictStrKeyAnyValue__/Dict[str,Any]/g"  ../annofabapi/dataclass/*.py  --in-place
# dict(str, int) -> Dict[str, int]
sed -E -e "s/dict\((.*)\)/Dict\[\1\]/g"  ../annofabapi/dataclass/*.py  --in-place


rm -Rf out/openapi_client


cd ../

# Format
FORMATTED_FILE="annofabapi/generated_api.py annofabapi/generated_api2.py annofabapi/models.py annofabapi/dataclass/*.py"
pipenv run isort  ${FORMATTED_FILE}
pipenv run yapf  --in-place ${FORMATTED_FILE}

popd

# Dictの型を修正
# SimpleAnnotationDetail.attributes, JobInfo
# InspectionStatisticsPhrases, InspectionStatisticsBreakdown