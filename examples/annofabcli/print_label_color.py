"""
アノテーションラベルの色(RGB)を出力する
"""

import argparse
import json
import logging
import annofabcli
from typing import Any, Callable, Dict, List, Optional, Tuple  # pylint: disable=unused-import

import annofabapi
from annofabcli.common.utils import AnnofabApiFacade

logger = logging.getLogger(__name__)


class PrintLabelColor:
    """
    アノテーションラベルの色(RGB)を出力する
    """

    def __init__(self, service: annofabapi.Resource, facade: AnnofabApiFacade):
        self.service = service
        self.facade = facade

    @staticmethod
    def get_rgb(label: Dict[str, Any]) -> Tuple[int, int, int]:
        color = label["color"]
        return color["red"], color["green"], color["blue"]

    def print_label_color(self, project_id: str):
        """
        今のアノテーション仕様から、label名とRGBを紐付ける
        Args:
            args:

        Returns:
        """
        annotation_specs = self.service.api.get_annotation_specs(project_id)[0]
        labels = annotation_specs["labels"]

        label_color_dict = {
            self.facade.get_label_name_en(l): self.get_rgb(l)
            for l in labels
        }

        print(json.dumps(label_color_dict, indent=2))

    def main(self, args):
        annofabcli.utils.load_logging_config_from_args(args, __file__)
        logger.info(args)

        self.print_label_color(args.project_id)


def parse_args(parser: argparse.ArgumentParser):
    parser.add_argument('project_id', type=str, help='対象のプロジェクトのproject_id')

    parser.set_defaults(subcommand_func=main)


def main(args):
    try:
        service = annofabapi.build_from_netrc()
        facade = AnnofabApiFacade(service)

        PrintLabelColor(service, facade).main(args)

    except Exception as e:
        logger.exception(e)
