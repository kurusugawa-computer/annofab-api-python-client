# 概要
annofabapiを使ったCLI(Command Line Interface)ツールです。
「タスクの一括差し戻し」や、「プロジェクト間の差分表示」など、AnnoFabの画面で実施するには時間がかかる操作を、コマンドとして提供しています。

# 注意
* 作者または著作権者は、ソフトウェアに関してなんら責任を負いません。
* 予告なく互換性のない変更がある可能性をご了承ください。
* AnnoFabプロジェクトに大きな変更を及ぼすツールも存在します。間違えて実行してしまわないよう、注意してください。


# Requirements
* Python 3.6+

# Install

```
$ git clone https://github.com/kurusugawa-computer/annofab-api-python-client.git
$ cd annofab-api-python-client/examples
$ pip install . -U
```


# 機能一覧

| サブコマンド                  | 内容                                                                                                     |
|-------------------------------|----------------------------------------------------------------------------------------------------------|
| cancel_acceptance             | 受け入れ完了タスクを、受け入れ取り消しする。                                                             |
| complete_tasks                | 未処置の検査コメントを適切な状態に変更して、タスクを受け入れ完了にする。                                 |
| diff_projects                 | プロジェクト間の差分を表示する                                                                           |
| invite_users                  | 複数のプロジェクトに、ユーザを招待する。                                                                 |
| print_unprocessed_inspections | 未処置の検査コメントList(task_id, input_data_idごと)をJSONとして出力する。                               |
| print_label_color             | アノテーション仕様から、label_nameとRGBを対応付けたJSONを出力する。                                      |
| reject_tasks                  | 検査コメントを付与してタスクを差し戻す。                                                                 |
| write_annotation_image        | アノテーションzipを展開したディレクトリから、アノテーションの画像（Semantic Segmentation用）を生成する。 |


# Usage

