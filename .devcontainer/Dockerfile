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
    # Install packages
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        docker-ce-cli \
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




# Add user / Grant sudo privileges
ARG USERNAME=vscode
RUN useradd -m -s /bin/bash -u 5000 -U ${USERNAME} \
&& echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/ALL

USER ${USERNAME}

ARG UV_VERSION=0.6.14
RUN set -x \
    && curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh \
    && echo 'eval "$(uv generate-shell-completion bash)"' >> /home/${USERNAME}/.bashrc \
    && echo 'eval "$(uvx --generate-shell-completion bash)"' >> /home/${USERNAME}/.bashrc

ENV PATH=/home/${USERNAME}/.local/bin/:${PATH} \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy
    
# install python
ARG PYTHON_VERSION=3.13.11
RUN uv python install ${PYTHON_VERSION} --default --preview

