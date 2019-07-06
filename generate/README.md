# 概要
[OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator)を使って、`annofabapi/generated_api.py`を生成します。


# 設計方針
AnnoFab WebAPIのswagger.yamlが多少間違っていても、クライアントライブラリが動くようなメソッド設計になっています。
swagger.yamlの間違いを許容する部分と許容しない部分は以下の通りです。

* 許容する部分
    * query_paramsの中身
    * header_paramsの中身
    * request_bodyの中身
* 許容しない部分
    * path_paramの中身
    * path
    * http method


## メソッド設計
### メソッド名
* `operationId`をスネークケースに変換したもの

### 引数
* Path Prametersの中身を引数にする。
* APIにQuery Parametersがあれば、引数に`query_params`を追加する。
* APIにHeader Parametersがあれば、引数に`header_params`を追加する。
* APIにRequest Bodyがあれば、引数に`request_body`を追加する。

### 戻り値
* `Tuple[Content, Reponse]`
    * `Content`：Responseの中身。
    * `Reponse`：Response自信。ReponseのLocationヘッダを参照するときもあるので、Responseも返すようにした。


# 生成方法

## Requirements
* Bash
* Docker

## ファイルの説明

```
generate/
│  generated_api_partial_header_v1.py
│  generated_api_partial_header_v2.py
│  enum_partial_header_v1.py
│  generate.sh
│
├─out/
│  
└─template
        api.mustache
        model.mustache

```

* `generate.sh`：`annofabapi/generated_api.py`を生成するBash Script
* `out/`：OpenAPI Generatorの出力先。
* `api.mustache`：APIに対応したメソッド用のテンプレートファイル。https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/resources/python/api.mustache からダウンロードしたファイルをカスタマイズした。
* `model.mustache`：schemeに列挙体用のテンプレートファイル。https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/resources/python/model.mustache からダウンロードしたファイルをカスタマイズした。
* `generated_api_partial_header_v1.py`：`annofabapi/generated_api.py`のヘッダ部分（OpenAPI Generatorで生成しない部分）。
* `generated_api_partial_header_v2.py`：`annofabapi/generated_api2.py`のヘッダ部分（OpenAPI Generatorで生成しない部分）。
* `enums_partial_header.py`：`annofabapi/enums.py`のヘッダ部分（OpenAPI Generatorで生成しない部分）。

## 実行方法

```bash
# https://annofab.com/docs/api/swagger.yaml を元に生成します。
$ generate/generate.sh

```

### `openapi-gnerator-cli`でエラーが発生した場合

1. swagger.yamlをチェックする。

```
$ cd generate
$ docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local openapitools/openapi-generator-cli validate \
    -i /local/swagger.yaml \

```

2. swagger.yamlを修正する

3. ローカルにある`swagger.yaml`（ダウンロードしない）を元に、`generated_api.py`を生成する。

```bash
$ generate/generate.sh --notdownload
```