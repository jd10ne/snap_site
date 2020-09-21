FROM alpine:edge

# install chromium
RUN apk add --update chromium curl

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
COPY bootstrap.sh Pipfile Pipfile.lock ./
COPY snap_api ./snap_api

# install API dependencies
RUN pipenv install
## Webdriver
# ADD https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip ./snap_api/browser_driver

EXPOSE 5000
# CMD ping localhost
ENTRYPOINT ["/usr/src/app/bootstrap.sh"]