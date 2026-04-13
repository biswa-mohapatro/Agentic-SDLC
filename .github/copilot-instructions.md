# [Title] — Product Requirements Document

## Purpose
This document is the single source of truth for all agents building this project. It defines every requirement, constraint, configuration contract, data contract, and acceptance criterion. Agents must not deviate from what is specified here without re-reading this document first.

---

## MCP Integration Preferences

Toggle these settings per project. Agents read this section before using MCP tools.

### Jira
- **Integration**: enabled | disabled
- **Auto-transition tickets**: enabled | disabled — automatically move tickets through workflow (Backlog → TODO → In Progress → Test → Acceptance → Done)
- **Post progress comments**: enabled | disabled — agents post status updates as Jira comments after each SDLC phase
- **Create sub-tasks from plan**: enabled | disabled — Planner agent creates Jira sub-tasks for each implementation task

### Confluence
- **Integration**: enabled | disabled
- **Auto-publish docs on completion**: enabled | disabled — Docs Engineer publishes documentation to Confluence after Phase 6
- **Read existing docs for context**: enabled | disabled — agents read relevant Confluence pages during Discovery & Planning phases

> **Note**: MCP requires the Atlassian MCP server to be configured in `.vscode/mcp.json` with valid credentials. Set `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`, `CONFLUENCE_URL`, `CONFLUENCE_USERNAME`, `CONFLUENCE_API_TOKEN` as environment variables on your machine.

---

## Overview

---

## Non-Goals

---

## Project Structure



---

## Config Contract (`config.yaml`) [Optional but recommended]

The config file drives all runtime behaviour. Agents must not hard-code any value that appears here.

---

## Build Order for Agents

Agents must build in this order to respect dependencies: