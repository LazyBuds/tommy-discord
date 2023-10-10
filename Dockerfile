FROM python:3

FROM gorialis/discord.py



RUN mkdir  /bot

WORKDIR /bot



COPY . .

RUN pip install -r requirements.txt

CMD [ "python3", "launcher.py" ]