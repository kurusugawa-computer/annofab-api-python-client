==================================================
アノテーションzipの読み込み方法
==================================================


レベル２
========


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
--------------------------------------------------
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


アノテーションzipを展開したディレクトリに対して読み込む
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

