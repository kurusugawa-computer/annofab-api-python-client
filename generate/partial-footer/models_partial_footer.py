@deprecated_class(deprecated_date="2022-08-23")
class InspectionStatus(Enum):
    """
    ##### スレッドの先頭のコメントである（`parent_inspection_id` に値がない）場合  * `annotator_action_required` - 未処置。`annotation`フェーズ担当者が何らかの回答をする必要あり * `no_correction_required` - 処置不要。`annotation`フェーズ担当者が、検査コメントによる修正は不要、と回答した * `error_corrected` - 修正済み。`annotation`フェーズ担当者が、検査コメントの指示どおり修正した  ##### 返信コメントである（`parent_inspection_id` に値がある）場合  現在は使用しておらず、レスポンスに含まれる値は不定です。APIのレスポンスにこの値を含む場合でも、「スレッドの先頭のコメント」の値を利用してください。  リクエストボディに指定する場合は、スレッドの先頭のコメントと同じ値を指定します。 
    """
    ANNOTATOR_ACTION_REQUIRED = "annotator_action_required"
    NO_CORRECTION_REQUIRED = "no_correction_required"
    ERROR_CORRECTED = "error_corrected"

