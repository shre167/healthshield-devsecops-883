FROM python:3.12-slim

WORKDIR /app

# Update Debian packages to include available security fixes
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install application dependencies and remove pip from the runtime image
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip uninstall -y pip \
    && useradd --create-home --uid 10001 appuser

COPY app.py .

USER 10001

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
