==================================================
開発者用の使い方
==================================================



ローカルのAnnoFab環境にアクセスする方法
--------------------------------------------------

.. code-block:: python

    from annofabapi import build
    service = build(login_user_id, login_password, endpoint_url="https://localhost:8080")



WebAPI v2にアクセスする方法
--------------------------------------------------
``service.api2`` インスタンス内に、WebAPI v2に対応したメソッドが定義されています。


.. code-block:: python

    from annofabapi import build
    content, _ = service.api2.get_annotation_specs_v2(project_id)

