# Use a lightweight Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project into the container
COPY . /app/

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Run the FastAPI app on port 8000 inside the container
CMD ["uvicorn", "Fastapi_Rover_Server:app", "--host", "0.0.0.0", "--port", "80"]
