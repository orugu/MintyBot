FROM python:3.11.14
#FROM python:3.9
WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup default 1.68.2

COPY requirements.txt .
RUN pip install --no-cache-dir \
    --extra-index-url https://download.pytorch.org/whl/cu121 \
    -r requirements.txt

COPY . .

CMD ["python", "main.py"]
