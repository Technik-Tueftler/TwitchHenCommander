FROM python:3.11.4-buster

ENV WORKING_DIR /user/app/TwitchHenCommander
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

ENV PYTHONPATH "${PYTHONPATH}:/user/app/TwitchHenCommander"
ENV PYTHONPATH "${PYTHONPATH}:/user/app/TwitchHenCommander/source"

WORKDIR /user/app/TwitchHenCommander/source/

CMD ["python", "-u", "main.py"]