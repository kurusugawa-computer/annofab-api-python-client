# Usage for Developer

## Requirements
* Linux
* Docker
* python 3.6+
* pipenv

## Install

```bash
$ make init
```


## `annofabapi/api.py`の生成方法
`annofabapi/api.py`は[AnnoFab Web APIのOpenAPI specification](https://annofab.com/docs/api/swagger.yaml)から自動生成しています。
詳細は[generate/README.md](generate/README.md)を参照してください。

## テスト実行方法
1. AnnoFabの認証情報を`.netrc`に記載する。
2. `pytest.ini`にテスト対象の`project_id`を指定. テスト実行により、プロジェクトが変更されることに注意！！
3. `$ make test`コマンドを実行する。

### テストの考え方
#### 確認すること
* get系のメソッドはワンパスが通ること
* 「タスクの作成」など、よく使うメソッドで、簡単に実行や確認ができるメソッドのワンパスが通ること

#### 確認しないこと
* 「組織の削除」、「プロジェクトの削除」など間違って操作してしまったときの影響が多いメソッド
* 「パスワード変更」など使用頻度が少なく、実行や確認がしづらいメソッド


## フォーマッターを実行

```
$ make format
```

## lintを実行

```
$ make lint
```

## リリースする

### `setup.py`のバージョンを上げる
* AnnoFabのリリースによってクライアントライブラリをリリースするときは、マイナーバージョンを上げる。
* クライアントライブラリのバグ/ドキュメント修正などをリリースするときは、パッチバージョンを上げる。


### PyPIに登録する
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



### GitHubのリリースページ
GitHubのRelease機能を使って、リリース情報を記載する。


### ドキュメントを作成する
TODO


## 開発フロー
* 開発途中のcommitをmasterブランチにpushします。
* リリース時のソースはGitHubのRelease機能からダウンロードしてください。
