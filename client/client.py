import asyncio
import os
import sys
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()
        self.available_tools = []

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        
        await self.session.initialize()
        
        # List available tools
        if self.session:
            response = await self.session.list_tools()
            self.available_tools = response.tools
            print("\nConnected to server with tools:", [tool.name for tool in self.available_tools])

    def display_available_tools(self):
        """Display all available tools with their descriptions"""
        print("\n=== Available Tools ===")
        for i, tool in enumerate(self.available_tools, 1):
            print(f"{i}. {tool.name}")
            if tool.description:
                print(f"   Description: {tool.description}")
            if tool.inputSchema:
                print(f"   Parameters: {tool.inputSchema}")
            print()

    def get_tool_by_name(self, tool_name: str):
        """Get a tool by name"""
        for tool in self.available_tools:
            if tool.name == tool_name:
                return tool
        return None

    async def call_tool_interactive(self, tool_name: str) -> str:
        """Call a tool interactively, prompting for parameters"""
        tool = self.get_tool_by_name(tool_name)
        if not tool:
            return f"Error: Tool '{tool_name}' not found"
        
        print(f"\nCalling tool: {tool_name}")
        if tool.description:
            print(f"Description: {tool.description}")
        
        # Collect parameters interactively
        args = {}
        if tool.inputSchema and tool.inputSchema.get("properties"):
            properties = tool.inputSchema["properties"]
            required = tool.inputSchema.get("required", [])
            
            for param_name, param_info in properties.items():
                param_type = param_info.get("type", "string")
                param_desc = param_info.get("description", "")
                is_required = param_name in required
                
                print(f"\nParameter: {param_name} ({param_type})")
                if param_desc:
                    print(f"Description: {param_desc}")
                if is_required:
                    print("(Required)")
                
                while True:
                    value = input(f"Enter value for {param_name}: ").strip()
                    if not value and is_required:
                        print("This parameter is required!")
                        continue
                    
                    # Convert value based on type
                    try:
                        if param_type == "number" or param_type == "integer":
                            if value:
                                args[param_name] = float(value) if param_type == "number" else int(value)
                            else:
                                args[param_name] = None
                        elif param_type == "boolean":
                            if value.lower() in ["true", "1", "yes"]:
                                args[param_name] = True
                            elif value.lower() in ["false", "0", "no"]:
                                args[param_name] = False
                            else:
                                args[param_name] = None
                        else:
                            args[param_name] = value if value else None
                        break
                    except ValueError:
                        print(f"Invalid {param_type} value. Please try again.")
        
        # Call the tool
        try:
            result = await self.session.call_tool(tool_name, args)
            return result.content
        except Exception as e:
            return f"Error calling tool: {str(e)}"

    async def interactive_menu(self):
        """Run an interactive menu for tool selection"""
        print("\n=== MCP Client Menu ===")
        print("1. List available tools")
        print("2. Call a tool")
        print("3. Quit")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                
                if choice == "1":
                    self.display_available_tools()
                elif choice == "2":
                    if not self.available_tools:
                        print("No tools available. Please connect to a server first.")
                        continue
                    
                    print("\nAvailable tools:")
                    for i, tool in enumerate(self.available_tools, 1):
                        print(f"{i}. {tool.name}")
                    
                    tool_choice = input("\nEnter tool number or name: ").strip()
                    
                    # Try to parse as number first
                    try:
                        tool_index = int(tool_choice) - 1
                        if 0 <= tool_index < len(self.available_tools):
                            tool_name = self.available_tools[tool_index].name
                        else:
                            print("Invalid tool number!")
                            continue
                    except ValueError:
                        # Treat as tool name
                        tool_name = tool_choice
                    
                    result = await self.call_tool_interactive(tool_name)
                    print(f"\nResult:\n{result}")
                    
                elif choice == "3":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.interactive_menu()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())