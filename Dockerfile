FROM python:3.8

MAINTAINER selen "selenintech@hotmail.com"


COPY . /api
WORKDIR /api
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["api.py"]