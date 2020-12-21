FROM python:3.6
ARG project_dir=/summarization_all/
COPY . ${project_dir}
WORKDIR ${project_dir}
RUN pip install --upgrade pip && pip install -r requirements.txt && apt update && apt-get install -y ffmpeg
