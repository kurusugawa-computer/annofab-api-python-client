# annofab-api-python-client
[Annofab Web API](https://annofab.com/docs/api/) のPythonクライアントライブラリです。

[![Build Status](https://github.com/kurusugawa-computer/annofab-api-python-client/actions/workflows/lint-test.yml/badge.svg)](https://github.com/kurusugawa-computer/annofab-api-python-client/actions)
[![PyPI version](https://badge.fury.io/py/annofabapi.svg)](https://badge.fury.io/py/annofabapi)
[![Python Versions](https://img.shields.io/pypi/pyversions/annofabapi.svg)](https://pypi.org/project/annofabapi/)





* **Annofab Web API Documentation:** https://annofab.com/docs/api/
* **Reference Documentation:** https://annofab-api-python-client.readthedocs.io/en/latest/
* **annofab-cli** https://github.com/kurusugawa-computer/annofab-cli
    * 「タスクの一括差し戻し」や、「プロジェクト間の差分表示」など、Annofabの画面で実施するには時間がかかる操作を、CLIツールとして提供しています。
* **開発者用ドキュメント**: [README_for_developer.md](https://github.com/kurusugawa-computer/annofab-api-python-client/blob/main/README_for_developer.md)




# 注意
* 作者または著作権者は、ソフトウェアに関してなんら責任を負いません。
* 現在、APIは開発途上版です。予告なく互換性のない変更がある可能性をご了承ください。
* put, post, delete系のメソッドを間違えて実行してしまわないよう、注意してください。特に「プロジェクト削除」や「アノテーション仕様更新」のAPIには十分注意してください。
 
# 廃止予定
https://annofab-api-python-client.readthedocs.io/en/latest/deprecations.html を参照してください。


# Features
cURLやPostmanなどよりも簡単にAnnofab Web APIにアクセスできます。

* ログインを意識せずに、APIを利用できます。
* アクセス過多などで失敗した場合は、リトライされます。
* 「画像を入力データとして登録する」機能など、APIを組み合わせた機能も利用できます。



# Requirements
* Python 3.12+

# Install

```
$ pip install annofabapi
```

https://pypi.org/project/annofabapi/

# Usage

## インスタンス生成

認証にはパーソナルアクセストークン（PAT）の利用を推奨します。

### user_id, passwordをコンストラクタ引数に渡す場合

```python
# APIアクセス用のインスタンスを生成
from annofabapi import build


user_id = "XXXXXX"
password = "YYYYYY"

service = build(user_id, password)
```

### PersonalAccessTokenをコンストラクタ引数に渡す場合

```python
# APIアクセス用のインスタンスを生成
from annofabapi import build


pat = "XXXXXX"

service = build(pat = pat)
```


### 環境変数に認証情報を設定する場合


* IDとパスワードで認証する場合
    * 環境変数`ANNOFAB_USER_ID`、`ANNOFAB_PASSWORD`にユーザIDとパスワードを設定します。
* パーソナルアクセストークンで認証する場合
    * 環境変数`ANNOFAB_PAT`にトークンを設定します。
    * `ANNOFAB_PAT`が設定されている場合、`ANNOFAB_USER_ID`、`ANNOFAB_PASSWORD`は無視されます。

```python
from annofabapi import build_from_env
service = build_from_env()
```


### 引数なしでインスタンスを生成する場合
``build()`` を実行すると、環境変数から認証情報を読み込みます。

```python
from annofabapi import build
service = build()
```

優先順位は以下の通りです。
1. `ANNOFAB_PAT`
2. `ANNOFAB_USER_ID`及び`ANNOFAB_PASSWORD`


## APIメソッドの引数

`service.api`・`service.api2` の生成されたAPIメソッドでは、`query_params`・`header_params`・`request_body` はキーワード専用引数です。パス引数は位置引数でも指定できます。

これらを位置引数で渡していたコードは、次のようにキーワード指定へ変更してください。位置引数で渡すと `TypeError` になります。

```python
# 変更前（TypeErrorになる呼び出し）
service.api.put_annotation(project_id, task_id, input_data_id, query_params, request_body)

# 変更後
service.api.put_annotation(
    project_id, task_id, input_data_id,
    query_params=query_params,
    request_body=request_body,
)
```

引数名を明示することで、API仕様の更新で引数が追加されても、別の引数として解釈されることを防ぎます。

## `service.api`のサンプルコード

* `service.api`には、Web APIに対応するメソッドが定義されています。
* メソッド名は、[Annofab Web APIのOpenAPI specification](https://annofab.com/docs/api/swagger.yaml)に記載されている`operationId`を、スネークケースに変換したものです。
* 各メソッドの戻り値の型は`Tupple[Content, Response]`です。
Responseは[requestsモジュールのReponseオブジェクト](https://2.python-requests.org/en/master/api/#requests.Response)です。
ContentはReponseの中身です。

```python
project_id = "ZZZZZZ"
# `status`が`complete`のタスクを取得する
content, response = service.api.get_tasks(project_id, query_params={"status": "complete"})

print(type(content))
# <class 'dict'>
print(content)
# {'list': [{'project_id': 'ZZZZZZ', 'task_id': '20190317_2', 'phase': 'acceptance', ...

print(type(response))
# <class 'requests.models.Response'>
print(response.headers["Content-Type"])
# application/json
```

## `service.wrapper`のサンプルコード

`service.wrapper`には、`server.api`を組み合わせたメソッドが定義されています。


```python
# `status`が`complete`のタスクすべてを取得する
tasks = service.wrapper.get_all_tasks(project_id, query_params={"status": "complete"})
print(type(tasks))
# <class 'list'>
print(tasks)
# [{'project_id': 'ZZZZZZ', 'task_id': '20190317_2', 'phase': 'acceptance', ...


# simpleアノテーションzipのダウンロード
service.wrapper.download_annotation_zip(project_id, 'output_dir/simple_annotation.zip')

# 画像ファイルを入力データとして登録する
service.wrapper.put_input_data_from_file(project_id, 'sample_input_data_id', f'sample.png')
```

## アノテーションzipの読み込み
ダウンロードしたアノテーションzipを、JSONファイルごとに読み込みます。
zipファイルを展開したディレクトリも読み込み可能です。

```python
import zipfile
from pathlib import Path
from annofabapi.parser import lazy_parse_simple_annotation_dir, lazy_parse_simple_annotation_zip, SimpleAnnotationZipParser, SimpleAnnotationDirParser, lazy_parse_simple_annotation_zip_by_task


# Simpleアノテーションzipの読み込み
iter_parser = lazy_parse_simple_annotation_zip(Path("simple-annotation.zip"))
for parser in iter_parser:
    simple_annotation = parser.parse()
    print(simple_annotation)

# Simpleアノテーションzipを展開したディレクトリの読み込み
iter_parser = lazy_parse_simple_annotation_dir(Path("simple-annotation-dir"))
for parser in iter_parser:
    simple_annotation = parser.parse()
    print(simple_annotation)

# Simpleアノテーションzipをタスク単位で読み込む
task_iter_parser = lazy_parse_simple_annotation_zip_by_task(Path("simple-annotation.zip"))
for task_parser in task_iter_parser:
    print(task_parser.task_id)
    for parser in task_parser.lazy_parse():
        simple_annotation = parser.parse()
        print(simple_annotation)
        

# Simpleアノテーションzip内の1個のJSONファイルを読み込み
with zipfile.ZipFile('simple-annotation.zip', 'r') as zip_file:
    parser = SimpleAnnotationZipParser(zip_file, "task01/12345678-abcd-1234-abcd-1234abcd5678.json")
    simple_annotation = parser.parse()
    print(simple_annotation)

# Simpleアノテーションzip内を展開したディレクトリ内の1個のJSONファイルを読み込み
parser = SimpleAnnotationDirParser(Path("task01/12345678-abcd-1234-abcd-1234abcd5678.json"))
simple_annotation = parser.parse()
print(simple_annotation)


```

### 塗りつぶし画像の読み込み
`annofabapi.segmentation` には、アノテーションZIPに格納されている塗りつぶし画像を扱うための関数が用意されています。
利用する場合は、以下のコマンドを実行してください。

```
$ pip install annofabapi[segmentation]
```



## DataClass
`annofabapi.dataclass`に、データ構造用のクラスがあります。
これらのクラスを利用すれば、属性で各値にアクセスできます。

```python
from annofabapi.dataclass.task import Task
dict_task, _ = service.api.get_task(project_id, task_id)
task = Task.from_dict(dict_task)

print(task.task_id)
print(task.status)

```




## 備考

### `annofabapi`のログを出力する方法（サンプル）

```python
import logging
logging_formatter = '%(levelname)-8s : %(asctime)s : %(name)s : %(message)s'
logging.basicConfig(format=logging_formatter)
logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)
```

