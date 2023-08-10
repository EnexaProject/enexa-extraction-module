FROM  python:3.9.6


# get list of installable packets and install wget
RUN apt-get update && \
    apt-get -y install \
		'vim'


COPY data/ /opt/enexa/data/ 
COPY KGs/ /opt/enexa/KGs/
COPY scripts/ /opt/enexa/scripts/

COPY README.md requirements.txt requirements_coref.txt /opt/enexa/

RUN python3 -m venv /opt/enexa/venv/
RUN /bin/bash -c "source /opt/enexa/venv/bin/activate && python3 -m pip install --upgrade pip wheel setuptools && python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r /opt/enexa/requirements.txt"

RUN python3 -m venv /opt/enexa/venv_coref/
RUN /bin/bash -c "source /opt/enexa/venv_coref/bin/activate && python3 -m pip install --upgrade pip wheel setuptools && python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r /opt/enexa/requirements_coref.txt"
RUN /bin/bash -c "source /opt/enexa/venv_coref/bin/activate && python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org spacy==3.2.6"



WORKDIR /app
ADD module ./
ADD Makefile ./
CMD ./module

# Add ENEXA utils.
COPY --from=hub.cs.upb.de/enexa/images/enexa-utils:1 / /.
