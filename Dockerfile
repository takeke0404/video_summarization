FROM python:3.6
ARG project_dir=/projects/
ADD src/requirements.txt  ${project_dir}
ADD src/list.txt ${project_dir}
WORKDIR ${project_dir}
RUN pip install -r requirements.txt && youtube-dl -a list.txt
