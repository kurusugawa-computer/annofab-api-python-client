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
$ cd annofab-api-python-client 

$ pipenv install
$ pipenv shell
$ cd examples

# サンプルコートを実行
$ python invite_user_to_projects.py --user_id user --role owner --organization ORG
```

## Pipenvを使わない場合

```
$ pip install annofabapi --upgrade

$ git clone https://github.com/kurusugawa-computer/annofab-api-python-client.git
$ cd annofab-api-python-client/examples

# サンプルコートを実行
$ python invite_user_to_projects.py --user_id user --role owner --organization ORG
```

## Helpの見方

```
$ python invite_user_to_projects.py -h
```


# examplesツール

## invite_user_to_projects.py
複数のプロジェクトに、ユーザを招待します。
このツールは、新しく組織にユーザを追加するときなどに、利用できます。

各プロジェクトのオーナ権限を持つユーザで実行してください。
※オーナ権限を持たないプロジェクトの場合はスキップします

```
# ORG組織配下のすべてのプロジェクトに、user1をownerロールで割り当てる
$ python invite_user_to_projects.py --user_id user1 --role owner --organization ORG

# prj1, prj2のプロジェクトに、user1をownerロールで割り当てる
$ python invite_user_to_projects.py --user_id user1 --role owner --project_id prj1 prj2
```

## cancel_acceptance.py
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
$ python cancel_acceptance.py --project_id prj1 --task_id_file file

# prj1プロジェクトのタスクを、受け入れ取り消しにする。再度受け入れを担当させるユーザはuser1
$ python cancel_acceptance.py --project_id prj1 --task_id_file file --user_id user1
```

## reject_tasks_with_adding_comment.py
検査コメントを付与して、タスクを差し戻します。検査コメントは、タスク内の先頭の画像の左上に付与します。

このツールは、アノテーション仕様を途中で変更したときなどに、利用できます。

プロジェクトのチェッカー以上の権限を持つユーザで実行してください。

```
# prj1プロジェクトのタスクを、差し戻す
$ python cancel_acceptance.py --project_id prj1 --task_id_file file --comment "auto comment at tool"
```

## write_semantic_segmentation_images.py

```
$ python write_semantic_segmentation_images.py  --annotation_dir /tmp/af-annotation-xxxx \
 --default_input_data_size 1280x720 \
 --label_color_json_file /tmp/label_color.json \
 --output_dir /tmp/output \
 --task_status_comlete
```
