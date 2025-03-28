FROM ubuntu:22.04

ENV PYTHONHASHSEED=0 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    TZ=Etc/UTC \
    PYTHON_VERSION=3.12 \
    REPO=textualize/rich \
    BRANCH=master \
    WORKSPACE=/rich

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    zlib1g-dev \
    libssl-dev \
    locales \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen

RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/bin" sh

RUN useradd -ms /bin/bash runner

RUN mkdir -p ${WORKSPACE} && \
    chown -R runner:runner ${WORKSPACE} && \
    chmod -R u+rwX,go+rX,go-w ${WORKSPACE}

USER runner
WORKDIR ${WORKSPACE}

RUN uv python install -v ${PYTHON_VERSION}

RUN git config --global http.postBuffer 1048576000 && \
    git config --global http.lowSpeedLimit 0 && \
    git config --global http.lowSpeedTime 999999

RUN git clone --depth=1 --branch ${BRANCH} "https://github.com/${REPO}.git" "${WORKSPACE}"

RUN uv venv -v
RUN uv pip -v install . pytest
RUN uv pip install -U attrs pytest pytest-mock hypothesis

ENV PATH="/rich/.venv/bin:$PATH"

RUN uv run python -m pytest -v tests || true

CMD ["bash"]

