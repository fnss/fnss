# Docker container for running FNSS
#
# Some useful commands:
#
# Build:        docker build [--build-arg py=<python-version>] -t fnss .
# Open shell:   docker run --rm -it fnss
#
ARG py=3.6
FROM python:${py}

COPY . /fnss
WORKDIR /fnss

RUN make install

CMD ["bash"]
