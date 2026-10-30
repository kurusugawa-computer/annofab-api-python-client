廃止予定の機能
========================================

2027-04-01以降に削除予定
----------------------------------------

ダウンロードメソッドの旧名
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ダウンロードするファイル形式が分かるように、``Wrapper`` のメソッド名を変更しました。
以下の旧メソッドは非推奨です。呼び出すと、移行先と削除予定日を案内する
``FutureWarning`` が発生します。

旧メソッドは2027-04-01以降に削除予定のため、新メソッドに移行してください。
引数、戻り値、ダウンロード処理は変わりません。

.. list-table::
   :header-rows: 1

   * - 旧メソッド名
     - 移行先のメソッド名
   * - ``download_annotation_archive``
     - ``download_annotation_zip``
   * - ``download_project_inputs_url``
     - ``download_project_inputs_json``
   * - ``download_project_tasks_url``
     - ``download_project_tasks_json``
   * - ``download_project_comments_url``
     - ``download_project_comments_json``
   * - ``download_project_task_history_events_url``
     - ``download_project_task_history_events_json``
   * - ``download_project_task_histories_url``
     - ``download_project_task_histories_json``

使用例は :doc:`user_guide/advanced_usage` を参照してください。
