# Python 3.9
FROM python:3.9-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
COPY streamlit_app.py .
COPY model.pkl .
COPY scaler.pkl .
COPY features.pkl .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8501

# Run streamlit app
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
