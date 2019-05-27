# 概要
[OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator)を使って、`annofabapi/api.py`を生成します。


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
│  api_template.py
│  generate.sh
│
├─out/
│  
└─template
        api.mustache

```

* `generate.sh`：`annofabapi/api.py`を生成するBash Script
* `out/`：OpenAPI Generatorの出力先。
* `api.mustache`：APIに対応してメソッド用のテンプレートファイル。https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/resources/python/api.mustache からダウンロードしたファイルをカスタマイズした。
* `api_template.py`：`annofabapi/api.py`の自動生成しない部分。このファイルとOpenAPI Generatorが生成したファイルを連結して、`annofabapi/api.py`を生成する。

## 実行方法

`$ generate/generate.sh`を実行すると、`annofabapi/api.py`が上書きされます。
`$ generate/generate.sh --notdownload`を実行すると`generate/swagger.yaml`を使って`api.py`が生成されます。


```bash
$ generate/generate.sh


$ generate/generate.sh --notdownload

```
