FROM python:3.8
WORKDIR /home/Develop/homework4
COPY . .
RUN pip install -U pip
RUN pip install --no-cache-dir -r ./requirements.txt
ENTRYPOINT [ "pytest" ]
