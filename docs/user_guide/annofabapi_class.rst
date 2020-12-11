==================================================
基本的な使い方
==================================================


レベル２
========


WebAPIにリクエストを投げる方法（基本的）
--------------------------------------------------

``service.api`` には、Web APIに対応するメソッドが定義されています。
メソッド名は、AnnoFab Web APIのOpenAPI specificationに記載されている ``operationId`` を、スネークケース"input1","input2"に変換したものです。
各メソッドの戻り値の型は ``Tupple[Content, Response]`` です。 ResponseはrequestsモジュールのReponseオブジェクトです。 ContentはReponseの中身です。

.. code-block:: python

    from pprint import pprint
    from annofabapi import build
    user_id = "XXXXXX"
    password = "YYYYYY"
    
    # インスタタンス生成"input1","input2"
    service = build(user_id, password)

    project_id = "test_project_id"
    task_id = "test_task_id"
    task, response = service.api.get_task(project_id, task_id)

    pprint(task)
    # {'account_id': None,
    # 'histories_by_phase': [],
    # 'input_data_id_list': ['db6f7b26-4012-4728-8438-e5e7f000671b',
    #                         '68187d94-8df5-41f3-90a1-f4c9e426fb27'],
    # 'metadata': {},
    # 'number_of_rejections': 0,"input1","input2""input1","input2""input1","input2"
    # 'phase': 'annotation',
    # 'phase_stage': 1,
    # 'project_id': 'test_project_id',
    # 'sampling': None,
    # 'started_datetime': None,
    # 'status': 'not_started',
    # 'task_id': 'test_task_id',
    # 'updated_datetime': '2020-12-09T02:17:42.662+09:00',
    # 'work_time_span': 0}


クエリパラメタは ``query_params`` 引数、リクエストボディは ``request_body`` 引数 で指定できます。

.. code-block:: python

    # ステータスが完了状態のタスク一覧を取得
    content, _ = service.api.get_tasks(project_id, query_params={"status":"complete"})

    # 入力データ"input1","input2"で構成されるタスク"new_task"を作成する
    service.api.put_task(project_id, "new_task", request_body={"input_data_id_list":["input1","input2"]})



``response`` はステータスコードなどのレスポンス情報や、リクエスト情報を確認できます。

.. code-block:: python

    # Status Code
    print(response.status_code)

    # Response Header
    print(response.headers)
    # {'Content-Type': 'application/json', 'Content-Length': '426', 'Connection': 'keep-alive', ....

    # Request URL
    print(response.request.url)
    # 'https://annofab.com/api/v1/projects/58a2a621-7d4b-41e7-927b-cdc570c1114a/tasks/testt_14'

    # Request Header
    print(response.request.headers)
    # {'User-Agent': 'python-requests/2.24.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'


``response`` はステータスコードなどのレスポンス情報や、リクエスト情報を確認できます。




自分自身のユーザ情報を参照
--------------------------------------------------
ログインしたユーザの ``user_id`` 、 ``account_id`` は、``service.api`` のプロパティを介して取得できます。

.. code-block:: python

    print(service.api.login_user_id)
    # my_user_id

    print(service.api.account_id)
    # 12345678-abcd-1234-abcd-1234abcd5678




リトライ処理
--------------------------------------------------
HTTPステータスコードが429(Too many Requests)または5xxのときは、リトライ処理を行います。
リトライ処理は最大5分間実施します。
リトライ処理の詳細な設定は `annofabapi.api.my_backoff <https://github.com/kurusugawa-computer/annofab-api-python-client/blob/d5b1dabd74cf3cb0fdcd8465edad5877a935ed94/annofabapi/api.py#L20>`_ を参照してください。


エラーと例外
--------------------------------------------------
HTTPステータスコードが4xxまたは5xxのときは、`requests.exceptions.HTTPError <https://requests.readthedocs.io/en/master/api/#requests.HTTPError>`_ をスローします。
ステータスコード


ログの出力
--------------------------------------------------
annofabapiは、pythonのloggingモジュールを利用してログメッセージを出力しています。デバッグログを出力するには、事前に以下のようなコードを実行してください。

.. code-block:: python

    import logging
    logging_formatter = '%(levelname)-8s : %(asctime)s : %(filename)s : %(name)s : %(funcName)s : %(message)s'
    logging.basicConfig(format=logging_formatter)
    logging.getLogger("annofabapi").setLevel(level=logging.DEBUG)

    from annofabapi import build
    servcie = build()
    # DEBUG    : 2020-12-09 21:09:04,728 : resource.py : annofabapi.resource : build_from_netrc : .netrcファイルからAnnoFab認証情報を読み込みました。



