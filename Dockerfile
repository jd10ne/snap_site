FROM alpine:edge

# install chromium
RUN apk add --update build-base chromium curl libffi-dev python3-dev

# install fonts
RUN mkdir /noto
ADD ./cache/NotoSansCJKjp-hinted.zip /noto
WORKDIR /noto
RUN unzip NotoSansCJKjp-hinted.zip && \
    mkdir -p /usr/share/fonts/noto && \
    cp *.otf /usr/share/fonts/noto && \
    chmod 644 -R /usr/share/fonts/noto/ && \
    fc-cache -fv
WORKDIR /
RUN rm -rf /noto

# install python environment
RUN apk add --update python3
ADD https://bootstrap.pypa.io/get-pip.py /tmp
RUN python3 /tmp/get-pip.py

RUN pip install --no-cache-dir pipenv

# Enable Local Venv Directory
ENV PIPENV_VENV_IN_PROJECT=1

# deploy application
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY snap_api ./
RUN rm -rf .venv

# install API dependencies
RUN pipenv install


ENV PORT=8080
EXPOSE $PORT

CMD ["/usr/src/app/bootstrap.sh"]
