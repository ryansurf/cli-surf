
FROM python:3.12.3-slim

#this instruction specifies the "working directory" 
#or the path in the image where files will be copied and commands will be executed.
WORKDIR /app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY . .

# # Setup an app user so the container doesn't run as the root user
# RUN useradd app
# USER app

# Set the working directory for running the application
WORKDIR /app/src
EXPOSE 8000

# Command to run the Flask application
CMD ["python3", "server.py"]
