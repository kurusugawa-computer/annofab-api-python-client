# Usage for Developer
開発者用のドキュメントです。
ソースコードの生成、テスト実行、リリース手順などを記載します。

# Requirements
* Bash
* Docker (OpenAPI Generatorを実行するのに必要)
* python 3.6+

# Install
以下のコマンドを実行してください。開発に必要な環境が構築されます。

```bash
$ make init
```

# Test

## テストの実行方法
1. AnnoFabの認証情報を、`.netrc`ファイルまたは環境変数に設定する。
2. 以下のコマンドを実行して、テスト用のプロジェクトとタスクを作成する。
     * `poetry run python tests/create_test_project.py --organization ${MY_ORGANIZATION}`
3. `pytest.ini`に、テスト対象の`project_id`と`task_id`を指定する。
    * `task_id`はプロジェクト`project_id`配下であること
    * **【注意】テストを実行すると、AnnoFabプロジェクトの内容が変更される**
4. `$ make test`コマンドを実行する。


#### テストメソッドを指定してテストする方法

```
$ poetry run pytest tests/test_api.py::TestLogin::test_login
```

annofabapiでは、pytestのカスタムオプションを定義しています。

```
# ジョブを投げるテスト（時間がかかるテスト）を実行する。
$ poetry run pytest --run_submitting_job tests 

# annofabapiモジュールのログを表示する。
$ poetry run pytest --print_log_annofabapi tests 
```

#### カバレッジの確認
`htmlcov/`ディレクトリにカバレッジの結果が出力されます。



### テストの考え方
#### 確認すること
* get系のメソッドはワンパスが通ること
* `put_instruction`など、簡単に実行できるのでput,post,delete系のメソッドは、簡単に実行できるのであればワンパスが通ること

#### 確認しないこと
* 「組織の削除」、「プロジェクトの削除」など間違って操作してしまったときの影響が多いメソッド
* 「パスワード変更」など使用頻度が少なく、実行や確認がしづらいメソッド


# Versioning
annofabapiのバージョンはSemantic Versioning 2.0に従います。
* メソッドが追加されたときは、マイナーバージョンを上げる。
* annofabapiのバグ/ドキュメント修正などにより、annofabapiをリリースするときは、パッチバージョンを上げる。

annofabapiのバージョンは以下のファイルで定義しています。
* `annofabapi/__version__.py`
* `pyproject.toml`


# PyPIへのリリース方法

## 事前作業

### PyPIのアカウントを作成
1. 以下のURLにアクセスして、PyPIのアカウントを作成する。
https://pypi.org/account/register/

2. 管理者に連絡して、Collaboratorsとして招待してもらう
https://pypi.org/project/annofabapi/

## リリース方法
以下のコマンドを実行してください。PyPIのユーザ名とパスワードの入力が求められます。

```
$ make publish
```


## Document
### ドキュメントの作成
`$ make docs` コマンドを実行すると、`docs/_build/html/`にHTMLファイルが生成されます。


### ドキュメントの修正
`docs/*.rst`ファイルを修正してください。rstファイルは[Sphinx](https://www.sphinx-doc.org/en/master/)でビルドしています。


### ドキュメントのホスティング
ドキュメントは、https://readthedocs.org/ にホスティングしています。
masterブランチにプッシュすると、[ReadTheDocsのドキュメント](https://annofab-api-python-client.readthedocs.io/)が自動的に更新されます。

ReadTheDocsに通知するタイミングは、[GitHubのwebhook設定画面](https://github.com/kurusugawa-computer/annofab-api-python-client/settings/hooks)で設定してください。
ドキュメント生成元のブランチは、[ReadTheDocsの管理画面](https://readthedocs.org/dashboard/annofab-api-python-client/advanced/)で設定してください。

ReadTheDocsのビルド結果は https://readthedocs.org/projects/annofab-api-python-client/builds/ で確認できます。
メンテナンスする場合は、事前に管理者からメンテナスとして招待してもらってください。



## 開発フロー
* masterブランチを元にしてブランチを作成して、プルリクを作成してください。masterブランチへの直接pushすることはGitHub上で禁止しています。
* リリース時のソースはGitHubのRelease機能、またはPyPIからダウンロードしてください。




-----------------
# AnnoFab WebAPIの更新により、リリースする
### 1.ソースコードの生成

annofabapiのいくつかのファイルは、[AnnoFab Web APIのOpenAPI Spec](https://annofab.com/docs/api/swagger.yaml)から自動生成しています。
以下のコマンドを実行すると、ソースコードが生成されます。詳細は[generate/README.md](generate/README.md)を参照してください。

```
# `generate/swagger/*.yaml`ファイルから、ソースコードを生成する
$ generate/generate.sh

# AnnoFab WebAPIのOpenAPI Spec を`generate/swagger/`にダウンロードしてから、ソースコードを生成する
$ generate/generate.sh --download

$ make format && make lint
```

### 2.テストの実施
「テストの実行方法」を参照

### 3.versionを上げる
「Versioning」を参照

### 4.プルリクを作ってマージする

### 5.PyPIへパッケージをアップロードする
「PyPIへのリリース方法」を参照

### 6.GitHubのリリースページに追加
GitHubのRelease機能を使って、リリース情報を記載します。







