
FROM python:3.8

EXPOSE 8000

COPY ../../content /mkdocs

WORKDIR /mkdocs

RUN pip install -r requirements.txt
RUN mkdocs builds

ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]