# 概要
[OpenAPI Generator](https://github.com/OpenAPITools/openapi-generator)を使って、ソースコードを生成する方法について記載します。

# ソースコードの自動生成

## Requirements
* Bash
* Docker

## ソースコードの生成方法
以下のコマンドを実行すると、ソースコードが生成されます。

```
# `generate/swagger/*.yaml`ファイルから、ソースコードを生成する
$ generate/generate.sh

# AnnoFab WebAPIのOpenAPI Spec を`generate/swagger/`にダウンロードしてから、ソースコードを生成する
$ generate/generate.sh --download

```


自動生成されるファイルの一覧です。

```
├── annofabapi
│   ├── dataclass
│   │   ├── *.py                       ... OpenAPI Specのスキーマに対応したDataClass
│   ├── generated_api.py                ... WebAPI v1に対応したメソッド
│   ├── generated_api2.py               ... WebAPI v2に対応したメソッド
│   ├── models.py                       ... OpenAPI Specのスキーマに対応したクラス（`Enum` or `Dict[str,Any]`）
```


## 各種ファイルの説明


```
├── generate
│   ├── generate.sh
│   ├── partial-header              ... 生成されるファイルのヘッダ部分。OpenAPI Generatorで生成したファイルとヘッダファイルをcatで連結して、ソースファイルを生成する。
│   │   ├── dataclass
│   │   │   ├── *.py
│   │   ├── generated_api_partial_header_v1.py
│   │   ├── generated_api_partial_header_v2.py
│   │   └── models_partial_header_v1.py
│   ├── template                ... `generated_api.py`, `generated_api2.py`, `models.py` を生成する際のテンプレートファイル
│   │   ├── api.mustache
│   │   └── model.mustache
│   └── template_dataclass      ... `dataclass/*.py`を生成する際のテンプレートファイル
│       └── model.mustache
```

### テンプレートファイルについて
テンプレートファイル（mustache）の書き方は[OpenAPI Generatorのドキュメント](https://openapi-generator.tech/docs/templating)を参照してください。
なお、annofabapiのテンプレートファイルは、以下のファイルを参考にしています。
* `api.mustache`：https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/resources/python/api.mustache
* `model.mustache`：https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/resources/python/model.mustache


### `openapi-gnerator-cli`でエラーが発生した場合
以下の手順に従ってください。

1. OpenAPI Specファイルをチェックする。

```
$ cd generate
$ docker run --rm   -u `id -u`:`id -g`  -v ${PWD}:/local openapitools/openapi-generator-cli validate  -i /local/swagger/swagger.yaml 
```

2. ローカルのOpenAPI Specファイル `generate/*.yaml` を修正する
3. `$ generate/generate.sh` コマンドを実行する。



# 設計方針
AnnoFab WebAPIのOpenAPI Specファイルが多少間違っていても、annofabapiは動くような設計になっています。

OpenAPI Specファイルの間違いを許容する部分/許容しない部分は以下の通りです。

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
* WebAPIにQuery Parametersがあれば、引数に`query_params`を追加する。
* WebAPIにHeader Parametersがあれば、引数に`header_params`を追加する。
* WebAPIにRequest Bodyがあれば、引数に`request_body`を追加する。
* WebAPIからRequest Bodyなどが不要になってもメソッドが動くようにするため、メソッド引数には`**kwarg`を用意する。


### 戻り値
* `Tuple[Content, Reponse]`
    * `Content`：Responseの中身。
    * `Reponse`：Response Object。ReponseのLocationヘッダを参照するときもあるので、Responseも返すようにした。

## クラス設計

### クラス名
OpenAPI Specのスキーマ名をクラス名にした。


### クラスの中身
#### models.py
OpenAPI Specのスキーマが`Enum`の場合は、列挙体クラスにした。
それ以外のクラスは、型ヒントとして利用できるよう、`Foo=Dict[str,Any]`のようにDict型のエイリアスとした。

#### dataclass/*.py
dictよりdataclassの方が扱いやすい場合があるので、よく使うクラスはDataClassとして定義した。


