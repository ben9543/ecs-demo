# syntax=docker/dockerfile:1

FROM python:3.10.5-alpine3.16

RUN python -m pip install boto3 && python -m pip install requests 

WORKDIR /scripts

COPY . .

CMD python3 script_session.py && python3 script_session_process_images.py && python3 script_session_move_images.py  
