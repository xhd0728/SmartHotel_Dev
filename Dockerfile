FROM python:3.8.8
WORKDIR /Smart_Hotel_DEV
ADD . .
RUN sed -i -re 's/(deb|security)\.debian\.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y gcc libpq-dev default-libmysqlclient-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ supervisor && \
    pip install --no-cache-dir --trusted-host mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ -r ./requirements.txt
EXPOSE 3000
ENTRYPOINT ["/bin/bash","-C","/code/start.sh"]
