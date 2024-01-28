FROM python:3.11-slim

# Устанавливаем необходимые системные зависимости, включая xvfb
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio \
    libglib2.0-0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Устанавливаем зависимости для Python
RUN pip install --no-cache-dir PyQt5

# Устанавливаем скрипт запуска, который будет использовать xvfb
CMD ["xvfb-run", "-a", "-s", "-screen 0 1024x768x24", "python", "main.py"]