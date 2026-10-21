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

入力データ・組織設定・組織メンバー・Webhook・プラグインの画面には、
次の生成・解析関数を利用できます。生成時には各IDや組織名をパーセントエンコードします。

.. list-table::
   :header-rows: 1

   * - 生成関数
     - 解析関数
     - 抽出する情報
   * - ``create_input_data_url``
     - ``parse_input_data_url``
     - ``project_id``, ``input_data_id``
   * - ``create_organization_url`` （設定画面）
     - ``parse_organization_url``
     - ``organization_name``
   * - ``create_organization_member_url``
     - ``parse_organization_member_url``
     - ``organization_name``, ``user_id``
   * - ``create_webhook_url``
     - ``parse_webhook_url``
     - ``project_id``, ``webhook_id``
   * - ``create_plugin_url``
     - ``parse_plugin_url``
     - ``organization_name``, ``plugin_id``

これらの解析関数は、後続のパス、クエリ、フラグメントを無視します。
``parse_project_url`` は入力データ・Webhookの画面にも、
``parse_organization_url`` は設定・メンバー・プラグインの画面にも対応します。

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

.. code-block:: python

    from annofabapi.util.page import create_organization_member_url, parse_organization_member_url

    url = create_organization_member_url("DAIKIN", "kawamatsu_yuuji")
    assert url == "https://annofab.com/organizations/DAIKIN/members/kawamatsu_yuuji"
    member = parse_organization_member_url(url)
    assert member.organization_name == "DAIKIN"
    assert member.user_id == "kawamatsu_yuuji"

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
