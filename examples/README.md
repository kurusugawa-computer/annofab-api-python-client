# 概要
annofabapiモジュールを使ったサンプルコードです。
pythonコマンドを使ってCLIとして利用できます。

# 使い方

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

```
# ORG組織配下のすべてのプロジェクトに、user1をownerロールで割り当てる
$ python invite_user_to_projects.py --user_id user1 --role owner --organization ORG

# prj1, prj2のプロジェクトに、user1をownerロールで割り当てる
$ python invite_user_to_projects.py --user_id user1 --role owner --project_id prj1 prj2
```

## cancel_acceptance.py
受け入れ完了タスクを、受け入れ取り消しにします。


```
# prj1プロジェクトのタスクを、受け入れ取り消しにする。再度受け入れを担当させるユーザは未担当
$ python cancel_acceptance.py --project_id prj1 --task_id_file file

# prj1プロジェクトのタスクを、受け入れ取り消しにする。再度受け入れを担当させるユーザはuser1
$ python cancel_acceptance.py --project_id prj1 --task_id_file file --user_id user1
```

