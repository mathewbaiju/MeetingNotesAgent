# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a **documentation-only repository** — there is no application code to build, run, or test. It serves as a guide and template collection for an AI-powered workflow that converts Zoom meeting recordings into structured meeting notes using MCP servers.

The actual automation runs interactively inside Cursor IDE (or Claude Code) with two MCP servers configured: Playwright (browser automation to download Zoom transcripts) and Confluence (wiki page creation).

## Repository Structure

- `README.md` — Full workflow guide including the prompt template, MCP configuration JSON, and meeting note section templates
- `Temp Files/` — Working directory where downloaded Zoom transcripts (.vtt files) are placed before processing
- `output/` — Generated meeting notes and data exports (markdown, CSV, txt)
- `requirements.txt` — Reference only; no Python runtime is needed

## Core Workflow

The three-step prompt used to trigger the automated workflow:

1. Use **Playwright MCP** to download the audio transcript (.vtt) from a Zoom recording URL into `Temp Files/`
2. Summarize transcript into structured meeting notes (Attendees, Date, Discussion Points, Action Items, Recording URL)
3. Create a new wiki page in Confluence personal space via **Confluence MCP**

## MCP Server Configuration

Configured in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "mcp-atlassian": {
      "command": "docker",
      "args": ["run", "--rm", "-i", "-e", "CONFLUENCE_URL", "-e", "CONFLUENCE_PERSONAL_TOKEN", "ghcr.io/sooperset/mcp-atlassian:latest"],
      "env": {
        "CONFLUENCE_URL": "YOUR_CONFLUENCE_URL",
        "CONFLUENCE_PERSONAL_TOKEN": "YOUR_TOKEN"
      }
    }
  }
}
```

## Meeting Notes Format

All generated notes follow the same structure seen in `Meeting_Notes_2025-11-21.md` and `Temp Files/meeting_notes.md`:

- **Date / Attendees** (names and roles)
- **Discussion Points** (numbered topics with sub-bullets)
- **Action Items** (owner + task + deadline)
- **Key Decisions** (checkmarked decisions)
- **Next Steps / Next Meeting**
- **Recording** section with original Zoom URL

## Contributing

Work in this repo is primarily updating documentation, prompt templates in `README.md`, and adding example outputs to `output/` or `Temp Files/`. There are no build steps, linters, or test suites.
