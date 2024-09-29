FROM postgres:13.11-alpine AS base

ENV DB_HOST db
ENV DB_NAME dev
ENV DB_USERNAME dev
ENV DB_PASSWORD dev

COPY scripts/000-init.sh /docker-entrypoint-initdb.d/

ADD sql /tmp/sql/

FROM base as dev

ENV DB_NAME_TEST dev_test

COPY scripts/001-init-test.sh /docker-entrypoint-initdb.d/
