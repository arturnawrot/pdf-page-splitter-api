# PDF Page Splitter API

The **PDF Page Splitter API** is a Python-based REST API designed to split PDF files into individual pages - each page in a seperate PDF file. Users can upload a PDF file via a URL, and the service will return links to the split PDF pages.

## Features
- Accepts a PDF file via a URL.
- Splits the PDF into individual pages.
- Returns URLs for the split pages.
- Simple and lightweight Docker-based deployment.

## Installation

```bash
git clone https://github.com/arturnawrot/pdf-page-splitter-api
docker build -t pdf_splitter .
docker run -p 80:80 pdf_splitter
```

## Testing

Run tests using `pytest` within the Docker container:
```bash
docker run -it --rm pdf_splitter pytest tests/
```

## Example Usage

### Using cURL
Send a POST request with the PDF URL:
```bash
curl -X POST http://127.0.0.1/split-pdf \
-H "Content-Type: application/json" \
-d '{
    "url": "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf"
}'
```
### Example Request
```bash
POST http://127.0.0.1/split-pdf
Content-Type: application/json

{
    "url": "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf"
}
```
### Example Response
```bash
200 OK
[
    "http://127.0.0.1/uploaded_files/9baab041-970c-44dd-8698-a35246040858.pdf",
    "http://127.0.0.1/uploaded_files/a8a0dcd8-3a79-410b-b9c2-d47e2287a465.pdf",
    "http://127.0.0.1/uploaded_files/c82aa4a7-7efc-4302-ba46-25379246e8d4.pdf"
]
```
Each link corresponds to one of the split PDF pages.

## License

This project is licensed under the MIT License.
