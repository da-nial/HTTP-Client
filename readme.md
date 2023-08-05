# HTTP Client

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

This Python script serves as an HTTP request client and is the solution to the first practical assignment for the Internet Engineering course at Amirkabir University of Technology, Spring 2020.
The assignment instructions are described in the `instructions.pdf` file, in Persian.

The script allows users to send HTTP requests to specified URLs with various configurations. It supports common HTTP methods. The user can also define headers, query parameters, data, JSON payloads, and even upload files as part of their requests.

---

## Features

- Send HTTP requests using various methods (GET, POST, PUT, PATCH, DELETE).
- Configure request headers and query parameters.
- Include request data, JSON payloads, or upload files.
- Handle response headers and body, including content of different media types.
- Download and display HTML content, if applicable.
- Supports custom timeouts for requests.

## Usage

Follow these steps to use the HTTP Request Client:

1. **Clone the Repository:** Clone the repository containing this script to your local host.

2. **Navigate to the Script Directory:** Open a terminal and navigate to the directory where the script is located.

3. **Install Dependencies:** Ensure you have the required dependencies installed. You can use the following command to install them:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Script:** Use the following command to run the script and perform HTTP requests:

    ```bash
    python main.py [OPTIONS] URL
    ```

    - `URL`: The target URL to send the HTTP request to.

## Options

- `-M`, `--method`: Specify the HTTP method (GET, POST, PUT, PATCH, DELETE). Default is GET.
- `-H`, `--headers`: Specify headers for the request. You can use this option multiple times for multiple headers.
- `-Q`, `--queries`: Specify query parameters for the request. You can use this option multiple times for multiple query parameters.
- `-D`, `--data`: Include data for the request. Used for POST requests with `application/x-www-form-urlencoded` data.
- `--json`: Include JSON payload for the request.
- `--file`: Upload a file as part of the request.
- `--timeout`: Set a timeout for the request in seconds.

## Example

Here's an example command to run the script:

```bash
python main.py --method POST -H "Authorization: Bearer TOKEN" -D "username=alice&password=bob" URL
```

This command sends a POST request with custom headers and data to the specified URL.

## Course Information
- **Course**: Internet Engineering
- **University**: Amirkabir University of Technology  
- **Semester**: Spring 2020

Let me know if you have any questions!

