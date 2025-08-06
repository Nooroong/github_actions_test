# 베이스 이미지
FROM python:3.10.14

MAINTAINER jiyeon <sjiyeon759@gmail.com>

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 작업 디렉토리 생성
WORKDIR /app

# 의존성 복사 및 설치
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 소스 복사
COPY . /app/

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# django 서버의 포트를 8000로 지정하였으므로 Docker의 컨테이너 또한 8000 포트를 열어준다.
EXPOSE 8000
