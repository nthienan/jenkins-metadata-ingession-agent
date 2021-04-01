FROM alpine:3.13.4

EXPOSE 5000
ENV JMIA_CONFIG_FILE=/ect/jmia/config.yaml

RUN apk --no-cache update && \
    apk --no-cache upgrade && \
    apk --no-cache add tzdata python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -rf /var/cache/apk/* && \
    rm -rf /root/.cache

WORKDIR /usr/app/jmia

COPY config.yaml /ect/jmia/config.yaml
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .

ENTRYPOINT ["python", "app.py"]
