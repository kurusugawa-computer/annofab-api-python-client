# annofab-api-python-client
[Annofab Web API](https://annofab.com/docs/api/) のPythonクライアントライブラリです。

[![Build Status](https://app.travis-ci.com/kurusugawa-computer/annofab-api-python-client.svg?branch=main)](https://app.travis-ci.com/kurusugawa-computer/annofab-api-python-client)
[![CodeQL](https://github.com/kurusugawa-computer/annofab-api-python-client/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kurusugawa-computer/annofab-api-python-client/actions/workflows/codeql-analysis.yml)
[![PyPI version](https://badge.fury.io/py/annofabapi.svg)](https://badge.fury.io/py/annofabapi)
[![Python Versions](https://img.shields.io/pypi/pyversions/annofabapi.svg)](https://pypi.org/project/annofabapi/)
[![Documentation Status](https://readthedocs.org/projects/annofab-api-python-client/badge/?version=latest)](https://annofab-api-python-client.readthedocs.io/en/latest/?badge=latest)




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
現在ありません。


# Features
cURLやPostmanなどよりも簡単にAnnofab Web APIにアクセスできます。

* ログインを意識せずに、APIを利用できます。
* アクセス過多などで失敗した場合は、リトライされます。
* 「画像を入力データとして登録する」機能など、APIを組み合わせた機能も利用できます。



# Requirements
* Python 3.11+

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

### PersonalAccessTokenをコンストラクタ引数に渡す場合

```python
# APIアクセス用のインスタンスを生成
from annofabapi import build


pat = "XXXXXX"

service = build(pat = pat)
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


* IDとパスワードで認証する場合
    * 環境変数`ANNOFAB_USER_ID`、`ANNOFAB_PASSWORD`にユーザIDとパスワードを設定します。
* パーソナルアクセストークンで認証する場合
    * 環境変数`ANNOFAB_PAT`にトークンを設定します。
    * `ANNOFAB_PAT`が設定されている場合、`ANNOFAB_USER_ID`、`ANNOFAB_PASSWORD`は無視されます。

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
    1. `ANNOFAB_PAT`
    2. `ANNOFAB_USER_ID`及び`ANNOFAB_PASSWORD`
2. `.netrc`


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


## Simple Annotation ZIPの属性制約の検証

アノテーション仕様（APIのv3形式）の `restrictions` を使って、Simple Annotationの属性値を検証できます。
検証器はAPI通信を行いません。仕様は別途APIなどで取得してください。

```python
from pathlib import Path

import annofabapi.parser
from annofabapi.util.attribute_restriction_validation import AttributeRestrictionValidator

validator = AttributeRestrictionValidator(annotation_specs)
for parser in annofabapi.parser.lazy_parse_simple_annotation_zip(Path("simple-annotation.zip")):
    annotation = parser.load_json()
    results = validator.validate_simple_annotation_details(annotation["details"])
    for violation in results:
        print(annotation["task_id"], annotation["input_data_id"], violation)
```

- 引数には同一タスク・同一入力データの `details` 全件を渡してください。リンク先の検索にも使用します。
- 結果は違反した「アノテーション × トップレベルの制約」で1件です。`restriction_index` は仕様の `restrictions` 内の0始まりの位置です。
- 各違反は `annotation_id`、`attribute_id`、`attribute_name`、`restriction_index` の4項目を持ちます。
  `attribute_name` は仕様上の英語名で、Simple Annotationの `attributes` のキーに対応します。
  成立・適用対象外の制約は返さず、違反0件なら空リストです。制約0件・アノテーション0件の場合も空リストです。
- `Equals` / `NotEquals`、`Matches` / `NotMatches`、ネストした `Imply`、`HasLabel` に対応します。
  `Imply` の前提がfalseの場合は違反を返しません。前提がtrueの場合に後続条件を評価し、違反時は後続条件の属性ID・英語名を返します。
- ラベルに属さない属性への制約、読取専用属性への制約、結論が `CanInput` の制約は結果に含めません。
  条件付き `CanInput` による他の制約の有効・無効の切り替えは再現しません。
- 未設定・nullは空値、チェックボックスの未設定・null・空文字はfalseと扱います。デフォルト値の補完や空白の除去は行いません。
  整数は数値として比較し、選択式の英語名は仕様の選択肢IDに対応付けます。
- 正規表現はPythonの `re.fullmatch` による全体一致です。例えば `\d` は数字1桁に一致し、2桁の数字には一致しません。
  Annofabの正規表現と完全互換ではありません。
- `HasLabel` は空リンクを許可します（必須条件は別途 `NotEquals ""` で評価）。許可ラベルが空のときはラベルを制限しません。
  空でないリンクの参照先が見つからない場合は `ValueError` にします。
- 評価に必要な名前を解決できない場合、不正な属性値・正規表現、未対応条件は `ValueError` にします。
  検証を中断するため、途中までの違反一覧は返しません。Implyの前提が評価できない場合も同様です。
- 属性名は対象ラベル内で解決します。別ラベル間で同じ属性名が使われていても構いませんが、
  同じラベル内で属性名が重複して一意に解決できない場合は `ValueError` にします。
  ラベルの英語名、参照する選択肢の英語名が重複して一意に解決できない場合も同様です。

Annofabの提出時検証を完全に再現する機能ではありません。
ZIPと仕様の英語名を対応付けるため、可能ならZIPに対応する時点の仕様を使用してください。
現在の仕様を渡した場合は、ZIPの値を現在の仕様に照らして検証します。
