FROM python:3.10.6-buster

ENV WORKING_DIR /user/app/TwitchHashtagBot
WORKDIR $WORKING_DIR

COPY requirements.txt ./

RUN pip install twitchio
RUN pip install requests

COPY files/ ./files/
COPY source/ ./source/

ENV PYTHONPATH "${PYTHONPATH}:/user/app/TwitchHashtagBot"

WORKDIR /user/app/TwitchHashtagBot/source/

CMD ["python", "-u", "main.py"]