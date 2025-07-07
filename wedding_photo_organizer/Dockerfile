# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install OS dependencies required by OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Copy app code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Disable Streamlit welcome message and telemetry
ENV STREAMLIT_DISABLE_WELCOME_MESSAGE=true
ENV STREAMLIT_TELEMETRY_EMAIL=""

# Expose Streamlit default port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.headless=true"]
