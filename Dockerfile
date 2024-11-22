# Build Phase: Use the AWS Lambda Python base image for building the Docker image
FROM public.ecr.aws/lambda/python@sha256:013e1e2a142f1e778b162e81c46eeb817474ec7f50720218496ca340d92033fa AS build

# Install dependencies, download Chrome and Chromedriver, and unzip them
RUN dnf install -y unzip atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/

# Runtime Phase: Use the AWS Lambda Python base image for runtime
FROM public.ecr.aws/lambda/python@sha256:013e1e2a142f1e778b162e81c46eeb817474ec7f50720218496ca340d92033fa

# Install runtime dependencies and selenium
RUN dnf install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm && \
    pip install selenium==4.26.1 pandas

# Copy Chrome and Chromedriver from the build phase and other packages
COPY --from=build /opt/chrome-linux64 /opt/chrome
COPY --from=build /opt/chromedriver-linux64 /opt/

# Copy the main Lambda handler code
COPY main.py ./

# Set the Lambda entry point
CMD [ "main.handler" ]
