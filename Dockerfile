FROM python:3.9

WORKDIR /indexos

COPY ./commands/* /indexos/commands/
COPY ./core/* /indexos/core/
COPY ./DB/* /indexos/DB/
COPY ./help/* /indexos/help/
COPY ./token/* /indexos/token/
COPY ./core.py /indexos/
COPY ./requirements.txt /indexos/

RUN pip install --no-cache-dir --upgrade -r /indexos/requirements.txt

CMD ["python", "-u", "/indexos/core.py"]
