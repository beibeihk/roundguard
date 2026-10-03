FROM python:3.11.5-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends latexmk texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils && rm -rf /var/lib/apt/lists/*
WORKDIR /roundguard
COPY . .
RUN pip install --no-cache-dir -e '.[reproduce]'
CMD ["python", "scripts/reproduce_all.py"]
