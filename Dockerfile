# Set the base image to Python 3.9
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the application will run on
EXPOSE 5000

# Set the command to run the application
HEALTHCHECK CMD curl --fail http://localhost:5000/_stcore/health
# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["LangChain_ChatPDF.py" ]
