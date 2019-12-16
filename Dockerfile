FROM python:3.6

ARG model
ENV model=$model

RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get clean

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

ADD mlserver.py .
ADD $model .

EXPOSE 8000
CMD ["python3", "-u", "mlserver.py", "-l", "0.0.0.0", "-p", "8000"]