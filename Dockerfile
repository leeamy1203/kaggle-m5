FROM python:3.7

ENV TINI_VERSION v0.18.0
ENV POETRY_VERSION=1.0.0 

ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini

RUN chmod +x /usr/bin/tini && \
    apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install "poetry==$POETRY_VERSION" && \
    mkdir -p /home/ngs

WORKDIR /home/ngs

COPY pyproject.toml .
COPY poetry.lock .

EXPOSE 8888

# Leverage container space as opposed to venv within contianer
RUN poetry config virtualenvs.create false && \
    poetry install

RUN jupyter contrib nbextension install --system --symlink --perform-running-check && \
    jupyter nbextension enable execute_time/ExecuteTime && \
    jupyter nbextension enable toggle_all_line_numbers/main && \
    jupyter nbextension enable varInspector/main && \
    jupyter nbextension enable code_prettify/autopep8 && \
    jupyter nbextension enable notify/notify

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--allow-root"]
