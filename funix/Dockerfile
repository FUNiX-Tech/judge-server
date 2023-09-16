FROM dmoj/runtimes-tier3

ARG TAG=master
RUN mkdir /judge /problems && cd /judge && \
    curl -L https://github.com/DMOJ/judge-server/archive/"${TAG}".tar.gz | tar -xz --strip-components=1 && \
    python3 -m venv --prompt=DMOJ /env && \
    /env/bin/pip3 install cython && \
    /env/bin/pip3 install -e . && \
    /env/bin/python3 setup.py develop && \
    HOME=~judge . ~judge/.profile && \
    runuser -u judge -w PATH -- /env/bin/dmoj-autoconf -V > /judge-runtime-paths.yml && \
    echo '  crt_x86_in_lib32: true' >> /judge-runtime-paths.yml

RUN apt-get update && apt-get install -y wget curl gnupg

###################################################################
############################## funix ##############################
###################################################################
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Set the PATH environment variable to include ChromeDriver
ENV PATH="/usr/local/bin:${PATH}"

# set display port to avoid crash
ENV DISPLAY=:99

# fix cptbox error due to cython version (probably)
RUN rm /judge/dmoj/cptbox/_cptbox.pyx
COPY _cptbox.pyx /judge/dmoj/cptbox/_cptbox.pyx 



RUN cd /judge && \
    python3 -m venv --prompt=DMOJ /env && \
    # selenium and bs4 for HTML problems
    /env/bin/pip3 install selenium && \
    /env/bin/pip3 install beautifulsoup4

# HTLM (fake) executor
COPY HTML.py /judge/dmoj/executors/HTML.py

# utils
COPY css_parser.py /judge/dmoj/utils
COPY chrome_driver.py /judge/dmoj/utils


ENTRYPOINT ["/usr/bin/tini", "--", "/judge/.docker/entry"]
