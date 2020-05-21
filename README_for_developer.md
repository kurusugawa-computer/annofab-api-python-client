# Usage for Developer
開発者用のドキュメントです。
ソースコードの生成、テスト実行、リリース手順などを記載します。

## Requirements
* Bash
* Docker (OpenAPI Generatorを実行するのに必要)
* python 3.6+
    * poetry

## Install
以下のコマンドを実行してください。開発に必要な環境が構築されます。

```bash
$ make init
```

## Source

### ソースコードの生成
annofabapiのいくつかのファイルは、[AnnoFab Web APIのOpenAPI Spec](https://annofab.com/docs/api/swagger.yaml)から自動生成しています。
以下のコマンドを実行すると、ソースコードが生成されます。詳細は[generate/README.md](generate/README.md)を参照してください。

```
# `generate/swagger/*.yaml`ファイルから、ソースコードを生成する
$ generate/generate.sh

# AnnoFab WebAPIのOpenAPI Spec を`generate/swagger/`にダウンロードしてから、ソースコードを生成する
$ generate/generate.sh --download

```

### フォーマットを実行
以下のコマンドを実行してください。

```
$ make format
```

### lintを実行
以下のコマンドを実行してください。

```
$ make lint
```

## Test

### テストの実行
1. AnnoFabの認証情報を`.netrc`に記載する。
2. `pytest.ini`にテスト対象の`project_id`を指定する。**【注意】テストを実行すると、AnnoFabプロジェクトの内容が変更される**
3. `$ make test`コマンドを実行する。

#### 直接pytestを実行する場合

```
$ poetry run pytest tests
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



## Release

## リリース方法

### 1. annofabapiのバージョンを上げる
`annofabapi/__version__.py`に記載されているバージョンを上げてください。バージョンはSemantic Versioning 2.0に従います。

* AnnoFabののバージョンアップにより、annofabapiをリリースするときは、マイナーバージョンを上げる。
* annofabapiのバグ/ドキュメント修正などにより、annofabapiをリリースするときは、パッチバージョンを上げる。


### 2. PyPIに登録する
1. TestPyPIに登録して、内容を確認する。

```
$ make publish_test
```

2. TestPyPIからインストールして、利用できることを確認する。

```
$ pip uninstall annofabapi
$ pip install --index-url https://test.pypi.org/simple/ annofabapi --upgrade
$ python -c "import annofabapi; print(annofabapi.__version__)"
```

3. PyPIに登録する。

```
$ make publish
```

4. PyPIからインストールして、利用できることを確認する。

```
$ pip uninstall annofabapi
$ pip install annofabapi --upgrade
$ python -c "import annofabapi; print(annofabapi.__version__)"
```



### 3. GitHubのリリースページに追加
GitHubのRelease機能を使って、リリース情報を記載します。


## Document
### ドキュメントの作成
masterブランチが更新されると、自動的に[ReadTheDocsのサイト](https://annofab-api-python-client.readthedocs.io/)が更新されます。
ReadTheDocsのビルド結果は https://readthedocs.org/projects/annofab-api-python-client/builds/ で確認できます。

ローカルでドキュメントを確認したい場合は、`$ make docs` コマンドを実行してください。`docs/_build/html/`にHTMLファイルが生成されます。


### ドキュメントの修正
`docs/*.rst`ファイルを修正してください。rstファイルは[Sphinx](https://www.sphinx-doc.org/en/master/)でビルドしています。



## 開発フロー
* masterブランチを元にしてブランチを作成して、プルリクを作成してください。masterブランチへの直接pushすることはGitHub上で禁止しています。
* リリース時のソースはGitHubのRelease機能、またはPyPIからダウンロードしてください。
