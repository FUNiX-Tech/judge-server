GIT_TAG ?= master
TAG ?= latest

.PHONY: judge-tier3 funix

all: judge-tier3 funix

judge-tier3:
	cd tier3 && docker build --build-arg TAG="${GIT_TAG}" -t dmoj/judge-tier3 -t dmoj/judge-tier3:$(TAG) .

funix:
	cd funix && docker build --build-arg TAG="${GIT_TAG}" -t judge -t judge:$(TAG) .
