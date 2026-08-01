FROM driveone/onedrive:debian
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir "/scratch"

# Latex packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-all && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-calc fonts-dejavu-core && \
    apt-get clean &&  \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends fontconfig && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/local/share/fonts/custom

COPY fonts/* /usr/local/share/fonts/custom/

RUN chmod 644 /usr/local/share/fonts/custom/* && \
    fc-cache -fv

COPY uv.lock /scratch/uv.lock
COPY pyproject.toml /scratch/pyproject.toml

RUN ln -s /usr/local/bin/gosu /usr/sbin/gosu # ugly hack to make the same script work on raspbian and in an ubuntu container

RUN cd /scratch && \
    /bin/uv sync


#ENTRYPOINT ["/scratch/docker_script.sh"]
#ENTRYPOINT ["/bin/bash"]