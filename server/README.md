# MCP Weather Server

A simple MCP server that provides weather information tools using the National Weather Service API.

## Features

- **get_alerts**: Get weather alerts for a US state
- **get_forecast**: Get weather forecast for a specific location (latitude/longitude)

## Installation

1. Install dependencies:
```bash
pip install -e .
```

## Usage

Run the server directly:

```bash
python weather.py
```

The server will start and listen for MCP client connections via stdio transport.

## Tools

### get_alerts

Get weather alerts for a US state.

**Parameters:**
- `state` (string, required): Two-letter US state code (e.g., CA, NY, TX)

**Example:**
```python
result = await session.call_tool("get_alerts", {"state": "CA"})
```

### get_forecast

Get weather forecast for a specific location.

**Parameters:**
- `latitude` (number, required): Latitude of the location
- `longitude` (number, required): Longitude of the location

**Example:**
```python
result = await session.call_tool("get_forecast", {
    "latitude": 37.7749,
    "longitude": -122.4194
})
```

## API Information

This server uses the National Weather Service (NWS) API:
- Base URL: https://api.weather.gov
- No API key required
- Free to use
- US locations only

## Requirements

- Python 3.13+
- MCP Python SDK
- httpx (for HTTP requests)
