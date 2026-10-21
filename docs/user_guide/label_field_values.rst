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
    assert descriptions[0].text == "ポリラインの向きを表示しません。"
    assert descriptions[0].is_supported

戻り値は入力順の ``FieldValueDescription`` のリストです。
各要素が元のフィールドID、説明文、設定全体を解釈できたかどうかを保持します。
JSONフィールド名の決定、CSV・Markdownの整形は呼び出し側で行います。
入力のラベルは変更しません。既存の属性制約APIの対応言語には影響しません。

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

* 最小サイズは ``min_width`` ・ ``min_height`` ・ ``min_warn_rule`` を必須とします。
  ``min_warn_rule={"_type": "And"}`` は幅と高さの **両方が最小値未満** の場合、
  ``{"_type": "Or"}`` は **いずれかが最小値未満** の場合の警告です。
  OpenAPIに記載された文字列形式の ``"and"`` ・ ``"or"`` も同じ意味として扱います。
  サイズ制約の警告はタスクの提出・合格を妨げません。
* 矩形の挿入位置は、最小サイズの矩形を作図ボタンで作成するときの位置です。
  ``position_for_minimum_bounding_box_insertion=[x, y]`` は画像左上を原点とする座標です。
  省略と ``null`` は説明上区別し、いずれも表示範囲の中央に挿入すると説明します。
  最小サイズの設定全体を解釈できた場合に限り説明します。
* 頂点数は ``min`` ・ ``max`` の両キーを必須とします。
  明示的な ``null`` は、その側の追加の頂点数制約を設けないことを意味します。
  ポリゴンの3頂点以上、ポリラインの2頂点以上という図形自体の条件は残ります。
  数値の下限は図形の最小頂点数以上、上限は下限以上とします。
* 最小面積は1以上の整数、最小幅・高さと許容誤差は0以上の整数として扱います。
  真偽値を整数と同一視しません。許容誤差は画像エディタで表示する円の半径も説明します。
* 線の向きの ``has_direction`` は真偽値を必須とします。``false`` は非表示です。
* 作図機能は ``append`` ・ ``erase`` ・ ``freehand`` ・ ``rectangle_fill`` ・
  ``polygon_fill`` ・ ``fill_near`` の真偽値をすべて必須とし、使用可否をそれぞれ説明します。

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
