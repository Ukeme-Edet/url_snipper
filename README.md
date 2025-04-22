# URL Snipper

URL Snipper is a FastAPI-based tool for creating, managing, and retrieving shortened URLs. It provides a simple and efficient way to handle URL shortening with additional features like batch processing and expiration dates.

## Features

-   Shorten URLs with unique keys
-   Retrieve original URLs using shortened keys
-   Delete shortened URLs
-   View all stored URLs
-   Built-in expiration for URLs (default: 8 weeks)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/url_snipper.git
cd url_snipper
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the FastAPI application:

```bash
uvicorn src.__init__:create_app --reload
```

Access the API documentation at `http://127.0.0.1:8000/docs`.

### API Endpoints

-   `GET /api/`: Root endpoint
-   `POST /api/shorten`: Create a shortened URL
-   `GET /api/expand/{snipper_id}`: Retrieve the original URL
-   `DELETE /api/delete/{snipper_id}`: Delete a shortened URL
-   `GET /api/all`: Retrieve all shortened URLs

### Example Request

To shorten a URL:

```bash
curl -X POST "http://127.0.0.1:8000/api/shorten" -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push to your branch.
4. Submit a pull request.

## License

This project is licensed under the MIT License.
