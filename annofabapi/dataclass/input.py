# flake8: noqa: W291
# pylint: disable=too-many-lines,trailing-whitespace

"""
annofabapiのmodelをDataClassで定義したクラス

Note:
    このファイルはopenapi-generatorで自動生成される。詳細は generate/README.mdを参照.
    oneOf, allOfなどは正しく表現できない可能性がある。
"""

import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

# 列挙体の一覧
from annofabapi.models import (AccountAuthority, AdditionalDataDefinitionType, AnnotationDataHoldingType,
                               AnnotationType, AssigneeRuleOfResubmittedTask, InputDataOrder, InputDataType,
                               InspectionStatus, OrganizationMemberRole, OrganizationMemberStatus, PricePlan,
                               ProjectMemberRole, ProjectMemberStatus, ProjectStatus, TaskPhase, TaskStatus)




@dataclass_json
@dataclass
class Resolution:
    """
    画像などの解像度 
    """
    width: float
    """"""



    height: float
    """"""










@dataclass_json
@dataclass
class InputData:
    """
    
    """
    input_data_id: str
    """"""



    project_id: str
    """"""



    input_data_name: str
    """表示用の名前です。"""



    input_data_path: str
    """入力データの実体が保存されたパスです。 s3スキーマまたはhttpsスキーマのみサポートしています。 """



    url: Optional[str]
    """入力データを取得するためのhttpsスキーマのURLです。  このURLはセキュリティのために認証認可が必要となっており、URLだけでは入力データを参照できません。 このURLは内部用であり、常に変更になる可能性があります。そのため、アクセスは保証外となります。 また、このURLのレスポンスは最低1時間キャッシュされます。 キャッシュを無効にしたい場合は、クエリパラメータにアクセス毎にランダムなUUIDなどを付与してください。  設定の不備等でデータが取得できない場合、この属性は設定されません。 """



    etag: Optional[str]
    """"""



    original_input_data_path: Optional[str]
    """AF外部のストレージから登録された場合、その外部ストレージ中のパス。 それ以外の場合は値なし """



    original_resolution: Optional[Resolution]
    """"""



    resized_resolution: Optional[Resolution]
    """"""



    updated_datetime: str
    """"""



    sign_required: Optional[bool]
    """データがSigned Cookieによるクロスオリジン配信に対応しているか否かです。 """







