annofabapi.util package
=======================

Submodules
----------

annofabapi.util.annotation\_specs module
----------------------------------------

.. automodule:: annofabapi.util.annotation_specs
   :members:
   :show-inheritance:
   :undoc-members:

annofabapi.util.attribute\_restrictions module
----------------------------------------------

.. automodule:: annofabapi.util.attribute_restrictions
   :members:
   :show-inheritance:
   :undoc-members:

annofabapi.util.page module
---------------------------

Annofabの画面URLの生成と解析に利用できます。

* ``parse_project_url``: プロジェクト配下の画面からプロジェクトIDを抽出します。
* ``parse_task_url``: 履歴やエディタを含むタスク配下の画面からプロジェクトIDとタスクIDを抽出します。
* ``parse_image_editor_url``: 画像エディタから入力データIDとアノテーションIDも抽出します。
* ``parse_video_editor_url``: 動画エディタからアノテーションIDと再生位置も抽出します。
* ``parse_3dpc_editor_url``: 3次元エディタのクエリとフラグメントから各IDを抽出します。
  カスタムのエディタには、生成時と同じ ``base_url`` を指定してください。

解析結果は属性名で参照できます。任意のIDが省略されている場合、その属性は ``None`` になります。
IDはパーセントデコードされます。対応しない形式には ``ValueError`` を送出します。
画面の存在やアクセス権は検証しません。

.. code-block:: python

    from annofabapi.util.page import parse_image_editor_url, parse_task_url

    url = "https://annofab.com/projects/p1/tasks/t1/editor?version=preview#i1/a1"
    task = parse_task_url(url)
    assert task.project_id == "p1"
    assert task.task_id == "t1"

    editor = parse_image_editor_url(url)
    assert editor.input_data_id == "i1"
    assert editor.annotation_id == "a1"

.. automodule:: annofabapi.util.page
   :members:
   :show-inheritance:
   :undoc-members:

annofabapi.util.task\_history module
------------------------------------

.. automodule:: annofabapi.util.task_history
   :members:
   :show-inheritance:
   :undoc-members:

annofabapi.util.tracking\_id module
-----------------------------------

.. automodule:: annofabapi.util.tracking_id
   :members:
   :show-inheritance:
   :undoc-members:

Module contents
---------------

.. automodule:: annofabapi.util
   :members:
   :show-inheritance:
   :undoc-members:
