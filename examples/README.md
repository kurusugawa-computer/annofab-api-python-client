# 概要
annofabapiモジュールを使ったサンプルコードです。
pythonコマンドを使ってCLIとして利用できます。

# Requirements
* Python 3.6+
* 最新のannofabapiモジュール

# Install

## Pipenvを使う場合

```
$ git clone https://github.com/kurusugawa-computer/annofab-api-python-client.git
$ cd annofab-api-python-client/examples
$ pipenv install
$ pipenv shell
```

`pipenv`は`$ pip install pipenv --upgrade`でインストールできる。


## Pipenvを使わずにpipを利用する場合

```
$ pip install annofabapi --upgrade
$ git clone https://github.com/kurusugawa-computer/annofab-api-python-client.git
$ cd annofab-api-python-client/examples
$ pip install . -U
```


# 使い方

## AnnoFabの認証情報の設定
`.netrc`ファイルにAnnoFabの認証情報を記載してください。
詳しくは[../README.md](../README.md)を参照してください。

## コマンドの実行方法

```
$ cd annofab-api-python-client/examples

# プロジェクト間の差分を表示
$ python -m annofabcli.diff_projects prj1 prj2
```


## Helpの見方

```
$ python invite_user_to_projects.py -h
```


# examplesツール

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
 --assigned_annotator_user_id usr1

```

## write_semantic_segmentation_images
アノテーションzipを展開したディレクトリから、アノテーションをSemantic Segmentation(Multi Class)用の画像をします。
矩形、ポリゴン、塗りつぶし、塗りつぶしv2が対象です。

複数のアノテーションディレクトリを指定して、画像をマージすることも可能です。ただし、各プロジェクトでtask_id, input_data_idが一致している必要があります。


```
# af-annotation-xxxx ディレクトリからSemantic Segmentation用の画像を生成. 生成対象はタスクのstatusがcompleteのみ。pngで生成。
$ python  -m annofabcli.write_semantic_segmentation_images write  --annotation_dir af-annotation-xxxx \
 --input_data_size 1280x720 \
 --label_color_file label_color.json \
 --output_dir output \
 --task_status_complete
 --image_extension png 
 
 
# label_nameと色を対応づけたjsonファイルを生成する。
$ python  -m annofabcli.write_semantic_segmentation_images create_label_color_file  --project_id prj1 label_color.json

 
 # af-annotation-xxxx ディレクトリに、af-annotation-1、af-annotation-2ディレクトリをマージした、Semantic Segmentation用の画像を生成する。
 # 生成対象は全タスク
$ python  -m annofabcli.write_semantic_segmentation_images write  --annotation_dir af-annotation-xxxx \
 --input_data_size 1280x720 \
 --label_color_file label_color.json \
 --output_dir output \
 --sub_annotation_dir af-annotation-1 af-annotation-2


```



## diff_projects
プロジェクト間の差分を表示します。
同じアノテーションルールのプロジェクトが複数ある場合、各種情報が同一であることを確認するときなどに、利用できます。


```

# アノテーション仕様のラベル情報の差分
$ python -m annofabcli.diff_projects prj1 prj2 --target annotation_labels

# 定型指摘の差分
$ python -m annofabcli.diff_projects prj1 prj2 --target inspection_phrases

# プロジェクトメンバの差分
$ python -m annofabcli.diff_projects prj1 prj2 --target members

# プロジェクト設定の差分
$ python -m annofabcli.diff_projects prj1 prj2 --target settings

# 上記項目すべての差分
$ python -m annofabcli.diff_projects prj1 prj2
```


## 非推奨ツール


### deprecated_complete_tasks
検査コメントを適切な状態（対応完了 or 対応不要）にして、タスクを受け入れ完了にします。

```
$ python -m annofabcli.deprecated_complete_tasks --project_id prj1 --task_id_file task_id_file.txt --inspection_status no_correction_required 

```