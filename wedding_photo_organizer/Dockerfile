FROM python:3.10

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy app files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit specific: prevent asking for email
ENV STREAMLIT_DISABLE_WELCOME_MESSAGE=true

# Expose port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
