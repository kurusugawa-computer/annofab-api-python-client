import argparse
import annofabapi
import annofabcli
from annofabcli.common.utils import AnnofabApiFacade

import annofabcli.complete_tasks
import annofabcli.cancel_acceptance
import annofabcli.diff_projects
import annofabcli.invite_users
import annofabcli.reject_tasks
import annofabcli.print_unprocessed_inspections
import annofabcli.print_label_color


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="annofabapiを使ったCLIツール", parents=[annofabcli.utils.create_parent_parser()], epilog="AnnoFab認証情報は`.netrc`に記載すること")

    subparsers = parser.add_subparsers()

    annofabcli.cancel_acceptance.parse_args(subparsers.add_parser("cancel_acceptance",
        help="受け入れ完了タスクを、受け入れ取り消しする。"))

    annofabcli.complete_tasks.parse_args(subparsers.add_parser("complete_tasks",
        help="deprecated: タスクを受け入れ完了にする。その際、検査コメントを適切な状態にする。"))

    annofabcli.diff_projects.parse_args(subparsers.add_parser("diff_projects",
        help="プロジェクト間の差分を表示する。"
        "ただし、AnnoFabで生成されるIDや、変化する日時などは比較しない。"))

    annofabcli.invite_users.parse_args(subparsers.add_parser("invite_users",
        help="複数のプロジェクトに、ユーザを招待する。"))

    annofabcli.reject_tasks.parse_args(subparsers.add_parser("reject_tasks",
        help="検査コメントを付与してタスクを差し戻す。検査コメントは先頭の画像の左上(0,0)に付与する。"))

    annofabcli.print_unprocessed_inspections.parse_args(subparsers.add_parser("print_unprocessed_inspections",
        help="未処置の検査コメントIDのList(task_id, input_data_idごと)を出力する。"
    "出力された内容は、`complete_tasks`ツールに利用する。"
    "出力内容は`Dict[TaskId, Dict[InputDatId, List[Inspection]]]`である."))

    annofabcli.print_label_color.parse_args(subparsers.add_parser("print_label_color",
        help="アノテーション仕様から、label_nameとRGBを対応付けたJSONファイルを出力する。"))

    args = parser.parse_args()

    if hasattr(args, 'subcommand_func'):
        args.subcommand_func(args)

    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()


