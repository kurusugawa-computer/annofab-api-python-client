import warnings  # pylint: disable=unused-import
from dataclasses import dataclass
from typing import Any, Dict, List, NewType, Optional, Tuple, Union  # pylint: disable=unused-import

from dataclasses_json import dataclass_json

from annofabapi.models import (AccountAuthority, AdditionalDataDefinitionType, AnnotationDataHoldingType,
                               AnnotationType, AssigneeRuleOfResubmittedTask, InputDataOrder, InputDataType,
                               InspectionStatus, OrganizationMemberRole, OrganizationMemberStatus, PricePlan,
                               ProjectMemberRole, ProjectMemberStatus, ProjectStatus, TaskPhase, TaskStatus)



@dataclass_json
@dataclass
class WebhookHeader:
    """

    """
    name: str
    """"""

    value: str
    """"""


@dataclass_json
@dataclass
class WebhookTestRequest:
    """

    """
    placeholders: object
    """プレースホルダ名と置換する値"""


@dataclass_json
@dataclass
class WebhookTestResponse:
    """

    """
    result: str
    """* success: 通知先から正常なレスポンス（2xx系）を受け取った * failure: 通知先からエラーレスポンス（2xx系以外）を受け取った * error: リクエスト送信に失敗した、もしくはレスポンスを受信できなかった """

    request_body: str
    """実際に送信されたリクエストボディ"""

    response_status: int
    """通知先から返されたHTTPステータスコード"""

    response_body: str
    """通知先から返されたレスポンスボディ"""

    message: str
    """result=\"error\" 時のエラー内容等"""




@dataclass_json
@dataclass
class Webhook:
    """

    """
    project_id: str
    """"""

    event_type: str
    """"""

    webhook_id: str
    """"""

    webhook_status: str
    """"""

    method: str
    """"""

    headers: List[WebhookHeader]
    """"""

    body: str
    """"""

    url: str
    """"""

    created_datetime: str
    """"""

    updated_datetime: str
    """"""
