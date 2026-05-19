# MCP Server Demo

A demo MCP (Model Context Protocol) server built with FastMCP, using an Employee Leave Management system as the example.

---

## Prerequisites

- [uv](https://docs.astral.sh/uv/) — Python package and project manager

---

## Setup & Run

> **Cloning this repo?** Run `uv sync` first to install all dependencies from the lockfile, then skip to step 4.

### 1. Initialize the project

```bash
uv init
```

### 2. Add MCP dependency

```bash
uv add "mcp[cli]"
```

### 3. Check MCP CLI helper

```bash
uv run mcp
```

### 4. Run the MCP server

```bash
uv run --with mcp leave-management.py
```

The server will start at `http://localhost:8000`.

### 5. Inspect via MCP Inspector

```bash
npx @modelcontextprotocol/inspector http://localhost:8000
```

Open the inspector in your browser to explore and test all tools, resources, and prompts.

---

## MCP Concepts

### Tools

Tools are callable functions exposed by the MCP server. Clients (AI agents, VS Code Copilot, etc.) can invoke them directly.

**Example — `get_leave_balance`:**
```python
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """Get employee leave balance in chat-friendly format."""
    ...
```

Available tools in this demo:

| Tool | Description |
|---|---|
| `get_leave_balance` | Get remaining leave days for an employee |
| `get_leave_history` | Get past leave records for an employee |
| `apply_leave` | Submit a new leave application |
| `get_employee_info` | Get full employee profile |
| `health_check` | Check if the MCP server is running |

---

### Resources

Resources are static or dynamic data exposed by the MCP server as reference documents — readable by clients but not invokable like tools.

**Example — `policy://leave`:**
```python
@mcp.resource("policy://leave")
def get_leave_policy() -> str:
    """Returns the company leave policy as a static reference document."""
    ...
```

Available resources in this demo:

| Resource URI | Description |
|---|---|
| `policy://leave` | Company leave policy (entitlements, rules, application process) |

---

### Prompts

Prompts are reusable message templates that MCP clients use to pre-populate a conversation context. They are not invokable like tools — they are rendered by the client.

**Example — `leave_application_prompt`:**
```python
@mcp.prompt()
def leave_application_prompt(employee_id: str, leave_type: str) -> str:
    """Generate a leave application prompt for the user."""
    ...
```

Available prompts in this demo:

| Prompt | Parameters | Description |
|---|---|---|
| `leave_application_prompt` | `employee_id`, `leave_type` | Generates a guided prompt asking the user for leave details |

---

## Connect to VS Code Copilot Chat

You can connect this MCP server directly to VS Code so GitHub Copilot Chat can use its tools.

### 1. Run the server

```bash
uv run --with mcp leave-management.py
```

### 2. Create `.vscode/mcp.json`

```bash
mkdir -p .vscode && touch .vscode/mcp.json
```

### 3. Add the MCP server config

```json
{
  "servers": {
    "employee-leave": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

### 4. Start the MCP server from VS Code

Open `.vscode/mcp.json` in VS Code — a **Start** button will appear above the server entry. Click it to activate the connection.

### 5. Enable the tools in Copilot Chat

Open VS Code Chat (`Ctrl+Alt+I` / `Cmd+Alt+I`), click the **Tools** icon, and check **employee-leave** to enable its tools.

### 6. Chat with your MCP server

Copilot Chat now has context of your MCP server. You can ask things like:

> "Check my leave balance for EMP001"
> "Apply annual leave for EMP001 from 2026-06-01 to 2026-06-03, 3 days, reason: family trip"
