"""プラグイン関係"""

from enum import Enum


class AnnotationTypePluginId(Enum):
    """
    アノテーション種類の標準（ビルトイン）プラグインのID
    """

    THREE_DIMENSION = "703ababa-96ac-4920-8afb-d4f2bddac7e3"
    """
    3次元プロジェクトのアノテーション仕様を定義した標準プラグインのID
    "af-default-extended-spec-plugin-for-3d-editor"
    （Annofab本番環境/開発環境でIDは同じ）
    """


class ThreeDimensionAnnotationType(Enum):
    """
    3次元アノテーションの種類（アノテーション種類の標準プラグインで定義されている）
    """

    BOUNDING_BOX = "user_bounding_box"
    """バウンディングボックス"""
    INSTANCE_SEGMENT = "user_instance_segment"
    """インスタンスセグメント"""
    SEMANTIC_SEGMENT = "user_semantic_segment"
    """セマンティックセグメント"""
