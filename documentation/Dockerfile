FROM python:3.8

EXPOSE 8000

COPY . .

RUN pip install -r requirements.txt
RUN mkdocs build

ENTRYPOINT ["mkdocs"]
CMD ["serve"]