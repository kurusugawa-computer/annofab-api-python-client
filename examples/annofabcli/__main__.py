import argparse
import annofabapi
import annofabcli
from annofabcli.common.utils import AnnofabApiFacade

import annofabcli.deprecated_complete_tasks
import annofabcli.cancel_acceptance
import annofabcli.diff_projects
import annofabcli.invite_users
import annofabcli.reject_tasks

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="annofabapiを使ったCLIツール", parents=[annofabcli.utils.create_parent_parser()], epilog="AnnoFab認証情報は`.netrc`に記載すること")

    subparsers = parser.add_subparsers()


    annofabcli.deprecated_complete_tasks.parse_args(subparsers.add_parser("deprecated_complete_tasks",
        help="deprecated: タスクを受け入れ完了にする。その際、検査コメントを適切な状態にする。"))

    annofabcli.diff_projects.parse_args(subparsers.add_parser("diff_projects",
        help="プロジェクト間の差分を表示する。"
        "ただし、AnnoFabで生成されるIDや、変化する日時などは比較しない。"))

    annofabcli.invite_users.parse_args(subparsers.add_parser("invite_users",
        help="複数のプロジェクトに、ユーザを招待する。"))

    annofabcli.reject_tasks.parse_args(subparsers.add_parser("reject_tasks",
        help="検査コメントを付与してタスクを差し戻す。検査コメントは先頭の画像の左上(0,0)に付与する。"))



    # annofabcli.cancel_acceptance(subparsers.add_parser("cancel_acceptance", help=""))

    args = parser.parse_args()
