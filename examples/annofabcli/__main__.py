import argparse
import logging

import annofabcli.cancel_acceptance
import annofabcli.complete_tasks
import annofabcli.diff_projects
import annofabcli.invite_users
import annofabcli.print_label_color
import annofabcli.print_unprocessed_inspections
import annofabcli.reject_tasks
import annofabcli.write_annotation_image

logger = logging.getLogger(__name__)

def main():
    """
    サブコマンドとして利用できるようにする。
    ただし`deprecated`なツールは、サブコマンド化しない。
    """

    parser = argparse.ArgumentParser(
        description="annofabapiを使ったCLIツール")

    subparsers = parser.add_subparsers()

    # サブコマンドの定義
    annofabcli.cancel_acceptance.add_parser(subparsers)

    annofabcli.complete_tasks.add_parser(subparsers)

    annofabcli.diff_projects.add_parser(subparsers)

    annofabcli.invite_users.add_parser(subparsers)

    annofabcli.print_unprocessed_inspections.add_parser(subparsers)

    annofabcli.print_label_color.add_parser(subparsers)

    annofabcli.reject_tasks.add_parser(subparsers)

    annofabcli.write_annotation_image.add_parser(subparsers)

    args = parser.parse_args()
    if hasattr(args, 'subcommand_func'):
        try:
            args.subcommand_func(args)
        except Exception as e:
            logger.exception(e)
            raise e

    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()


if __name__ == "__main__":
    main()
