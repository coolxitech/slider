FROM centos:7

RUN yum -y update && yum install -y epel-release
RUN yum -y install python3 python3-pip python3-devel make gcc gcc-c++ swig mesa-libGL.x86_64

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /app

CMD ["uvicorn", "main:app"]
