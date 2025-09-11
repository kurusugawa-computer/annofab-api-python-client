# copilot-instructions.md

## プロジェクトの目的
AnnofabのWebAPIのPythonクライアントライブラリです。

## 開発でよく使うコマンド
* コードのフォーマット: `make format`
* Lintの実行: `make lint`
* テストの実行: `make test`
* ドキュメントの実行: `make docs`

## 技術スタック
* Python 3.9 以上
* テストフレームワーク: Pytest v8 以上

## ディレクトリ構造概要

* `annofabcli/**`: アプリケーションのソースコード
* `tests/**`: テストコード
    * `tests/data/**`: テストコードが参照するリソース
* `docs/*`: ドキュメント

## コーディングスタイル

### Python
* dictから値を取得する際、必須なキーならばブラケット記法を使う。キーが必須がどうか分からない場合は、必須とみなす。
* できるだけ`os.path`でなく`pathlib.Path`を使う（Lint`flake8-use-pathlib`に従う）
* Noneの判定、空文字列の判定、長さが0のコレクションの判定は、falsyとして判定するのでなく、`if a is not None:`のように判定内容を明記してください。
* 型ヒントを`dict`にする場合、`dict[str, Any]`のようにキーと値の型を指定する。

### テストコード
* Errorの確認は、`pytest.raises`を使用する。エラーメッセージの確認は行わない。
* 一時ディレクトリを使用する場合は、`tmp_path` fixtureを利用する。


## 作業の進め方
* コードの修正が完了したら`make format`を実行してフォーマットを行い、その後`make lint`を実行してLintエラーがないことを確認する。

## レビュー
* PRレビューの際は、日本語でレビューを行う
