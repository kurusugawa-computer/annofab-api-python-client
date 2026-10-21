ラベルの図形設定の説明
======================

``annofabapi.util.label_field_values.describe_label_field_values`` は、
ラベルの ``field_values`` を定型文で説明します。ネットワークアクセスやLLMは使用しません。
``lang="ja"`` で日本語、``lang="en"`` （既定値）で英語を指定します。
未対応の言語は ``ValueError`` になります。

.. code-block:: python

    from annofabapi.util.label_field_values import describe_label_field_values

    label = {
        "annotation_type": "polyline",
        "field_values": {
            "display_line_direction": {
                "_type": "DisplayLineDirection",
                "has_direction": False,
            }
        },
    }
    descriptions = describe_label_field_values(label, lang="ja")
    assert descriptions[0].field_id == "display_line_direction"
    assert descriptions[0].text == "ポリラインの向きの表示は無効です。"
    assert descriptions[0].is_supported

戻り値は入力順の ``FieldValueDescription`` のリストです。
各要素が元のフィールドID、説明文、設定全体を解釈できたかどうかを保持します。
JSONフィールド名の決定、CSV・Markdownの整形は呼び出し側で行います。
説明はJSONの設定値・論理条件・有効無効・指定状態を対象とします。入力のラベルは変更しません。

対応範囲
--------

標準の画像ラベルについて、次のフィールドIDと ``_type`` の組み合わせに対応します。

.. list-table::
   :header-rows: 1
   :widths: 38 30 32

   * - フィールドID
     - ``_type``
     - 適用する ``annotation_type``
   * - ``minimum_size_2d``
     - ``MinimumSize2d``
     - polygon, polyline, segmentation, segmentation_v2
   * - ``minimum_size_2d_with_default_insert_position``
     - ``MinimumSize2dWithDefaultInsertPosition``
     - bounding_box
   * - ``minimum_area_2d``
     - ``MinimumArea2d``
     - polygon
   * - ``vertex_count_min_max``
     - ``VertexCountMinMax``
     - polygon, polyline
   * - ``margin_of_error_tolerance``
     - ``MarginOfErrorTolerance``
     - bounding_box, polygon, polyline, point, segmentation, segmentation_v2
   * - ``display_line_direction``
     - ``DisplayLineDirection``
     - polyline
   * - ``annotation_editor_feature``
     - ``AnnotationEditorFeature``
     - segmentation, segmentation_v2

* 最小サイズは ``min_width`` ・ ``min_height`` ・ ``min_warn_rule`` を必須とし、
  設定された幅・高さと論理条件を説明します。
  ``min_warn_rule`` は違反条件の論理演算なので、制約を満たす条件では演算が逆になります。
  ``{"_type": "And"}`` は「幅が最小値以上、または高さが最小値以上」、
  ``{"_type": "Or"}`` は「幅が最小値以上、かつ高さが最小値以上」です。
  文字列形式の ``"and"`` ・ ``"or"`` も同じ意味として扱います。
* 矩形の ``position_for_minimum_bounding_box_insertion`` は、指定された座標を説明します。
  省略と ``null`` は区別してその指定状態を説明します。
* ``minimum_area_2d.min_area`` は最小面積（平方ピクセル）、
  ``margin_of_error_tolerance.max_pixel`` は誤差許容範囲（ピクセル）として説明します。
* 頂点数は ``min`` ・ ``max`` の上下限をそれぞれ説明します。
  省略と ``null`` は区別し、どちらもその側の追加制約が指定されていないことを説明します。
* 線の向きの ``has_direction`` は、表示設定の有効・無効として説明します。
* 作図機能は ``append`` ・ ``erase`` ・ ``freehand`` ・ ``rectangle_fill`` ・
  ``polygon_fill`` ・ ``fill_near`` の真偽値をすべて必須とします。
  ``append`` ・ ``erase`` は作図モードの選択、残りは作図ツールの有効・無効として説明します。

数値を出力するときは、JSONにある設定値をそのまま使います。

省略・未対応項目
----------------

明示された設定だけを説明します。``field_values`` の省略・空オブジェクトは空リストを返し、
「制限なし」や「無効」などの既定動作は補完しません。
``field_values`` 自体が ``null`` ・ ``false`` などの場合は、そのコンテナを未対応として返します。

設定値の ``null`` ・ ``false`` ・空オブジェクト、必須項目の欠落、未知のキー・型・値、
既知の設定に含まれる未知の入れ子の項目も、黙って省略しません。
一部だけ解釈して設定全体を説明したように見せることを避けるため、
そのフィールド全体を ``is_supported=False`` とし、指定言語の説明と元のキー・値のJSONを返します。
ほかのフィールドの説明は続行します。

ユーザー定義ラベル・任意のフィールドID、``OneIntegerFieldValue`` ・ ``OneStringFieldValue`` ・
``OneBooleanFieldValue`` ・ ``EmptyFieldValue`` 、動画・3次元ラベルの設定は未対応です。
フィールド定義やプラグインが必要な設定の意味は推測しません。
このAPIは説明生成用であり、Annofabの入力検証全体を代替するものではありません。

仕様確認元
----------

2026年10月22日時点の以下の資料と、既存テストデータの実レスポンス例を確認しました。

* `画像プロジェクトで利用可能なラベル <https://annofab.readme.io/docs/image-labels>`_
* `Annofab WebAPI OpenAPI <https://annofab.com/docs/api/swagger-api-components.yaml>`_
  （リポジトリ内の ``generate/swagger/swagger-api-components.yaml`` と同一）
* `CLIのfield_valuesのサンプル <https://annofab-cli.readthedocs.io/ja/latest/command_reference/annotation_specs/update_label_field_values.html>`_

OpenAPIの ``min_warn_rule`` は文字列形式ですが、実レスポンス例では
``{"_type": "And"}`` ・ ``{"_type": "Or"}`` です。
また、OpenAPIの数値下限やnullableの記載には実データとの差があるため、
幅・高さ・許容誤差の0や頂点数の ``null`` を一律に不正値とは扱いません。

設定の型・適用対象・論理条件・省略と ``null`` の意味は、Annofab本体の
リビジョン ``5c7c420de456b87eb29274c0b974d23045ba28da`` でも確認しました。
