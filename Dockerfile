FROM python:3.11.4-buster

ENV WORKING_DIR /user/app/TwitchHashtagBot
WORKDIR $WORKING_DIR

COPY requirements.txt ./

RUN pip install -r requirements.txt
RUN pip install twitchio
# RUN pip install sqlalchemy[asyncio] aiosqlite
# RUN pip install requests
# RUN pip install websockets
# RUN pip install python-dotenv

COPY files/ ./files/
COPY source/ ./source/

ENV PYTHONPATH "${PYTHONPATH}:/user/app/TwitchHashtagBot"

WORKDIR /user/app/TwitchHashtagBot/source/

CMD ["python", "-u", "main.py"]