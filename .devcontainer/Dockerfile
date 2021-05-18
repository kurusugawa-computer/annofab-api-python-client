FROM ubuntu:18.04 as devcontainer

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        tzdata \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* \
    && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && echo 'Asia/Tokyo' >/etc/timezone

# create vscode user
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        sudo \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >>/etc/sudoers.d/ALL \
    && groupadd \
        --gid 5000 \
        vscode \
    && useradd \
        --uid 5000 \
        --gid 5000 \
        --home-dir /home/vscode \
        --create-home \
        --shell /bin/bash \
        vscode

# vscode extensions cache
# https://code.visualstudio.com/docs/remote/containers-advanced#_avoiding-extension-reinstalls-on-container-rebuild
RUN set -x \
    && mkdir -p /home/vscode/.vscode-server/extensions /home/vscode/.vscode-server-insiders \
    && chown -R vscode:vscode /home/vscode/.vscode-server /home/vscode/.vscode-server-insiders \
    && ln -s /home/vscode/.vscode-server/extensions /home/vscode/.vscode-server-insiders/extensions

# common tools
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        bash-completion \
        curl \
        git \
        gnupg2 \
        iputils-ping \
        jq \
        less \
        net-tools \
        openssh-client \
        tar \
        time \
        unzip \
        xz-utils \
        zip \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*

# docker
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        docker-ce-cli \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* \
    && groupadd --gid 999 docker \
    && usermod -aG docker vscode

# docker compose
ARG COMPOSE_VERSION=1.27.4
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* \
    && curl -fsSL "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose \
    && curl -fsSL -o /etc/bash_completion.d/docker-compose "https://raw.githubusercontent.com/docker/compose/${COMPOSE_VERSION}/contrib/completion/bash/docker-compose"

# docker / docker-compose in devcontainer
RUN set -x \
    && mkdir -p /usr/local/devcontainer-tool/bin \
    && curl -fsSL -o /usr/local/devcontainer-tool/bin/docker https://raw.githubusercontent.com/thamaji/devcontainer-docker/main/docker \
    && chmod +x /usr/local/devcontainer-tool/bin/docker \
    && curl -fsSL -o /usr/local/devcontainer-tool/bin/docker-compose https://github.com/thamaji/devcontainer-compose/releases/download/v1.0.0/docker-compose \
    && chmod +x /usr/local/devcontainer-tool/bin/docker-compose
ENV PATH=/usr/local/devcontainer-tool/bin:${PATH}

# python3.8
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3.8 \
        python3-distutils \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* \
    && ln -s $(which python3.8) /usr/local/bin/python

# pip
RUN set -x \
    && curl -sSL https://bootstrap.pypa.io/get-pip.py | sudo -u vscode -i python - 

# poetry
RUN set -x \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | sudo -u vscode -i python - \
    && sudo -u vscode -i /home/vscode/.local/bin/poetry config virtualenvs.in-project true
ENV PATH=$PATH:/home/vscode/.local/bin

# fix poetry issue (see: https://github.com/python-poetry/poetry/issues/221)
RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        language-pack-en \
    && apt-get clean && rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/*
ENV LC_ALL=C.UTF-8


USER vscode

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "bash", "-eux", "/entrypoint.sh" ]
