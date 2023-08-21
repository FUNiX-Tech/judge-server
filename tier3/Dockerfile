FROM dmoj/runtimes-tier3

RUN apt-get update && apt-get install -y wget curl gnupg

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Set the PATH environment variable to include ChromeDriver
ENV PATH="/usr/local/bin:${PATH}"

# set display port to avoid crash
ENV DISPLAY=:99

ARG TAG=master
RUN mkdir /judge /problems && cd /judge && \
	curl -L https://github.com/DMOJ/judge-server/archive/"${TAG}".tar.gz | tar -xz --strip-components=1 && \
	rm requirements.txt && \
	rm dmoj/cptbox/_cptbox.pyx 

COPY _cptbox.pyx /judge/dmoj/cptbox/_cptbox.pyx 
COPY requirements.txt /judge/requirements.txt
COPY HTML.py /judge/dmoj/executors/HTML.py
COPY chrome_driver.py /judge/dmoj/utils/chrome_driver.py
COPY css_parser.py /judge/dmoj/utils/css_parser.py

RUN cd /judge && \
	python3 -m venv --prompt=DMOJ /env && \
	/env/bin/pip3 install cython==0.29.32 && \
	/env/bin/pip3 install selenium && \
	/env/bin/pip3 install beautifulsoup4 && \
	/env/bin/pip3 install -e . && \
	/env/bin/python3 setup.py develop && \
	HOME=~judge . ~judge/.profile && \
	runuser -u judge -w PATH -- /env/bin/dmoj-autoconf -V > /judge-runtime-paths.yml && \
	echo '  crt_x86_in_lib32: true' >> /judge-runtime-paths.yml

ENTRYPOINT ["/usr/bin/tini", "--", "/judge/.docker/entry"]
