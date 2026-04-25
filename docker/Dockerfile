FROM driveone/onedrive:debian

RUN mkdir "/scratch"
RUN apt-get update
RUN apt-get install -y  \
    python3 \
    gnucash sqlite3

RUN apt-get install -y python3-pil python3-pip

RUN pip3 install --break-system-packages docxtpl

# Latex packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-all && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-calc fonts-dejavu-core && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY generate_kamp_overview.py /scratch/generate_kamp_overview.py
COPY docker/docker_script.sh /scratch/docker_script.sh
COPY build_declaration.py /scratch/build_declaration.py
COPY generate_enroll_forms.py /scratch/generate_enroll_forms.py
COPY template.tex /scratch/template.tex
COPY form_templates /scratch/form_templates/
#COPY bon_1.xlsx /scratch/bon_1.xlsx

RUN ln -s /usr/local/bin/gosu /usr/sbin/gosu # ugly hack to make the same script work on raspbian and in this container

ENTRYPOINT ["/scratch/docker_script.sh"]
#ENTRYPOINT ["/bin/bash"]