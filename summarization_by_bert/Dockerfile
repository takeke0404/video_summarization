FROM python:3
ARG project_dir=/summarization_by_bert/
COPY . ${project_dir}
WORKDIR ${project_dir}
RUN pip install --upgrade pip && pip install -r requirements.txt
