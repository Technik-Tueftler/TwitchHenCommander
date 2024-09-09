FROM python:3.11.4-buster

ENV WORKING_DIR /user/app/TwitchHenCommander
WORKDIR $WORKING_DIR

COPY requirements.txt ./

RUN pip install -r requirements.txt
# RUN pip install twitchio

COPY files/ ./files/
COPY source/ ./source/

ENV PYTHONPATH "${PYTHONPATH}:/user/app/TwitchHenCommander"

WORKDIR /user/app/TwitchHenCommander/source/

CMD ["python", "-u", "main.py"]