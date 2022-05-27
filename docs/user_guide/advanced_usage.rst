==================================================
Advanced Usage
==================================================

``service.wrapper``
==================================================
``service.wrapper`` には、``server.api`` を組み合わせたメソッドが定義されています。

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


Annofabにファイルをアップロードするメソッド
---------------------------------------------
Annofabにファイルをアップロードしてから、入力データや補助情報などを登録するメソッドです。

* ``put_input_data_from_file``
* ``put_supplementary_data_from_file``

.. code-block:: python

    # "sample.png"をAnnofabにアップロードして、入力データ"input1"を作成する。
    service.wrapper.put_input_data_from_file(project_id, input_data_id="input1",
        file_path="sample.png")

    # 入力データ"input1"に、"sample.png"を補助情報として登録する
    service.wrapper.put_supplementary_data_from_file(project_id, input_data_id="input1",
    supplementary_data_id="supplementary1", file_path="sample.png", request_body={"supplementary_data_number":1})

AnnofabのS3にアップロードのみ実施する場合は、``upload_file_to_s3`` メソッドを利用してください。

.. code-block:: python

    # "sample.png"をAnnofabにアップロードして、入力データ"input1"を作成する。
    s3_path = service.wrapper.upload_file_to_s3(project_id, file_path="sample.png")
    print(s3_path)
    # 's3://annotationfactory.production.temporary/xxxxxx'



``annofabapi.parser``
==================================================
``annofabapi.parser`` には、アノテーションzipを読み込むためのメソッドやクラスが定義されています。


アノテーションzip内の1個のJSONを読み込む
--------------------------------------------------
``SimpleAnnotationParser.parse()`` を実行すると、JSONファイルを読み込みます。
JSONファイルの中身については、https://annofab.com/docs/api/#tag/x-annotation-zip を参照してください。

.. code-block:: python

    import zipfile
    from annofabapi.parser import SimpleAnnotationZipParser

    # Simpleアノテーションzip内の"task_1/12345678-abcd-1234-abcd-1234abcd5678.json" を読み込む
    with zipfile.ZipFile("simple-annotation.zip", "r") as zip_file:
        parser = SimpleAnnotationZipParser(zip_file, "task_1/12345678-abcd-1234-abcd-1234abcd5678.json")

        print(parser.task_id)
        # 'task_1'

        print(parser.input_data_id)
        # '12345678-abcd-1234-abcd-1234abcd5678'

        print(parser.parser.json_file_path)
        # 'task_1/12345678-abcd-1234-abcd-1234abcd5678.json'

        # JSONファイルを読み込む
        simple_annotation = parser.parse()
        print(simple_annotation)
        # SimpleAnnotation(annotation_format_version='1.2.0', project_id='test_project_id', task_id='task_1', task_phase=<TaskPhase.ACCEPTANCE: 'acceptance'>, ...




``SimpleAnnotationDetail`` クラスのdataプロパティをdictからデータクラスに変換する
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
``SimpleAnnotationParser.parse`` 関数に、``SimpleAnnotationDetail`` クラスの ``data``  プロパティをdictからデータクラスに変換する関数を渡すことができます。
        

