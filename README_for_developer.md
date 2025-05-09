# Usage for Developer
開発者用のドキュメントです。
ソースコードの生成、テスト実行、リリース手順などを記載します。

# Requirements
VSCodeのdevcontainerを起動してください。

# Generate source code

annofabapiのいくつかのファイルは、[Annofab Web APIのOpenAPI Spec](https://annofab.com/docs/api/swagger.yaml)から自動生成しています。
以下のコマンドを実行すると、ソースコードが生成されます。

```
# `generate/swagger/*.yaml`ファイルから、ソースコードを生成する
$ generate/generate.sh

# Annofab WebAPIのOpenAPI Spec を`generate/swagger/`にダウンロードしてから、ソースコードを生成する
$ generate/generate.sh --download

$ make format && make lint
```

# Test

## テストの実行方法
1. Annofabの認証情報を、`.netrc`ファイルまたは環境変数に設定する。
2. 以下のコマンドを実行して、テスト用のプロジェクトとタスクを作成する。
     * `uv run python tests/create_test_project.py --organization ${MY_ORGANIZATION}`
3. `pytest.ini`に、テスト対象の`project_id`と`task_id`を指定する。
    * `task_id`はプロジェクト`project_id`配下であること
    * **【注意】テストを実行すると、Annofabプロジェクトの内容が変更される**
4. `$ make test`コマンドを実行する。


#### テストメソッドを指定してテストする方法

```
$ uv run pytest tests/test_api.py::TestLogin::test_login
```

annofabapiでは、pytestのカスタムオプションを定義しています。

```
# ジョブを投げるテスト（時間がかかるテスト）を実行する。
$ uv run pytest --run_submitting_job tests 

# annofabapiモジュールのログを表示する。
$ uv run pytest --print_log_annofabapi tests 
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

# Release
GitHubのReleasesからリリースしてください。
バージョンはSemantic Versioningに従います。
リリースすると、以下の状態になります。

* ソース内のバージョン情報（`pyproject.toml`, `__init__.py`）は、uv-dynamic-versioning によりGitHubのバージョンタグから生成されます。
* 自動でPyPIに公開されます。




# 開発フロー
* mainブランチを元にしてブランチを作成して、プルリクを作成してください。mainブランチへの直接pushすることはGitHub上で禁止しています。


# Document
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
メンテナンスする場合は、事前に管理者から招待してもらってください。








