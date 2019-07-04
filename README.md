# annofab-api-python-client
[AnnoFab Web API](https://annofab.com/docs/api/)のPythonクライアントライブラリです。


# 注意
* 作者または著作権者は、ソフトウェアに関してなんら責任を負いません。
* 現在、APIは開発途上版です。予告なく互換性のない変更がある可能性をご了承ください。
* put, post, delete系のメソッドを間違えて実行してしまわないよう、注意してください。特に「プロジェクト削除」や「アノテーション仕様更新」のAPIには十分注意してください。
 


# Features
cURLやPostmanなどよりも簡単にAnnoFab Web APIにアクセスできます。

* ログインを意識せずに、APIを利用できます。
* アクセス過多などで失敗した場合は、リトライされます。
* 「画像を入力データとして登録する」機能など、APIを組み合わせた機能も利用できます。



# Requirements
* Python 3.6+

# Install

```
$ pip install annofabapi
```

https://pypi.org/project/annofabapi/

# Usage

## インスタンス生成

### user_id, passwordをコンストラクタ引数に渡す

```python
# APIアクセス用のインスタンスを生成
from annofabapi import build


user_id = "XXXXXX"
password = "YYYYYY"

service = build(user_id, password)
```

### `.netrc`に記載されたuser_id, passwordから生成
`.netrc`ファイルに、AnnofabのユーザIDとパスワードを記載します。

```plain:.netrc
machine annofab.com
login annofab_user_id
password annofab_password
```

```python
from annofabapi import build_from_netrc
service = build_from_netrc()
```


#### For Linux
* パスは`$HOME/.netrc`
* `$ chmod 600 $HOME/.netrc`でパーミッションを変更する



#### For Windows
* パスは`%USERPROFILE%\.netrc`


## `service.api`のサンプルコード

* `service.api`には、Web APIに対応するメソッドが定義されています。
* メソッド名は、[AnnoFab Web APIのOpenAPI specification](https://annofab.com/docs/api/swagger.yaml)に記載されている`operationId`をスネークケースに変換したものです。
* 各メソッドの戻り値の型は`Tupple[Content, Response]`です。
Responseは[requestsモジュールのReponseオブジェクト](https://2.python-requests.org/en/master/api/#requests.Response)です。
ContentはReponseの中身です。

```python
project_id = "ZZZZZZ"
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
tasks = service.wrapper.get_all_tasks(project_id, query_params={'status': 'complete'})
print(tasks)
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

### `annofabapi`のログを出力する方法（サンプル）

```python
import logging
logging_formatter = '%(levelname)-8s : %(asctime)s : %(filename)s : %(name)s : %(funcName)s : %(message)s'
logging.basicConfig(format=logging_formatter)
logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)
```

# Documentation
https://annofab-api-python-client.readthedocs.io/en/latest/


# CLIツール
「タスクの一括差し戻し」や、「プロジェクト間の差分表示」など、AnnoFabの画面で実施するには時間がかかる操作を、CLIツールとして提供しています。
詳しくは[annofab-cli](https://github.com/kurusugawa-computer/annofab-cli)を参照してください。

# Usage for Develper
[README_for_developer.md](README_for_developer.md)を参照してください。
