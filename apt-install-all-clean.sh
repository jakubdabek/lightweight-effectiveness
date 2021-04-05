DEBIAN_FRONTEND=noninteractive apt update && \
    apt install -y --no-install-recommends "$@" && \
    apt clean && apt autoclean && apt autoremove && rm -rf /var/lib/apt/lists/*
