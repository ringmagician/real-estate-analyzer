# Use Playwright's official image with dependencies installed
FROM mcr.microsoft.com/playwright/python:v1.39.0

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copy the backend code to the container
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port (5000)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
