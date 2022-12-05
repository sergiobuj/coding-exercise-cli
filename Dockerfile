FROM python:3.10-slim

RUN useradd --create-home --shell /bin/bash swrelogs
WORKDIR /home/swrelogs
COPY requirements.txt ./

USER swrelogs
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
