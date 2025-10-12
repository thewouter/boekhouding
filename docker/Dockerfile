#FROM driveone/onedrive:debian
#
#RUN mkdir "/scratch"
#RUN apt-get update
#RUN apt-get install -y  \
#    python3 \
#    gnucash sqlite3
#
#RUN apt-get install -y python3-pil
#
## Latex packages
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
#    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-all && \
#    rm -rf /var/lib/apt/lists/*
#
#RUN apt-get update && \
#    apt-get install -y libreoffice libreoffice-calc fonts-dejavu-core && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*
#
#COPY generate_kamp_overview.py /scratch/generate_kamp_overview.py
#COPY docker/docker_script.sh /scratch/docker_script.sh
#COPY build_declaration.py /scratch/build_declaration.py
#COPY template.tex /scratch/template.tex
##COPY bon_1.xlsx /scratch/bon_1.xlsx
#
#ENTRYPOINT ["/scratch/docker_script.sh"]
##ENTRYPOINT ["/bin/bash"]

FROM driveone/onedrive:debian

# Create working dir
RUN mkdir -p /scratch

# Install only required packages (Python, Pillow, SQLite, LibreOffice, LaTeX essentials)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-pillow \
    sqlite3 \
    libreoffice-core \
    libreoffice-calc \
    libreoffice-common \
    texlive-latex-recommended \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-lang-european \
    poppler-utils \
    ghostscript \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy scripts/templates
COPY generate_kamp_overview.py /scratch/
COPY build_declaration.py /scratch/
COPY docker/docker_script.sh /scratch/
COPY template.tex /scratch/

# Make script executable
RUN chmod +x /scratch/docker_script.sh

ENTRYPOINT ["/scratch/docker_script.sh"]