.. code-block:: python

    from annofabapi.dataclass.annotation import FullAnnotationDataBoundingBox

    def convert_deitail_data(self, dict_data):
        if dict_data["_type"] == "BoundingBox":
            dict_data["type"] = dict_data["_type"]
            return FullAnnotationDataBoundingBox.from_dict(dict_data)
        else:
            return dict_data

            
    # Simpleアノテーションzip内の"task_1/12345678-abcd-1234-abcd-1234abcd5678.json" を読み込む
    with zipfile.ZipFile("simple-annotation.zip", "r") as zip_file:
        parser = SimpleAnnotationZipParser(zip_file, "task_1/12345678-abcd-1234-abcd-1234abcd5678.json")

        simple_annotation = parser.parse()
        print(type(simple_annotation.details[0].data)
        # dict

        simple_annotation = parser.parse()
        print(type(simple_annotation.details[0].data)
        # => dict

        simple_annotation2 = parser.parse()
        print(type(simple_annotation2.details[0].data)
        # => FullAnnotationDataBoundingBox




塗りつぶし画像を読み込む
--------------------------------------------------
``SimpleAnnotationParser.open_outer_file()`` メソッドを実行すると、塗りつぶし画像を読み込みます。

.. code-block:: python

    simple_annotation = parser.parse()
    # 塗りつぶし画像が含まれているアノテーション情報
    detail = simple_annotation.details[0]
    # 塗りつぶし画像の相対パス
    data_uri = detail.data["data_uri"]

    # 塗りつぶし画像を読み込む
    with parser.open_outer_file(data_uri) as f:
        pass



アノテーションzip内のすべてのJSONを読み込む
--------------------------------------------------

``annofabapi.parser.lazy_parse_simple_annotation_zip`` メソッドを利用すると、アノテーションzip内のすべてのJSONを読み込むことができます。


.. code-block:: python

    import zipfile
    from pathlib import Path
    from annofabapi.parser import lazy_parse_simple_annotation_zip

    # Simpleアノテーションzipの読み込み
    iter_parser = lazy_parse_simple_annotation_zip(Path("simple-annotation.zip"))
    for parser in iter_parser:
        simple_annotation = parser.parse()



アノテーションzip内のすべてのJSONをタスク単位で読み込む
----------------------------------------------------------------------------------------------------
``annofabapi.parser.lazy_parse_simple_annotation_zip_by_task`` メソッドを利用すると、アノテーションzip内のすべてのJSONを、タスク単位で読み込むことができます。

.. code-block:: python

    import zipfile
    from pathlib import Path
    from annofabapi.parser import lazy_parse_simple_annotation_zip_by_task

    task_iter_parser = lazy_parse_simple_annotation_zip_by_task(Path("simple-annotation.zip"))
    for task_parser in task_iter_parser:
        print(task_parser.task_id)
        for parser in task_parser.lazy_parse():
            simple_annotation = parser.parse()
            print(simple_annotation)


アノテーションzipを展開したディレクトリを読み込む
--------------------------------------------------
アノテーションzipだけでなく、アノテーションzipを展開したディレクトリも読み込むことが可能です。


.. code-block:: python

    from annofabapi.parser import lazy_parse_simple_annotation_dir

    # Simpleアノテーションzipを展開したディレクトリの読み込み
    iter_parser = lazy_parse_simple_annotation_dir(Path("simple-annotation-dir"))
    for parser in iter_parser:
        simple_annotation = parser.parse()
        print(simple_annotation)


以下の表に、アノテーションzipとそれを展開したディレクトリ、それぞれに対応したメソッド/クラス名を記載します。



+------------------------------------------------------+------------------------------------------+------------------------------------------+
| 内容                                                 | アノテーションzip                        | アノテーションzipを展開したディレクトリ  |
+======================================================+==========================================+==========================================+
| すべてのデータを入力データ単位（JSON単位）で読み込む | lazy_parse_simple_annotation_zip         | lazy_parse_simple_annotation_dir         |
+------------------------------------------------------+------------------------------------------+------------------------------------------+
| すべてのデータをタスク単位で読み込む                 | lazy_parse_simple_annotation_zip_by_task | lazy_parse_simple_annotation_dir_by_task |
+------------------------------------------------------+------------------------------------------+------------------------------------------+
| 1個のJSONを読み込む                                  | SimpleAnnotationZipParser                | SimpleAnnotationDirParser                |
+------------------------------------------------------+------------------------------------------+------------------------------------------+


``annofabapi.dataclass``
=============================================


``annofabapi.dataclass`` には、タスクや入力データなどよく利用するオブジェクトのデータクラスが定義されています。


.. code-block:: python

    from annofabapi.dataclass.task import Task
    dict_task, _ = service.api.get_task(project_id, "test_task_id")
    task = Task.from_dict(dict_task)

    print(type(task))
    # <class 'annofabapi.dataclass.task.Task'>
    print(task.task_id)
    # 'test_task_id'
    print(task.status)
    # <TaskStatus.NOT_STARTED: 'not_started'>


``annofabapi.models``
=============================================
``annofabapi.models`` には、タスクのステータスなどの列挙体が定義されています。

.. code-block:: python

    from annofabapi.models import TaskStatus
    dict_task, _ = service.api.get_task(project_id, "test_task_id")
    
    if dict_task["status"] == TaskStatus.COMPLETE.value:
        print("タスクは完了状態")
    else:
        print("タスクは未完了状態")


