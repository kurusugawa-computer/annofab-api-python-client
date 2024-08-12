FROM ubuntu:22.04

# Install prerequisites
RUN set -x \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        gnupg2 \
        software-properties-common \
        language-pack-ja \
        tzdata \
        curl \
        lsb-release \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

# Set locale & timezone
RUN update-locale LANG=ja_JP.UTF-8 LANGUAGE=ja_JP:ja \
    && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo "Asia/Tokyo" > /etc/timezone

ENV LANG=ja_JP.UTF-8
ENV LC_ALL=ja_JP.UTF-8
ENV LC_CTYPE=ja_JP.UTF-8

RUN set -x \
    && sed -i.bak -r 's!(deb|deb-src) \S+!\1 http://jp.archive.ubuntu.com/ubuntu/!' /etc/apt/sources.list

# Install Ubuntu packages
RUN set -x \
    # for docker
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    # Python3.12をインストールするために、deadsnakes PPAを追加
    && add-apt-repository ppa:deadsnakes/ppa \
    # Install packages
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        docker-ce-cli \
        # python
        python3.12-dev \
        # common tools
        bash-completion \
        build-essential \
        git \
        iputils-ping \
        jq \
        less \
        net-tools \
        openssh-client \
        sudo \
        tar \
        time \
        unzip \
        vim \
        wget \
        xz-utils \
        zip \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*


# docker hack in devcontainer
RUN set -x \
    && mkdir -p /usr/local/devcontainer-tool/bin \
    && curl -fsSL -o /usr/local/devcontainer-tool/bin/docker https://github.com/thamaji/devcontainer-docker/releases/download/v1.0.3/docker \
    && chmod +x /usr/local/devcontainer-tool/bin/docker
ENV PATH=/usr/local/devcontainer-tool/bin:${PATH}


# Python / pip
RUN ln -s $(which python3.12) /usr/bin/python
RUN curl -sSL https://bootstrap.pypa.io/get-pip.py | python -
ENV PYTHONDONTWRITEBYTECODE=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# # poetry
RUN set -x \
    && python -m pip install "poetry<1.9"

# Add user / Grant sudo privileges
RUN useradd -m -s /bin/bash -u 5000 -U vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/ALL \
    && groupadd --gid 999 docker \
    && usermod -aG docker vscode

USER vscode

RUN poetry config virtualenvs.in-project true

ENTRYPOINT [ "bash", "/entrypoint.sh" ]
