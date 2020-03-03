FROM show0k/alpine-miniconda

USER root
RUN mkdir -p /output && mkdir -p /src

WORKDIR /
COPY . /cpip

# Copy binaries to /bin and /src
RUN cp /cpip/bin/cpip /bin/ \
    && chmod +x /bin/cpip \
    && cp -r /cpip/src/* /src/ \
    && chmod +x /src/cpip-clean \
    && chmod +x /src/cpip-pack

ENV OSTYPE linux-gnu

RUN conda update conda && conda update --all

WORKDIR /cpip

RUN conda env create

WORKDIR /

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Expect to find the environment.yml mounted to root:
CMD source activate cpip && cpip pack -n conda -f environment.yml -o /output -p . --force
