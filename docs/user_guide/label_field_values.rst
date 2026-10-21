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
  幅・高さは外接矩形の大きさです。ベクタ図形では、各頂点座標を整数に丸めてから座標の最大値と最小値の差を求めます。
  塗りつぶしでは領域をクロップした矩形のサイズを使います。
  ``min_warn_rule={"_type": "And"}`` は幅と高さの **両方が最小値未満** の場合、
  ``{"_type": "Or"}`` は **いずれかが最小値未満** の場合の警告です。
  ポリゴン・ポリラインは同じ最小サイズ制約を提出時にも検証し、違反は提出エラーになります。
  矩形・塗りつぶしのこのサイズ警告自体は提出・合格を妨げません。
* OpenAPIに記載された文字列形式の ``"and"`` ・ ``"or"`` も説明用の互換入力として扱います。
  本体のJSON形式は判別子付きオブジェクトです。互換入力を説明できることは、
  その形式でAnnofabのAPIに登録できることを意味しません。
* 矩形の挿入位置は、作図モードで作図ボタンを押して矩形を作成するときの位置です。
  警告の閾値は0でも、挿入時の幅・高さはそれぞれ ``max(設定値, 1)`` に補正されます。
  ``position_for_minimum_bounding_box_insertion=[x, y]`` は画像左上を原点とする矩形の左上座標です。
  省略と ``null`` は説明上区別し、いずれも表示範囲の中央を基準に配置します。
  中央から幅・高さの半分（整数除算）を引いた左上座標が負なら、その座標を0に補正します。
  明示した座標にはこの補正を適用しません。
* 最小面積はポリゴンの面積についての警告です。外接矩形の面積ではありません。
  この面積警告自体は提出・合格を妨げません。
* 頂点数の ``min`` ・ ``max`` は省略可能です。省略と明示的な ``null`` を区別して説明し、
  いずれもその側の追加の頂点数制約を設けないことを意味します。
  数値は上下限を含む範囲で判定し、追加制約の違反は警告です。
  図形自体に必要なポリゴンの3頂点、ポリラインの2頂点を下回る場合は提出エラーになります。
  頂点数は保存された配列の要素数を使い、重複頂点を除去して数え直すことはしません。
  本APIの対応範囲では数値の上下限を図形の最小頂点数以上、上限を下限以上とします。
* ポリゴンの頂点数設定は、多角形作図ツールの頂点数の初期値にも使われます。
  上限があれば上限を採用し、上限がなければ下限と標準初期値16の大きい方を採用します。
  ポリラインにこの作図初期値の説明は追加しません。
* 最小面積は1以上の整数、最小幅・高さと許容誤差は0以上の整数として扱います。
  真偽値を整数と同一視しません。
  許容誤差は自動的に誤差を検証する制約ではなく、許容範囲表示に使う値です。
  0の場合は円を描画しません。正の値では画素境界を考慮して描画半径に0.5を加えるため、
  説明文では「設定値と同じ半径の円」とは断定しません。
* 線の向きの ``has_direction`` は真偽値を必須とします。
  ``false`` は非表示、``true`` は表示を有効にする設定です。
  ``true`` でもエディタ側の線の向きの非表示設定が優先されます。
* 作図機能は ``append`` ・ ``erase`` ・ ``freehand`` ・ ``rectangle_fill`` ・
  ``polygon_fill`` ・ ``fill_near`` の真偽値をすべて必須とします。
  ``append`` ・ ``erase`` は作図モードの選択、残りは作図ツールの有効・無効として説明します。
  追記・消しゴムモードには、編集可能な状態と対象アノテーションの選択も必要です。
  塗りつぶしv2では ``append=false`` でも、通常の作図モードで同じラベルの既存領域へ追記します。

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

本体ソースとの照合
------------------

Annofab本体のリビジョン ``5c7c420de456b87eb29274c0b974d23045ba28da`` に対して、
設定定義から画像エディタへの変換、表示・作図、提出時検証までを静的に照合しました。
以下のパスはAnnofab本体リポジトリ内のものです。

* ``common/shared/src/main/scala/jp/kurusugawa/af/common/model/v1/AnnotationSpecs.scala``

  * ``AnnotationTypeDefinition.getSystemDefinedAnnotationTypeDefinition``: 標準ラベルの適用可能なフィールド。
  * ``AnnotationTypeFieldValue``: 実際のJSONの型。頂点数の上下限は ``Option[Int]``。
  * ``AnnotationSpecsLabel.V2.fromV3`` / ``toLabelV2MetadataAndFeature``: 画像エディタ向けの設定変換。
  * ``AnnotationTypeFieldDefinition.MinimumSize2d.validateAnnotation``: ポリゴン・ポリラインの最小サイズ検証。
    矩形用の ``MinimumSize2dWithDefaultInsertPosition`` と面積・頂点数の検証は同じ実装ではありません。
* ``common/shared/src/main/scala/jp/kurusugawa/af/common/model/v1/TaskValidation.scala``

  * ``ValidationError.validateSingle``: 図形の最低頂点数とフィールドの検証結果を提出エラーへ変換。
  * ``InspectionValidation.canSubmit``: アノテーションエラーがあると提出不可。
* ``server/js/src/main/scala/jp/kurusugawa/af/server/application/v1/task/OperateTask.scala``

  * ``validateForSubmit``: 標準ラベルの定義を使って検証し、違反時は提出操作を失敗させる経路。
* ``client/projects/annotation-editor-images/src/main/scala/jp/kurusugawa/af/client/annotation_editor_images/``

  * ``view/data/AnnotationSpecsLabel.scala``: 外接矩形サイズ・面積・頂点数の警告、作図ツールの有効性。
  * ``view/data/AnnotationDetailBody.scala``: ベクタ図形の整数への丸めと外接矩形、塗りつぶしのクロップサイズ。
  * ``logic/ViewLogic.scala``: 矩形挿入時の0→1補正、挿入位置、作図モードの選択条件、初期頂点数。
  * ``view/tool/PolyToolProvider.scala``: 初期頂点数を多角形作図ツールに適用。
  * ``view/tool/SegmentationToolProvider.scala``: 塗りつぶしv2の通常作図でも既存領域へ追記する分岐。
  * ``view/AnnotationCanvas.scala``: ラベルの線の向きの設定と、エディタの非表示設定の組み合わせ。
  * ``view/ToleranceCircleGraphics.scala``: 許容誤差0は非描画、正の値の円は半径に0.5を加えて描画。

公式マニュアルにはサイズ違反は警告と記載されていますが、上記の本体リビジョンでは
ポリゴン・ポリラインの最小サイズ違反を提出時にも検証する経路があります。
本APIの説明はこのラベル種類による差を反映しています。
回帰テストの期待値も、この本体ソースで確認した条件に基づいています。
本体やエディタの仕様変更時は、この対応関係も見直してください。
