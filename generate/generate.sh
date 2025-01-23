#!/bin/bash -uex

DOCKER_IMAGE=openapitools/openapi-generator-cli:v7.11.0

PROGNAME=$(basename $0)

usage_exit() {
        echo "Usage: ${PROGNAME} [--download]" 1>&2
        exit 1
}

FLAG_DOWNLOAD=false


if [ $# -gt 0 ]; then
    for OPT in "$@"
    do
    case ${OPT} in
        "--download")
            FLAG_DOWNLOAD=true
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


# swagger.yamlを修正したいときがあるので、
if "${FLAG_DOWNLOAD}"; then
    curl https://annofab.com/docs/api/swagger.yaml --output swagger/swagger.yaml
    curl https://annofab.com/docs/api/swagger.v2.yaml --output swagger/swagger.v2.yaml
    curl https://annofab.com/docs/api/swagger-api-components.yaml  --output swagger/swagger-api-components.yaml
fi


JAVA_OPTS="-Dlog.level=info"

# `__DictStrKeyAnyValue__`の意味：あとで`dict[str,Any]`に置換できるようにするための無意味な値
OPENAPI_GENERATOR_CLI_COMMON_OPTION="--generator-name python \
    --output /local/out \
    --type-mappings array=list,DateTime=str,date=str,object=__DictStrKeyAnyValue__"

# v1 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local  -e JAVA_OPTS=${JAVA_OPTS} ${DOCKER_IMAGE} generate \
    --input-spec swagger/swagger.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template \
    --global-property apis,apiTests=false,apiDocs=false \
    --ignore-file-override=/local/.openapi-generator-ignore_v1

cat partial-header/generated_api_partial_header_v1.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api.py
# delete_project_job メソッドのjob_type引数の型がJobTypeだと、他のメソッドと統一感がなくなるので、型をstrに変換する
sed  -e "s/job_type: ProjectJobType/job_type: str/g"  ../annofabapi/generated_api.py  --in-place

rm -Rf out/openapi_client

# v2 apiを生成
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local -e JAVA_OPTS=${JAVA_OPTS} ${DOCKER_IMAGE} generate \
    --input-spec swagger/swagger.v2.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template \
    --global-property apis,apiTests=false,apiDocs=false \
    --ignore-file-override=/local/.openapi-generator-ignore_v2

