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
詳細は[generate/README.md](generate/README_for_generate.md)を参照してください。

## テスト実行方法
TODO

### 準備
1. pytest.iniにテスト対象のproject_idを指定. **プロジェクトが変更される恐れがあることに注意！！**
2. 以下の環境変数にAnnofabの認証情報を設定
    * `ANNOFAB_USER_ID`
    * `ANNOFAB_PASSWORD`
3. `pipenv run tox` でテスト実行

### 備考
* 基本的に、テストメソッドは、エラーが発生しないこと（HTTP STatus codeが400系でないこと）を確認しています。それより詳細な確認は行っていません。

    

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


2. PyPIに登録する。

```
$ make publish
```

### GitHubのリリースページ
GitHubのRelease機能を使って、リリース情報を記載する。


### ドキュメントを作成する
TODO


## 開発フロー
* 開発途中のcommitをmasterブランチにpushします。
* リリース時のソースはGitHubのRelease機能からダウンロードしてください。
