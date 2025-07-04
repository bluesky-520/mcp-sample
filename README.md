# MCP Sample

A simple MCP (Model Context Protocol) sample with a client and server that demonstrates direct tool interaction without requiring any AI model or API keys.

## Overview

This sample includes:
- **Server**: A weather information server using the National Weather Service API
- **Client**: An interactive client that can connect to any MCP server and call tools directly

## Quick Start

### 1. Install Dependencies

Install both client and server dependencies:

```bash
# Install server dependencies
cd server
pip install -e .

# Install client dependencies  
cd ../client
pip install -e .
```

### 2. Run the Server

```bash
cd server
python weather.py
```

The server will start and wait for client connections.

### 3. Run the Client

In a new terminal:

```bash
cd client
python client.py ../server/weather.py
```

Or use the main entry point:

```bash
cd client
python main.py ../server/weather.py
```

## Features

### Server
- **get_alerts**: Get weather alerts for US states
- **get_forecast**: Get weather forecasts for specific coordinates
- Uses National Weather Service API (free, no API key required)

### Client
- Interactive menu system
- Automatic parameter prompting
- Tool discovery and listing
- No external API dependencies

## Example Usage

```
Connected to server with tools: ['get_alerts', 'get_forecast']

=== MCP Client Menu ===
1. List available tools
2. Call a tool
3. Quit

Enter your choice (1-3): 2

Available tools:
1. get_alerts
2. get_forecast

Enter tool number or name: 1

Calling tool: get_alerts
Description: Get weather alerts for a US state.

Parameter: state (string)
Description: Two-letter US state code (e.g. CA, NY)
(Required)
Enter value for state: CA

Result:
Event: Heat Advisory
Area: San Francisco Bay Area
Severity: Minor
Description: Heat index values up to 100 expected...
```

## Architecture

- **Transport**: stdio (standard input/output)
- **Protocol**: MCP (Model Context Protocol)
- **No AI Model Required**: Direct tool interaction
- **No API Keys**: Uses free public APIs

## Requirements

- Python 3.13+
- MCP Python SDK
- httpx (for server HTTP requests)

## Directory Structure

```
mcp-sample/
├── client/
│   ├── client.py      # Main client implementation
│   ├── main.py        # Entry point
│   ├── pyproject.toml # Client dependencies
│   └── README.md      # Client documentation
├── server/
│   ├── weather.py     # Weather server implementation
│   ├── pyproject.toml # Server dependencies
│   └── README.md      # Server documentation
└── README.md          # This file
```