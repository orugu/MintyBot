# 베이스 이미지
FROM python:3.11

# 필수 패키지 설치
RUN apt-get update && apt-get install -y curl build-essential pkg-config\
    libmariadb3 libmariadb-dev gcc g++ musl-dev

# 작업 디렉토리 설정 &&uv 설치
COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/
WORKDIR /app
RUN export PATH="/mnt/highspeed_docker/Mintybot/bin:$PATH"
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

# mintybot 사용자 생성 (권한 문제 방지)
RUN groupadd -r mintybot && useradd -r -g mintybot mintybot
USER mintybot

# 앱 실행
CMD ["python", "main.py"]
