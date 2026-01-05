# Skill Seekers Web Interface

A user-friendly web interface for configuring and running Skill Seekers workflows.

## 🚀 Quick Start

### Installation

First, install Skill Seekers with web interface support:

```bash
# Install with web interface
pip install -e ".[web]"

# Or install all optional dependencies
pip install -e ".[all]"
```

### Starting the Web Interface

```bash
# Using the CLI command
skill-seekers-web

# Or using streamlit directly
streamlit run src/skill_seekers/webapp.py

# Or using Python module
python -m streamlit run src/skill_seekers/webapp.py
```

The web interface will automatically open in your browser at `http://localhost:8501`

## 📖 Features

### 1. 🏠 Home Page

Overview of the web interface with:
- Quick statistics (available configs, output projects, supported platforms)
- Feature descriptions
- Quick start guide

### 2. 📝 Configuration Generator

Create and manage configuration files without writing JSON manually.

**Features:**
- **Create New Config Tab:**
  - Fill in form fields to generate configuration
  - Basic information (name, description, base URL)
  - CSS selectors customization
  - URL patterns (include/exclude)
  - Categories configuration
  - Advanced settings (max pages, rate limit, timeout)

- **Manage Existing Configs Tab:**
  - View all existing configurations
  - Preview configuration JSON
  - Copy to clipboard
  - Delete configurations

**Example Workflow:**
1. Navigate to "Configuration Generator"
2. Fill in the form:
   - Configuration Name: `my-framework`
   - Description: `Framework for building modern web apps`
   - Base URL: `https://example.com/docs`
   - Selectors: Use defaults or customize
   - Include patterns: `/docs`, `/guides`
   - Exclude patterns: `/blog`, `/examples`
3. Click "🔧 Generate Configuration"
4. Configuration saved to `configs/my-framework.json`

### 3. 🌐 Documentation Scraper

Scrape documentation websites with a visual interface.

**Features:**
- Select existing configuration
- Choose scraper type (Documentation, GitHub, PDF, Unified)
- Enable/disable options:
  - Dry run mode
  - Async mode (faster scraping)
  - Skip scraping (rebuild only)
- View command before execution
- Real-time output display

**Example Workflow:**
1. Navigate to "Documentation Scraper"
2. Select configuration: `my-framework`
3. Choose "Documentation" scraper type
4. Options: Disable dry run for actual scraping
5. Click "🚀 Start Scraping"
6. Review the command
7. Click "⚡ Execute Command"

### 4. 📦 Skill Packager

Package scraped content into platform-specific formats.

**Features:**
- Browse output projects
- Preview SKILL.md content
- Select target platform:
  - Claude AI (.zip)
  - Google Gemini (.tar.gz)
  - OpenAI ChatGPT (.zip)
  - Generic Markdown (.zip)
- Dry run mode support

**Example Workflow:**
1. Navigate to "Skill Packager"
2. Select project: `my-framework`
3. Review SKILL.md preview
4. Choose target platform: `claude`
5. Disable dry run for actual packaging
6. Click "📦 Package Skill"
7. Click "⚡ Execute Packaging"

### 5. ☁️ Upload

Upload packaged skills to LLM platforms.

**Features:**
- List available packages (.zip, .tar.gz)
- Auto-detect platform from filename
- Secure API key input
- Platform-specific upload commands

**Example Workflow:**
1. Navigate to "Upload"
2. Select package: `my-framework-claude.zip`
3. Verify detected platform: CLAUDE
4. Enter API key (or set as environment variable)
5. Click "☁️ Upload Skill"
6. Click "⚡ Execute Upload"

**API Keys Setup:**

```bash
# Claude AI
export ANTHROPIC_API_KEY=sk-ant-...

# Google Gemini
export GOOGLE_API_KEY=AIza...

# OpenAI ChatGPT
export OPENAI_API_KEY=sk-...
```

### 6. 🔄 Complete Workflow

Automate the entire process from URL to uploaded skill.

**Features:**
- One-click automation
- Configuration selection
- Target platform selection
- Optional AI enhancement
- Complete workflow summary
- Dry run mode for testing

**Example Workflow:**
1. Navigate to "Complete Workflow"
2. Select configuration: `my-framework`
3. Choose target platform: `claude`
4. Enable AI enhancement (optional)
5. Disable dry run for actual execution
6. Click "🚀 Start Complete Workflow"
7. Click "⚡ Execute Workflow"

**Workflow Steps:**
1. 📝 Generate/create configuration
2. 🌐 Scrape documentation
3. 🤖 AI Enhancement (if enabled)
4. 📦 Package for target platform
5. ☁️ Upload to platform

## 🎨 UI Features

### Responsive Design
- Wide layout for better content display
- Mobile-friendly interface
- Collapsible sections for better organization

### User Experience
- Intuitive navigation with sidebar
- Real-time command preview
- Success/error notifications
- Progress indicators

### Data Visualization
- Configuration statistics
- Project metrics
- Platform information

## 🔧 Configuration

### Streamlit Configuration

Create `.streamlit/config.toml` in your project root:

```toml
[server]
port = 8501
headless = false
```

### Environment Variables

```bash
# Optional: Set default API keys
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=AIza...
export OPENAI_API_KEY=sk-...

# Optional: Set default rate limit
export SKILLSEEKERS_RATE_LIMIT=0.5
```

## 📝 Tips and Best Practices

### 1. Start with Dry Run
Always use dry run mode first to verify commands before actual execution.

### 2. Progressive Workflow
- Start small: Test with a few pages
- Verify output: Check SKILL.md quality
- Scale up: Increase max pages as needed

### 3. Configuration Management
- Use descriptive names for configurations
- Document your configuration choices
- Keep version control of configs

### 4. Error Handling
- Check command output for errors
- Verify file permissions
- Ensure sufficient disk space

### 5. Performance Optimization
- Enable async mode for faster scraping
- Adjust rate limit based on server capacity
- Use skip-scrape for rebuilding

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Use a different port
streamlit run src/skill_seekers/webapp.py --server.port 8502
```

### Command Not Found

```bash
# Reinstall the package
pip install -e ".[web]"

# Verify installation
which skill-seekers-web
```

### Import Errors

```bash
# Ensure you're in the project directory
cd /path/to/Skill_Seekers

# Install in editable mode
pip install -e ".[web]"
```

### Commands Failing

1. Check if CLI tools work independently
2. Verify configuration file format
3. Check file permissions
4. Review error messages in output

## 🚀 Advanced Usage

### Customizing the Web Interface

The web interface is built with Streamlit. You can modify `src/skill_seekers/webapp.py` to:

- Add new pages
- Customize UI elements
- Add new features
- Integrate with external services

### Running in Production

For production deployment:

```bash
# With authentication
streamlit run src/skill_seekers/webapp.py --server.enableCORS=false

# Behind proxy
streamlit run src/skill_seekers/webapp.py --server.enableXsrfProtection=false
```

See [Streamlit Deployment](https://docs.streamlit.io/deploy) for more options.

## 📚 Related Documentation

- [README.md](../README.md) - Main project documentation
- [BULLETPROOF_QUICKSTART.md](../BULLETPROOF_QUICKSTART.md) - Beginner guide
- [CLAUDE.md](../CLAUDE.md) - Developer documentation
- [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) - Common issues

## 🤝 Contributing

Contributions to the web interface are welcome! Please:

1. Test thoroughly in both dry run and live modes
2. Maintain consistent UI/UX patterns
3. Add error handling for user inputs
4. Document new features

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details
