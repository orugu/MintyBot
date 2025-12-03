# 베이스 이미지
FROM python:3.11

# 필수 패키지 설치
RUN apt-get update && apt-get install -y curl build-essential

# 작업 디렉토리 설정
WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN export PATH="/mnt/highspeed_docker/Mintybot/bin:$PATH"
# 파이썬 패키지 설치
RUN pip install --upgrade pip setuptools wheel
RUN pip install \
    python-dotenv \
    torch==2.9.1 \
    torchvision==0.24.1 \
    torchaudio==2.9.1 \
    transformers==4.57.3 \
    tokenizers==0.22.1 \
    discord \
    asyncio \
    ffmpeg \
    gtts \
    keras \
    yt-dlp \
    pyglet \
    pynacl

RUN python -m pip install python-dotenv
RUN python -m pip install mariadb  

# 앱 소스 복사
COPY . .

# mintybot 사용자 생성 (권한 문제 방지)
RUN groupadd -r mintybot && useradd -r -g mintybot mintybot
USER mintybot

# 앱 실행
CMD ["python", "main.py"]
