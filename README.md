# annofab-api-python-client
[AnnoFab Web API](https://annofab.com/docs/api/) のPythonクライアントライブラリです。

[![Build Status](https://app.travis-ci.com/kurusugawa-computer/annofab-api-python-client.svg?branch=master)](https://app.travis-ci.com/kurusugawa-computer/annofab-api-python-client)
[![CodeQL](https://github.com/kurusugawa-computer/annofab-api-python-client/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kurusugawa-computer/annofab-api-python-client/actions/workflows/codeql-analysis.yml)
[![PyPI version](https://badge.fury.io/py/annofabapi.svg)](https://badge.fury.io/py/annofabapi)
[![Python Versions](https://img.shields.io/pypi/pyversions/annofabapi.svg)](https://pypi.org/project/annofabapi/)
[![Documentation Status](https://readthedocs.org/projects/annofab-api-python-client/badge/?version=latest)](https://annofab-api-python-client.readthedocs.io/en/latest/?badge=latest)




* **AnnoFab Web API Documentation:** https://annofab.com/docs/api/
* **Reference Documentation:** https://annofab-api-python-client.readthedocs.io/en/latest/
* **annofab-cli** https://github.com/kurusugawa-computer/annofab-cli
    * 「タスクの一括差し戻し」や、「プロジェクト間の差分表示」など、AnnoFabの画面で実施するには時間がかかる操作を、CLIツールとして提供しています。
* **開発者用ドキュメント**: [README_for_developer.md](https://github.com/kurusugawa-computer/annofab-api-python-client/blob/master/README_for_developer.md)




# 注意
* 作者または著作権者は、ソフトウェアに関してなんら責任を負いません。
* 現在、APIは開発途上版です。予告なく互換性のない変更がある可能性をご了承ください。
* put, post, delete系のメソッドを間違えて実行してしまわないよう、注意してください。特に「プロジェクト削除」や「アノテーション仕様更新」のAPIには十分注意してください。
 
# 廃止予定


### 2022-02-01 以降
* 以下の関数を非推奨にします。WebAPIが将来的に廃止されるためです。
    * AnnofabApi.get_labor_control
    * Wrapper.get_labor_control_worktime
    * Wrapper.get_labor_control_availability
* 統計関係の関数を非推奨にします。WebAPIが将来的に廃止されるためです。
   * annofabapi.Wrapper
       * get_task_statistics
       * get_account_statistics
       * get_inspection_statistics
       * get_task_phase_statistics
       * get_worktime_statistics
    * annofabapi.AnnofabApi
       * get_task_statistics
       * get_account_statistics
       * get_inspection_statistics
       * get_task_phase_statistics
       * get_worktime_statistics


# Features
cURLやPostmanなどよりも簡単にAnnoFab Web APIにアクセスできます。

* ログインを意識せずに、APIを利用できます。
* アクセス過多などで失敗した場合は、リトライされます。
* 「画像を入力データとして登録する」機能など、APIを組み合わせた機能も利用できます。



# Requirements
* Python 3.7+ 

# Install

```
$ pip install annofabapi
```

https://pypi.org/project/annofabapi/

# Usage

## インスタンス生成

### user_id, passwordをコンストラクタ引数に渡す場合

```python
# APIアクセス用のインスタンスを生成
from annofabapi import build


user_id = "XXXXXX"
password = "YYYYYY"

service = build(user_id, password)
```

### `.netrc`に認証情報を記載する場合
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


### 環境変数に認証情報を設定する場合
環境変数`ANNOFAB_USER_ID`、`ANNOFAB_PASSWORD`にユーザIDとパスワードを設定します。

```python
from annofabapi import build_from_env
service = build_from_env()
```


### `.netrc`または環境変数に認証情報を設定する場合
``build()`` を実行すると、環境変数または `.netrc` ファイルから認証情報を読み込みます。

```python
from annofabapi import build
service = build()
```

優先順位は以下の通りです。
1. 環境変数
2. `.netrc`


## `service.api`のサンプルコード

* `service.api`には、Web APIに対応するメソッドが定義されています。
* メソッド名は、[AnnoFab Web APIのOpenAPI specification](https://annofab.com/docs/api/swagger.yaml)に記載されている`operationId`を、スネークケースに変換したものです。
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
service.wrapper.download_annotation_archive(project_id, 'output_dir')

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
logging_formatter = '%(levelname)-8s : %(asctime)s : %(filename)s : %(name)s : %(funcName)s : %(message)s'
logging.basicConfig(format=logging_formatter)
logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)
```

