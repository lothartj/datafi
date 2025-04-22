# Mobile Data Proxy

A simple Flask application that allows you to browse websites with a mobile user-agent, making them behave as if you're accessing them from a mobile data connection.

## Purpose

Some websites or web applications only work properly when accessed from a mobile data connection, either due to carrier-specific features or user-agent detection. This proxy allows you to access such sites from your WiFi connection by mimicking mobile data characteristics.

## Features

- Forwards requests to the target website with a mobile user-agent
- Maintains all original request parameters, cookies, and headers
- Simple web interface to configure the target URL
- Proxies all HTTP methods (GET, POST, PUT, DELETE, etc.)

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:

```
python app.py
```

2. Open your browser and navigate to http://localhost:5000
3. Enter the URL of the website you want to access (the one that only works on mobile data)
4. All requests through this proxy will now appear to come from a mobile device

## Configuration

You can optionally set a default target URL by creating a `.env` file with:

```
TARGET_URL=https://example.com
```

## Security Notice

This is a simple proxy for personal use. It doesn't include security features like HTTPS, authentication, or input validation. Do not expose this service to the public internet. 