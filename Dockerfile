# Use an official Python base image
FROM python:3.12.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port if needed (for Streamlit or Flask apps)
EXPOSE 8501

# Command to run the app (adjust as per your app's entry point)
CMD ["streamlit", "run", "app.py"]
