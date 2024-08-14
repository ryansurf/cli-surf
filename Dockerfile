FROM python:3

#this instruction specifies the "working directory"
#or the path in the image where files will be copied and commands will be executed.
WORKDIR /app

# Copy in the source code
COPY . .

# Copy in the .env file
COPY .env.example .env

# Install the application dependencies
RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

# Set the working directory for running the application
EXPOSE 8000

# Command to run the Flask application
CMD ["poetry", "run", "python", "src/server.py"]
