# MCP Client (Non-Claude)

A simple MCP client that directly interacts with MCP servers without requiring any AI model or API keys.

## Features

- Connect to any MCP server via stdio transport
- Interactive menu system for tool selection
- Automatic parameter prompting based on tool schemas
- No external API dependencies

## Installation

1. Install dependencies:
```bash
pip install -e .
```

## Usage

Run the client with a path to an MCP server script:

```bash
python client.py ../server/weather.py
```

Or use the main entry point:

```bash
python main.py ../server/weather.py
```

## Interactive Menu

The client provides an interactive menu with the following options:

1. **List available tools** - Shows all tools with descriptions and parameters
2. **Call a tool** - Select and call a specific tool with interactive parameter input
3. **Quit** - Exit the client

## Example Session

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

## Requirements

- Python 3.13+
- MCP Python SDK

