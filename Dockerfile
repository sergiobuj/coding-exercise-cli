FROM python:3.7.15-slim

RUN useradd --create-home --shell /bin/bash swrelogs
WORKDIR /home/swrelogs
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
USER swrelogs

COPY . .

ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
