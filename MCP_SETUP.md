# 🚀 MCP Server Setup Guide for MeetingNotesAgent

## 📋 What You Need

To use the AI-powered automated meeting notes feature, you need to configure MCP (Model Context Protocol) servers in your Cursor IDE.

## 🛠️ Setup Steps

### 1. Create/Edit MCP Configuration File

Create or edit the file: `~/.cursor/mcp.json`

### 2. Add Required MCP Servers

```json
{
  "mcpServers": {
    "playwright": { 
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "mcp-atlassian": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e", "CONFLUENCE_URL",
        "-e", "CONFLUENCE_PERSONAL_TOKEN",
        "-e", "CONFLUENCE_SSL_VERIFY",
        "-e", "JIRA_URL",
        "-e", "JIRA_PERSONAL_TOKEN",
        "-e", "JIRA_SSL_VERIFY",
        "ghcr.io/sooperset/mcp-atlassian:latest"
      ],
      "env": {
        "CONFLUENCE_URL": "https://api.wiki.autodesk.com",
        "CONFLUENCE_PERSONAL_TOKEN": "YOUR_CONFLUENCE_TOKEN_HERE",
        "CONFLUENCE_SSL_VERIFY": "true",
        "JIRA_URL": "https://jira.autodesk.com",
        "JIRA_PERSONAL_TOKEN": "YOUR_JIRA_TOKEN_HERE",
        "JIRA_SSL_VERIFY": "true"
      }
    }
  }
}
```

### 3. Get Your Tokens

#### Confluence Token
1. Go to your Confluence instance
2. Click on your profile picture → Settings
3. Go to Personal Access Tokens
4. Create a new token with appropriate permissions

#### Jira Token (Optional)
1. Go to your Jira instance
2. Click on your profile picture → Profile
3. Go to Security → Create API token
4. Copy the token

### 4. Install Dependencies

#### Node.js (for Playwright MCP)
```bash
# Install Node.js if you haven't already
brew install node  # macOS
# or download from https://nodejs.org/
```

#### Docker (for Confluence/Jira MCP)
```bash
# Install Docker Desktop
# Download from https://www.docker.com/products/docker-desktop/
```

### 5. Test Your Setup

1. **Restart Cursor** after making MCP configuration changes
2. **Test Playwright**: Try opening a webpage
3. **Test Confluence**: Try creating a simple page

## 🔧 Troubleshooting

### Common Issues

#### Playwright MCP Not Working
```bash
# Install Playwright browsers
npx playwright install

# Check if npx is available
which npx
```

#### Docker MCP Not Working
```bash
# Check Docker is running
docker --version
docker ps

# Test Docker container
docker run --rm hello-world
```

#### Permission Issues
```bash
# Check file permissions
ls -la ~/.cursor/mcp.json

# Ensure proper ownership
chown $USER ~/.cursor/mcp.json
```

### Debug Mode

Enable verbose logging in Cursor:
1. Open Command Palette (Cmd/Ctrl + Shift + P)
2. Search for "MCP"
3. Look for any error messages

## 📚 Additional Resources

- **MCP Documentation**: https://modelcontextprotocol.io/
- **Playwright MCP**: https://github.com/playwright-ai/playwright-mcp
- **Confluence MCP**: https://github.com/sooperset/mcp-atlassian
- **Cursor MCP Setup**: https://cursor.sh/docs/mcp

## 🎯 Next Steps

Once your MCP servers are configured:

1. **Test the workflow** with a simple Zoom URL
2. **Customize templates** for your meeting types
3. **Share with your team** the new capabilities
4. **Provide feedback** for future enhancements

---

*Need help? Check the troubleshooting section or create an issue on GitHub!*