## AnnoFabの認証情報の設定
`.netrc`ファイルにAnnoFabの認証情報を記載してください。
詳しくは[annofab-api-python-client/README.md](https://github.com/kurusugawa-computer/annofab-api-python-client#netrc%E3%81%AB%E8%A8%98%E8%BC%89%E3%81%95%E3%82%8C%E3%81%9Fuser_id-password%E3%81%8B%E3%82%89%E7%94%9F%E6%88%90)を参照してください。




## 共通のオプション引数

### `-h` or `--help`
コマンドのヘルプを出力します。

```
# annofabcli全体のヘルプ
$ annofabcli -h

# diff_projectsサブコマンドのヘルプ
$ annofabcli diff_projects -h
```

### `--logdir`
ログファイルを保存するディレクトリを指定します。指定しない場合、`.log`ディレクトリにログファイルを出力します。

### `--logging_yaml`
ロギグングの設定ファイル(YAML)を指定します。指定した場合、`--logdir`オプションは無視されます。指定しない場合、デフォルトのロギング設定ファイルが読み込まれます。
設定ファイルの書き方は https://docs.python.org/ja/3/howto/logging.html を参照してください。

```yaml:logging-sample.yaml
# WARNINGレベル以上のログをコンソールに出力する

version: 1
handlers:
  consoleHandler:
    class: logging.StreamHandler
root:
  level: WARNING
  handlers: [consoleHandler]

# デフォルトのロガーを無効化しないようにする https://docs.djangoproject.com/ja/2.1/topics/logging/#configuring-logging
disable_existing_loggers: False
```


### `--task_id_file`
`task_id`の一覧が記載されたファイルです。`task_id`は改行（CR/LF）で区切られています。
`--task_id_file`を指定できないサブコマンドもあります。

```plain:task.txt
task_id_1
task_id_2
...
```


## サブコマンドの使い方

### cancel_acceptance
受け入れ完了タスクを、受け入れ取り消しにします。
アノテーションルールを途中で変更したときなどに、利用します。


```
# prj1プロジェクトのタスクを、受け入れ取り消しにする。再度受け入れを担当させるユーザは未担当
$ annofabcli cancel_acceptance --project_id prj1 --task_id_file task.txt

# prj1プロジェクトのタスクを、受け入れ取り消しにする。再度受け入れを担当させるユーザはuser1
$ annofabcli cancel_acceptance --project_id prj1 --task_id_file task.txt --user_id user1
```

* オーナ権限を持つユーザで実行してください。


### complete_tasks
未処置の検査コメントを適切な状態に変更して、タスクを受け入れ完了にします。
特定のタスクのみ受け入れをスキップしたいときに、利用します。

```
# 未処置の検査コメントは"対応完了"状態にして、prj1プロジェクトのタスクを受け入れ完了にする。
$ annofabcli complete_tasks --project_id prj1 --task_id_file task.txt　 --inspection_json inspection.json --inspection_status error_corrected

# 未処置の検査コメントは"対応不要"状態にして、prj1プロジェクトのタスクを受け入れ完了にする。
$ annofabcli complete_tasks --project_id prj1 --task_id_file task.txt　 --inspection_json inspection.json --inspection_status no_correction_required
```

* オーナ権限を持つユーザで実行してください。
* inspection.jsonは、未処置の検査コメントです。ファイルのフォーマットは、[print_unprocessed_inspections](#print_unprocessed_inspections)の出力結果と同じです。


### diff_projects
プロジェクト間の差分を表示します。
同じアノテーションルールのプロジェクトが複数ある場合、各種情報が同一であることを確認するときに、利用します。


```
# すべての差分
$ annofabcli diff_projects  prj1 prj2

# アノテーション仕様のラベル情報の差分
$ annofabcli diff_projects prj1 prj2 --target annotation_labels

# 定型指摘の差分
$ annofabcli diff_projects prj1 prj2 --target inspection_phrases

# プロジェクトメンバの差分
$ annofabcli diff_projects  prj1 prj2 --target members

# プロジェクト設定の差分
$ annofabcli diff_projects  prj1 prj2 --target settings

```


### invite_users
複数のプロジェクトに、ユーザを招待します。

```
# ORG組織配下のすべてのプロジェクトに、user1, user2をownerロールで招待する
$ annofabcli invite_users --user_id user1 user2 --role owner --organization ORG

# prj1, prj2のプロジェクトに、user1をaccepterロールで招待する
$ annofabcli invite_users --user_id user1 --role accepter --project_id prj1 prj2
```

* オーナ権限を持つユーザで実行してください。


### print_unprocessed_inspections
未処置の検査コメントList(task_id, input_data_idごと)をJSONとして出力します。出力結果は[complete_tasks](#complete_tasks)に利用します。

```
# 未処置の検査コメント一覧を出力する
$ annofabcli print_unprocessed_inspections --project_id prj1 --task_id_file task.txt

# 未処置で、user1が"hoge"とコメントした検査コメント一覧を出力する
$ annofabcli print_unprocessed_inspections --project_id prj1 --task_id_file task.txt --inspection_comment "hoge" --commenter_user_id user1
```

```json:出力結果
{
  "task_id_1": {
    "input_data_id_1": [
      {
        "inspection_id": "inspection_id_1",
        ...
      }
    ],
    ...
  },
  ...
}
```





### print_label_color
アノテーション仕様から、label_name(english)とRGBを対応付けたJSONを出力します。出力結果は[write_annotation_image](#write_annotation_image)に利用します。

```
# 未処置の検査コメント一覧を出力する
$ annofabcli print_label_color --project_id prj1 --task_id_file task.txt

# 未処置で、user1が"hoge"とコメントした検査コメント一覧を出力する
$ annofabcli print_unprocessed_inspections --project_id prj1 --task_id_file task.txt --inspection_comment "hoge" --commenter_user_id user1
```

```json:出力結果
{
  "cat": [
    255,
    99,
    71
  ],
  "dog": [
    255,
    0,
    255
  ],
```



### reject_tasks
検査コメントを付与して、タスクを差し戻します。検査コメントは、タスク内の先頭の画像の左上に付与します。
アノテーションルールを途中で変更したときなどに、利用します。


```
# prj1プロジェクトに、"hoge"という検査コメントを付与して、タスクを差し戻す。差し戻したタスクに担当者を割り当てない。
$ annofabcli reject_tasks --project_id prj1 --task_id_file tasks.txt --comment "hoge"

# 差し戻したタスクに、最後のannotation phaseを担当したユーザを割り当てる（画面と同じ動き）
$ annofabcli reject_tasks --project_id prj1 --task_id_file tasks.txt --comment "hoge" --assign_last_annotator

# 差し戻したタスクに、ユーザuser1を割り当てる
$ annofabcli reject_tasks --project_id prj1 --task_id_file tasks.txt --comment "hoge" --assigned_annotator_user_id user1
```

* オーナ権限を持つユーザで実行してください。



### write_annotation_image
アノテーションzipを展開したディレクトリから、アノテーションの画像（Semantic Segmentation用）を生成します。
アノテーション種類が矩形、ポリゴン、塗りつぶし、塗りつぶしv2のアノテーションが生成対象です。
複数のアノテーションディレクトリを指定して、画像をマージすることも可能です。ただし、各プロジェクトでtask_id, input_data_idが一致している必要があります。


```
# af-annotation-xxxx ディレクトリからアノテーションの画像を生成する。タスクのstatusがcompleteのみ画像を生成する。
$ annofabcli write_annotation_image  --annotation_dir af-annotation-xxxx \
 --input_data_size 1280x720 \
 --label_color_file label_color.json \
 --output_dir output \
 --task_status_complete
 --image_extension png 
 
 
# af-annotation-xxxx ディレクトリに、af-annotation-1、af-annotation-2ディレクトリをマージしたアノテーションの画像を生成する。
# af-annotation-xxxxに存在するすべてのタスクに対して、画像を生成する。
$ python  -m annofabcli.write_semantic_segmentation_images write  --annotation_dir af-annotation-xxxx \
 --input_data_size 1280x720 \
 --label_color_file label_color.json \
 --output_dir output \
 --sub_annotation_dir af-annotation-1 af-annotation-2
```

* `label_color.json`は、`label_name`とRGBを対応付けたJSONファイルです。ファイルのフォーマットは、[print_label_color](#print_label_color)の出力結果と同じです。

