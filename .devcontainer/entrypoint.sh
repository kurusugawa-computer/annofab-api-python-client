#!/bin/bash
set -eu

# docker.sock から gid を取得して、docker グループの gid を変更
docker_group_id=$(ls -n /var/run/docker.sock | cut -d ' ' -f 4)
sudo groupmod --gid ${docker_group_id} docker

# 無限待ち（vscode デフォルトの entrypoint と同じ方法で）
while sleep 1000; do :; done