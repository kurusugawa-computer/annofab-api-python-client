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

`generate/generate.sh`を実行すると、`annofabapi/api.py`が上書きされます。

```bash
$ generate/generate.sh
...
```


# swagger.yamlやAPIの不具合で正しく動かない部分

* `getInstruction`のContent-Type
* `get_instruction_image_url_for_put`に`header_params`がない


```
    def get_instruction_image_url_for_put(self, project_id, image_id, header_params: Optional[Dict[str, Any]] = None) -> Tuple[Any, requests.Response]:  # noqa: E501
        """作業ガイドの画像登録・更新用URL取得  # noqa: E501
        プロジェクトの作業ガイドの画像を登録するためのput先URLを取得します。  リクエストヘッダには、登録する画像に応じた適切な Content-Type を指定してください。   # noqa: E501
        Args:
            project_id (str):  プロジェクトID (required)
            image_id (str):  作業ガイド画像ID (required)

        Returns:
            Tuple[Any, requests.Response]

        """
        url_path = f'/projects/{project_id}/instruction-images/{image_id}/put-url'
        http_method = 'GET'
        keyword_params = {
            'header_params': header_params
        }

        return self._request_wrapper(http_method, url_path, **keyword_params)
```

