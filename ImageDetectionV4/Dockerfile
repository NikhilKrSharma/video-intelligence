FROM python:3.11

WORKDIR /app

COPY . /app

# Set environment variables
ENV TERM=xterm
ENV PYTHONPATH="/app/TrackerModules:${PYTHONPATH}"

# Update pip and install system dependencies
RUN pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libglib2.0-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "Main.py"]