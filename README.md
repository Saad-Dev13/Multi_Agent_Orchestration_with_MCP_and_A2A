# Multi Agent Orchestration with MCP and A2A

An early-stage project exploring multi-agent orchestration with the Model Context Protocol (MCP) and agent-to-agent style coordination.

The current focus is a local MCP server that connects to Claude Desktop and can run terminal commands in a controlled workspace.

## Project Status

**Status:** Early development  
**Phase:** Foundation setup and MCP integration  
**Current focus:** Claude Desktop connection, terminal tool behavior, and project tracking

## What This Project Is About

This repository is a practical experiment in combining:

- Model Context Protocol for tool integration
- Multi-agent orchestration ideas
- Local command execution through a custom MCP server
- Claude Desktop as the front-end interface for interacting with tools

The goal is to build a small but useful orchestration setup that can grow over time.

## Current Highlights

- MCP server created using FastMCP
- Claude Desktop config connected to the local server
- Terminal command execution tool being tested
- Working directory issues identified and fixed
- Project progress and fixes tracked in dedicated log files

## Project Structure

- `mcp/servers/terminal_server/terminal_server.py` - MCP server for running terminal commands
- `FIXES.md` - Detailed log of fixes, file changes, and reasoning
- `PROJECT_STATUS.md` - Progress tracker and GitHub push history
- `main.py` - Project entry point or placeholder script
- `pyproject.toml` - Python project configuration
- `uv.lock` - Locked dependency state for `uv`

## MCP Server Overview

The current MCP server exposes a terminal command tool that:

- accepts a command string
- runs it through `subprocess`
- returns command output or errors
- uses a stable default workspace on the Desktop

This was added so Claude Desktop can interact with local commands without relying on a fragile working directory.

## Setup

### 1. Create the virtual environment

```powershell
uv venv