FROM python:3
ARG project_dir=/speech_segmentation/
COPY . ${project_dir}
WORKDIR ${project_dir}
RUN pip install -r requirements.txt && apt update && apt-get install -y ffmpeg
