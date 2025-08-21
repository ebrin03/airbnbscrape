FROM alpine:latest

# Install Python
RUN apk add --no-cache python3 py3-pip

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the Flask application
CMD ["flask" , "--app", "app", "--host", "0.0.0.0", "run"]