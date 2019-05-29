# 概要
annofabapiモジュールを使ったサンプルコードです。
pythonコマンドを使ってCLIとして利用できます。

# Requirements
* Python 3.6+
* 最新のannofabapiモジュール

# 使い方

## AnnoFabの認証情報の設定
`.netrc`ファイルにAnnoFabの認証情報を記載してください。
詳しくは[../README.md](../README.md)を参照してください。

## Pipenvを使う場合

```
$ git clone https://github.com/kurusugawa-computer/annofab-api-python-client.git
$ cd annofab-api-python-client/examples
$ pipenv install
$ pipenv shell

# サンプルコートを実行
$ python -m annofabcli.diff_annotation_specs prj1 prj2
```

## Pipenvを使わない場合

```
$ pip install annofabapi --upgrade
$ git clone https://github.com/kurusugawa-computer/annofab-api-python-client.git
$ cd annofab-api-python-client/examples
$ pip install . -U

# サンプルコートを実行
$ python -m annofabcli.diff_annotation_specs prj1 prj2
```

## Helpの見方

```
$ python invite_user_to_projects.py -h
```


# examplesツール

以下のpythonコマンドは、`$ pipenv shell`でPythonの仮想環境を有効にした状態で、実行してください。

## invite_user_to_projects
複数のプロジェクトに、ユーザを招待します。
このツールは、新しく組織にユーザを追加するときなどに、利用できます。

各プロジェクトのオーナ権限を持つユーザで実行してください。
※オーナ権限を持たないプロジェクトの場合はスキップします

```
# ORG組織配下のすべてのプロジェクトに、user1をownerロールで割り当てる
$ python -m annofabcli.invite_user_to_projects --user_id user1 --role owner --organization ORG

# prj1, prj2のプロジェクトに、user1をownerロールで割り当てる
$ python -m annofabcli.invite_user_to_projects --user_id user1 --role owner --project_id prj1 prj2
```

## cancel_acceptance
受け入れ完了タスクを、受け入れ取り消しにします。
アノテーション仕様を途中で変更したときなどに、利用します。

対象のタスクは、以下のようなtask_idの一覧が記載されたファイルで指定します。

```
task_id1
task_id2
task_id3
...
```


プロジェクトのオーナ権限を持つユーザで実行してください。

```
# prj1プロジェクトのタスクを、受け入れ取り消しにする。再度受け入れを担当させるユーザは未担当
$ python -m annofabcli.cancel_acceptance --project_id prj1 --task_id_file file

# prj1プロジェクトのタスクを、受け入れ取り消しにする。再度受け入れを担当させるユーザはuser1
$ python -m annofabcli.cancel_acceptance --project_id prj1 --task_id_file file --user_id user1
```

## reject_tasks_with_adding_comment
検査コメントを付与して、タスクを差し戻します。検査コメントは、タスク内の先頭の画像の左上に付与します。

このツールは、アノテーション仕様を途中で変更したときなどに、利用できます。

プロジェクトのチェッカー以上の権限を持つユーザで実行してください。

```
# prj1プロジェクトのタスクを、差し戻す。差し戻したタスクの担当者は割り当てられていない
$ python -m annofabcli.reject_tasks_with_adding_comment --project_id prj1 --task_id_file file \
 --comment "auto comment at tool"

# 差し戻したタスクに、最後のannotation phaseを担当したユーザに割り当てる（画面と同じ動き）
$ python -m annofabcli.reject_tasks_with_adding_comment --project_id prj1 --task_id_file file \
 --comment "auto comment at tool" \
 --assign_last_annotator

# 差し戻したタスクには、usr1を割り当てる
$ python -m annofabcli.reject_tasks_with_adding_comment --project_id prj1 --task_id_file file \
 --comment "auto comment at tool" \
 ----assigned_annotator_user_id usr1

```

## write_semantic_segmentation_images
アノテーションzipを展開したディレクトリから、アノテーションをSemantic Segmentation(Multi Class)用の画像をします。
矩形、ポリゴン、塗りつぶし、塗りつぶしv2が対象です。
複数のアノテーションディレクトリを指定して、画像をマージすることも可能です。


```
$ python  -m annofabcli.write_semantic_segmentation_images  --annotation_dir /tmp/af-annotation-xxxx \
 --default_input_data_size 1280x720 \
 --label_color_json_file /tmp/label_color.json \
 --output_dir /tmp/output \
 --task_status_comlete
```



## diff_annotation_specs
プロジェクト間のアノテーション仕様の差分を表示します。ただし、label_idなどAnnoFab内で生成されるIDは比較しません。
このツールは、同じアノテーションルールのプロジェクトが複数ある場合、アノテーション仕様が同一であることを確認するときなどに、利用できます。

プロジェクトのチェッカー以上の権限を持つユーザで実行してください。


```
$ python -m annofabcli.diff_annotation_specs prj1 prj2
```

## diff_project_members
プロジェクト間のプロジェクトメンバの差分を表示します。


```
$ python -m annofabcli.diff_project_members prj1 prj2
```