cat partial-header/generated_api_partial_header_v2.py out/openapi_client/api/*_api.py > ../annofabapi/generated_api2.py
rm -Rf out/openapi_client


# modelsを生成
cat swagger/swagger-partial-header.yaml swagger/swagger-api-components.yaml > swagger/swagger-models.yaml

# datetime型を含むクラスでは、JSONにserializeiできなかったので、str型にする
# https://github.com/OpenAPITools/openapi-generator/issues/19517
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local -e JAVA_OPTS=${JAVA_OPTS} ${DOCKER_IMAGE} generate \
    --input-spec swagger/swagger-models.yaml \
    --generator-name python \
    --output /local/out \
    --type-mappings DateTime=str,date=str \
    --global-property models,modelTests=false,modelDocs=false \

sed 's/from openapi_client.models./from annofabapi.pydantic_models./g' out/openapi_client/models/*.py --in-place


replace_from_dict_method() {
    # `from_json`メソッドで`_type`が正しくない場合は`ValueError`を発生させるようにする
    # 本来は`from_dict`メソッドを修正すべきだが、
    local type_value=$1
    local filename=$2
    sed "s/return cls\.from_dict(json\.loads(json_str))/result = cls.from_dict(json.loads(json_str))\\n        if result.type != \"$type_value\": raise ValueError(\"Invalid type\")\\n        return result/" out/openapi_client/models/${filename} --in-place
}
# `from_dict`メソッドで`oneOf`に該当するスキーマが複数見つかる場合はErrorが発生する
# その場合は、`type`の値を判定するようにした
replace_from_dict_method Movie system_metadata_movie.py
replace_from_dict_method Image system_metadata_image.py
replace_from_dict_method Custom system_metadata_custom.py
replace_from_dict_method Classification full_annotation_data_classification.py
replace_from_dict_method Segmentation full_annotation_data_segmentation.py
replace_from_dict_method SegmentationV2 full_annotation_data_segmentation_v2.py


cp out/openapi_client/models/*.py ../annofabapi/pydantic_models
rm -Rf out/openapi_client


DOCKER_IMAGE=openapitools/openapi-generator-cli:v4.3.1
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local -e JAVA_OPTS=${JAVA_OPTS} ${DOCKER_IMAGE} generate \
    --input-spec swagger/swagger-models.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template \
    --global-property models,modelTests=false,modelDocs=false \
    --ignore-file-override=/local/.openapi-generator-ignore_v1

cat partial-header/models_partial_header_v1.py out/openapi_client/models/*.py partial-footer/models_partial_footer.py> ../annofabapi/models.py
rm -Rf out/openapi_client

# v1 apiのmodelからDataClass用のpythonファイルを生成する。
docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local -w /local  -e JAVA_OPTS=${JAVA_OPTS} \
    ${DOCKER_IMAGE} generate \
    --input-spec swagger/swagger-models.yaml \
    ${OPENAPI_GENERATOR_CLI_COMMON_OPTION} \
    --template-dir /local/template_dataclass \
    --global-property models,modelTests=false,modelDocs=false  \

MODELS_DIR=out/openapi_client/models
rm swagger/swagger-models.yaml

############################
# DataClassを作成
############################

# Annotation
declare -a model_files=(${MODELS_DIR}/point.py \
 ${MODELS_DIR}/full_annotation_data_classification.py \
 ${MODELS_DIR}/full_annotation_data_segmentation.py \
 ${MODELS_DIR}/full_annotation_data_segmentation_v2.py \
 ${MODELS_DIR}/full_annotation_data_bounding_box.py \
 ${MODELS_DIR}/full_annotation_data_points.py \
 ${MODELS_DIR}/full_annotation_data_single_point.py \
 ${MODELS_DIR}/full_annotation_data_range.py \
 ${MODELS_DIR}/additional_data_v1.py \
 ${MODELS_DIR}/additional_data_v2.py \
 ${MODELS_DIR}/full_annotation_additional_data.py \
 ${MODELS_DIR}/full_annotation_detail.py \
 ${MODELS_DIR}/full_annotation.py \
 ${MODELS_DIR}/simple_annotation_detail.py \
 ${MODELS_DIR}/simple_annotation.py \
 ${MODELS_DIR}/single_annotation_detail_v1.py \
 ${MODELS_DIR}/single_annotation_detail_v2.py \
 ${MODELS_DIR}/single_annotation_v1.py \
 ${MODELS_DIR}/single_annotation_v2.py \
 ${MODELS_DIR}/annotation_detail_v1.py \
 ${MODELS_DIR}/annotation_v1.py \
 ${MODELS_DIR}/annotation_props_for_editor.py \
 ${MODELS_DIR}/additional_data_value_flag.py \
 ${MODELS_DIR}/additional_data_value_integer.py \
 ${MODELS_DIR}/additional_data_value_comment.py \
 ${MODELS_DIR}/additional_data_value_text.py \
 ${MODELS_DIR}/additional_data_value_choice.py \
 ${MODELS_DIR}/additional_data_value_select.py \
 ${MODELS_DIR}/additional_data_value_tracking.py \
 ${MODELS_DIR}/additional_data_value_link.py \
 ${MODELS_DIR}/annotation_detail_content_input_inner.py \
 ${MODELS_DIR}/annotation_detail_content_input_outer.py \
 ${MODELS_DIR}/annotation_detail_v2_create.py \
 ${MODELS_DIR}/annotation_detail_v2_import.py \
 ${MODELS_DIR}/annotation_detail_v2_update.py \
 ${MODELS_DIR}/annotation_v2_input.py \
 ${MODELS_DIR}/annotation_detail_content_output_inner.py \
 ${MODELS_DIR}/annotation_detail_content_output_inner_unknown.py \
 ${MODELS_DIR}/annotation_detail_content_output_outer.py \
 ${MODELS_DIR}/annotation_detail_content_output_outer_unresolved.py \
 ${MODELS_DIR}/annotation_detail_v2_get.py \
 ${MODELS_DIR}/annotation_v2_output.py \
)
cat partial-header/dataclass/common.py partial-header/dataclass/annotation.py  \
 ${model_files[@]} > ../annofabapi/dataclass/annotation.py

# Annotation Specs
declare -a model_files=(${MODELS_DIR}/keybind.py \
 ${MODELS_DIR}/position_for_minimum_bounding_box_insertion.py \
 ${MODELS_DIR}/bounding_box_metadata.py \
 ${MODELS_DIR}/segmentation_metadata.py \
 ${MODELS_DIR}/internationalization_message_messages.py \
 ${MODELS_DIR}/internationalization_message.py \
 ${MODELS_DIR}/inspection_phrase.py \
 ${MODELS_DIR}/annotation_specs_history.py \
 ${MODELS_DIR}/color.py \
 ${MODELS_DIR}/additional_data_definition_v1_choices.py \
 ${MODELS_DIR}/additional_data_definition_v1.py \
 ${MODELS_DIR}/additional_data_definition_v2.py \
 ${MODELS_DIR}/annotation_editor_feature.py \
 ${MODELS_DIR}/annotation_type_field_value_minimum_size.py \
 ${MODELS_DIR}/annotation_type_field_value_minimum_size2d_with_default_insert_position.py \
 ${MODELS_DIR}/annotation_type_field_value_margin_of_error_tolerance.py \
 ${MODELS_DIR}/annotation_type_field_value_vertex_count_min_max.py \
 ${MODELS_DIR}/annotation_type_field_value_minimum_area2d.py \
 ${MODELS_DIR}/annotation_type_field_value_display_line_direction.py \
 ${MODELS_DIR}/annotation_type_field_value_annotation_editor_feature.py \
 ${MODELS_DIR}/annotation_type_field_value_one_integer_field_value.py \
 ${MODELS_DIR}/annotation_type_field_value_one_string_field_value.py \
 ${MODELS_DIR}/annotation_type_field_value_one_boolean_field_value.py \
 ${MODELS_DIR}/annotation_type_field_value_empty_field_value.py \
 ${MODELS_DIR}/label_v1.py \
 ${MODELS_DIR}/label_v2.py \
 ${MODELS_DIR}/additional_data_restriction.py \
 ${MODELS_DIR}/annotation_specs_v1.py \
 ${MODELS_DIR}/annotation_specs_v2.py \
 ${MODELS_DIR}/label_v3.py \
 ${MODELS_DIR}/annotation_specs_v3.py \
 
)
cat partial-header/dataclass/common.py partial-header/dataclass/annotation_specs.py  \
 ${model_files[@]} > ../annofabapi/dataclass/annotation_specs.py

# comment
declare -a model_files=(${MODELS_DIR}/comment.py)
cat partial-header/dataclass/common.py partial-header/dataclass/comment.py  \
 ${model_files[@]} > ../annofabapi/dataclass/comment.py

# Input
declare -a model_files=(${MODELS_DIR}/resolution.py ${MODELS_DIR}/input_data.py)
cat partial-header/dataclass/common.py partial-header/dataclass/input.py  \
 ${model_files[@]} > ../annofabapi/dataclass/input.py

# Organization
declare -a model_files=(${MODELS_DIR}/organization.py)
cat partial-header/dataclass/common.py partial-header/dataclass/organization.py  \
 ${model_files[@]} > ../annofabapi/dataclass/organization.py

# Organization Member
declare -a model_files=(${MODELS_DIR}/organization_member.py)
cat partial-header/dataclass/common.py partial-header/dataclass/organization_member.py  \
 ${model_files[@]} > ../annofabapi/dataclass/organization_member.py

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

# `dict(str, int)` を `dict[str, int]`のように置換する
sed -E -e "s/dict\((.*)\)/dict\[\1\]/g"  ../annofabapi/dataclass/*.py  --in-place
# Task.metadataなどでは、`__DictStrKeyAnyValue__`を`dict[str, Any]`に置換すると正しい型にならないので、無理やり正しい型に置換する
sed -e  "s/dict\[str, __DictStrKeyAnyValue__\]/dict[str, Any]/g" ../annofabapi/dataclass/*.py  --in-place 
# `__DictStrKeyAnyValue__`を`dict[str, Any]`に置換する
sed  -e "s/__DictStrKeyAnyValue__/dict[str,Any]/g"  ../annofabapi/dataclass/*.py  --in-place



rm -Rf out/openapi_client

pushd ../

# Format
make format

# rstファイルの自動生成
docs/create_pydantic_modes_rst.sh

popd
popd

# Dictの型を修正
# SimpleAnnotationDetail.attributes, JobInfo
# InspectionStatisticsPhrases, InspectionStatisticsBreakdown