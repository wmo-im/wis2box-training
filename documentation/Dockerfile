FROM python:3.8

EXPOSE 8000

COPY . .

RUN pip3 install -r requirements.txt
RUN mkdocs build

ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]
