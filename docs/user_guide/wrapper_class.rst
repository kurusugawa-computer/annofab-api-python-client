==================================================
Wrapper
==================================================

WebAPIにリクエストを投げる方法（基本的）
--------------------------------------------------


service.wrapper.get_all_xxx メソッド
--------------------------------------------------
ページネーションを意識せずに、すべての情報を取得できます。

.. code-block:: python

    task_list = service.wrapper.get_all_tasks(project_id, query_params={"status":"complete"})

    print(type(task_list))
    # <class 'list'>

    pprint(task_list[0])
    # {'project_id': 'test_project_id',
    # 'task_id': 'test_task_id',
    # ...}


get_all_xxx メソッドの一覧です。

* ``get_all_annotation_list``
* ``get_all_input_data_list``
* ``get_all_my_organizations``
* ``get_all_organization_members``
* ``get_all_project_job``
* ``get_all_project_members``
* ``get_all_projects_of_organization``
* ``get_all_tasks``


service.wrapper.get_xxx_or_none メソッド
--------------------------------------------------
HTTPステータスコードが404のときは、``None`` を返します。


.. code-block:: python

    task = service.wrapper.get_task_or_none(project_id, "test_task_id")
    if task is not None:
        print("task exists.")
    else:
        print("task does not exist.")

    pprint(task)
    # {'project_id': 'test_project_id',
    # 'task_id': 'test_task_id',
    # ...}


get_xxx_or_none メソッドの一覧です。

* ``get_input_data_or_none``
* ``get_organization_or_none``
* ``get_organization_member_or_none``
* ``get_project_or_none``
* ``get_project_member_or_none``
* ``get_task_or_none``


service.wrapper.download_xxx メソッド
---------------------------------------------
アノテーションzipなどのファイルをダウンロードできるメソッドです。

* ``download_annotation_archive``
* ``download_full_annotation_archive``
* ``download_project_inputs_url``
* ``download_project_tasks_url``
* ``download_project_inspections_url``
* ``download_project_task_history_events_url``
* ``download_project_task_histories_url``


.. code-block:: python
    # アノテーションzipをダウンロードする
    service.wrapper.download_annotation_archive(project_id, "out/simple_annotation.zip")




service.api.operate_task を使いやすくしたメソッド
--------------------------------------------------
``service.api.operate_task`` メソッドをユースケースごと分割して、使いやすくしたメソッドです。

* ``change_task_status_to_working``
* ``change_task_status_to_break``
* ``change_task_status_to_on_hold``
* ``complete_task``
* ``cancel_submitted_task``
* ``cancel_completed_task``
* ``change_task_operator``
* ``reject_task``


.. code-block:: python
    # タスクのステータスを「作業中」に変更する
    task = service.wrapper.change_task_status_to_working(project_id, "test_task_id")


statistics系APIの中身を返すメソッド
---------------------------------------------
statistics系APIは、統計情報が格納されたJSONのファイルパスを返すだけで、統計情報は返しません。
以下のメソッドは、統計情報を返すメソッドになります。

* ``get_account_statistics``
* ``get_inspection_statistics``
* ``get_task_phase_statistics``
* ``get_label_statistics``
* ``get_inspection_statistics``
* ``get_worktime_statistics``


.. code-block:: python
    # タスクのステータスを「作業中」に変更する
    account_statistics = service.wrapper.get_account_statistics(project_id)


AnnoFabにファイルをアップロードするメソッド
---------------------------------------------
AnnoFabにファイルをアップロードしてから、入力データや補助情報などを登録するメソッドです。

* ``put_input_data_from_file``
* ``put_supplementary_data_from_file``

.. code-block:: python
    # "sample.png"をAnnoFabにアップロードして、入力データ"input1"を作成する。
    service.wrapper.put_input_data_from_file(project_id, input_data_id="input1",
        file_path="sample.png")

    # 入力データ"input1"に、"sample.png"を補助情報として登録する
    service.wrapper.put_supplementary_data_from_file(project_id, input_data_id="input1",
    supplementary_data_id="supplementary1", file_path="sample.png", request_body={"supplementary_data_number":1})

AnnoFabのS3にアップロードのみする場合は、``upload_file_to_s3`` メソッドを利用してください。

.. code-block:: python
    # "sample.png"をAnnoFabにアップロードして、入力データ"input1"を作成する。
    s3_path = service.wrapper.upload_file_to_s3(project_id, file_path="sample.png")
    print(s3_path)
    # 's3://annotationfactory.production.temporary/xxxxxx'



# 少し発展的なこと
* modelsの紹介(enum)
* dataclassの紹介
* annotation_zip, parser

# 開発者しか使わない
* v2 api
* endpoint

