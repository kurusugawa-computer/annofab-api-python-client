# annofab-api-python-Client
AnnoFab Web APIのPythonクライアントライブラリです。
https://annofab.com/docs/api/

# 注意
* 作者または著作権者は、ソフトウェアに関してなんら責任を負いません。
* 現在、APIは開発途上版です。予告なく互換性のない変更がある可能性をご了承ください。
* put, post, delete系のメソッドを間違えて実行してしまわないよう、注意してください。特に「プロジェクト削除」や「アノテーション仕様更新」APIは十分注意してください。
 


# Features
* ログインを意識せずに、APIを利用できます。
* アクセス過多などで失敗した場合は、リトライされます。
* 「画像を入力データとして登録する」機能など、APIを組み合わせた機能を利用できます。

# Requirements
* python 3.5+

# Install
TODO

# Usage

## インスタンス生成

```python
# APIアクセス用のインスタンスを生成
from annofabapi import build


user_id = "XXXXXX"
password = "YYYYYY"
project_id = "ZZZZZZ"

service = build(user_id, password)
```

## `service.api`のサンプルコード

* `service.api`には、Web APIに対応するメソッドが定義されています。
* メソッド名は、[AnnoFab Web APIのOpenAPI specification](https://annofab.com/docs/api/swagger.yaml)に記載されている`operationId`をスネークケースに変換したものです。
* 各メソッドの戻り値は`Tupple[Content, Response]`です。
Responseは[requestsモジュールのReponseオブジェクト](https://2.python-requests.org/en/master/api/#requests.Response)です。

```python
# `status`が`complete`のタスクを取得する
content, response = service.api.get_tasks(project_id, query_params={'status': 'complete'})
print(content)
# {'list': [{'project_id': ...

# simpleアノテーションzipのダウンロード用URLを取得する
content, response = service.api.get_annotation_archive(project_id)
url = response.headers['Location']
```

## `service.wrapper`のサンプルコード

`service.wrapper`は、APIを組み合わせたメソッドが定義されています。


```python
# `status`が`complete`のタスクすべてを取得する
content, response = service.wrapper.get_all_tasks(project_id, query_params={'status': 'complete'})
print(content)
# [{'project_id': ...

# simpleアノテーションzipのダウンロード
service.wrapper.download_annotation_archive(project_id, 'output_dir')

# 画像ファイルを入力データとして登録する
service.wrapper.put_input_data_from_file(project_id, 'sample_input_data_id', f'sample.png')

src_project_id = "AAAAAA"
dest_project_id = "BBBBBB"

# プロジェクトメンバをコピー（誤って実行しないように注意すること）
service.wrapper.copy_project_members(src_project_id, dest_project_id)

# アノテーション仕様のコピー（誤って実行しないように注意すること）
service.wrapper.copy_annotation_specs(src_project_id, dest_project_id)
```

## 備考

### ログの出力方法の例

```python
import logging
logging_formatter = '%(levelname)s : %(asctime)s : %(name)s : %(funcName)s : %(message)s'
logging.basicConfig(format=logging_formatter)
logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)
```

### リトライの処理をカスタマイズ
TODO

# テスト実行方法

## 準備
1. pytest.iniにテスト対象のproject_idを指定. **プロジェクトが変更される恐れがあることに注意！！**
2. 以下の環境変数にAnnofabの認証情報を設定
    * `ANNOFAB_USER_ID`
    * `ANNOFAB_PASSWORD`
3. `pipenv run tox` でテスト実行

### 備考
* 基本的に、テストメソッドは、エラーが発生しないこと（HTTP STatus codeが400系でないこと）を確認しています。それより詳細な確認は行っていません。

    

# document生成方法

### Windowsの場合

```
> docs\make.bat
```


# ソースチェックツール

```bash
$ mypy annofabapi

$ flake8 

```


# その他

## 注意
* 以下のAPIは使用する機会が少ない or 使用する危険度が高いので、未実装です。
    * account関係のPUT, POST, DELETEメソッド
    * organization関係のPUT, POST, DELETEメソッド
    * project関係のPUT, POST, DELETEメソッド
* 予告なく互換性のない変更がある可能性があります。

予告なく互換性のない変更がある可能性があります。
メソッド名は、swagger.yamlのoperationIdと対応していません
作者または著作権者は、ソフトウェアに関してなんら責任を負いません。
put, post, delete系のメソッドを間違えて実行してしまわないよう、注意してください。


