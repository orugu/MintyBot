<h1>Attention!</h1>
<h2>MGPT2 will be disabled at rc versions.</h2>


You must add this context to .env file 

DISCORD_TOKEN=                      \#discord bot token
MGPT2_Enable="true"                 \#if "true", MGPT2 will be enabled

\#input MINTYRANK DB INFO
MINTYRANK_HOST=         
MINTYRANK_PORT=
MINTYRANK_USER=
MINTYRANK_PASSWORD=
MINTYRANK_DATABASE=

\#input MINTYBOT DB INFO
MINTYBOT_DB_HOST= 
MINTYBOT_DB_USER= 
MINTYBOT_DB_PASSWORD= 
MINTYBOT_DB_DATABASE=
MINTYBOT_DB_PORT=

\#input MINTYCURRENCY DB INFO
MINTYCURRENCY_DB_HOST=
MINTYCURRENCY_DB_USER=
MINTYCURRENCY_DB_PASSWORD=
MINTYCURRENCY_DB_DATABASE=
MINTYCURRENCY_DB_PORT=

※Patchnote v0.1.0
-각 기능 별 코드 정리 및 최적화
-MGPT2 최적화 및 fine tuning 완료
-tts 기능 실행 불가 버그 수정
-


※Patchnote v0.0.3
-MintyCurrency의 본격 개발 시작
-Command decorator 정리 시작 및 정리
-MintyHelp: !help 명령어를 통한 현재 사용 가능 명령어 정리
-initialize 등의 명령어를 통한 현재 사용 가능한 채널 특정 기능 추가
-MariaDB + SQLAlchemy 사용 시작

※Patchnote v0.0.2
-MintyRank 기능 추가
-MintyMusic refactoring
-MintyGPT2의 모델을 distilgpt2로 변경

※패치예정
관리자권한 확인 기능

