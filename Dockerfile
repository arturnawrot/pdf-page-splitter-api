FROM python:3.8-slim

WORKDIR /pdf_splitter

# Copy everything first
COPY . /pdf_splitter

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# Default command
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]