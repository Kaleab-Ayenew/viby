# 🤖 Viby - AI Terminal Assistant

Viby is an AI-powered terminal assistant that helps you generate shell commands and get coding help directly from your terminal. Stop googling commands and start describing what you want to do!

## ✨ Features

- **🎯 Smart Command Generation**: Describe what you want to do, get the exact command
- **🧠 Context Awareness**: Record terminal sessions for better AI responses based on your current work
- **💬 Chat Mode**: Ask questions about errors, commands, or coding concepts
- **🔧 Shell Integration**: Seamless integration with bash/zsh
- **📹 Session Recording**: Capture terminal output for contextual help
- **⚡ Fast Setup**: One-command installation with automatic configuration

## 🚀 Quick Install

### One-Line Installation
```bash
curl -LsSf https://raw.githubusercontent.com/kaleab-ayenew/viby/main/install.sh | sh
```

### Manual Installation
If you prefer manual installation:

```bash
# Install via pipx (recommended)
pipx install viby

# Or via pip
pip install viby

# Install shell integration
viby install
```

## 📋 Requirements

- **Python**: 3.9 or higher
- **OpenAI API Key**: Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **OS**: Linux or macOS
- **Shell**: Bash or Zsh

## ⚙️ Configuration

### First-Time Setup

After installation, run the configuration command:

```bash
viby config
```

This will:
1. Prompt you for your OpenAI API key
2. Save it securely to `~/.config/viby/.env`
3. Verify the connection

### Manual Configuration

You can also set up the API key manually:

```bash
# Create config directory
mkdir -p ~/.config/viby

# Add your API key
echo "OPENAI_API_KEY=your_api_key_here" > ~/.config/viby/.env
```

### Environment Variable

Alternatively, export the API key in your shell:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Shell Integration

To enable recording and enhanced features:

```bash
viby install
source ~/.bashrc  # or restart your terminal
```

## 🎯 Usage

### Basic Commands

#### Generate Commands
```bash
# File operations
viby do "find all python files larger than 1MB"
viby do "compress all images in this directory"
viby do "delete files older than 30 days"

# System operations  
viby do "show disk usage by directory"
viby do "kill process using port 3000"
viby do "create a backup of this folder"

# Git operations
viby do "undo last commit but keep changes"
viby do "create new branch from current state"
viby do "show files changed in last commit"
```

#### Chat with AI
```bash
# Error explanations
viby chat "what does 'permission denied' mean?"
viby chat "explain this docker error message"

# Command explanations
viby chat "what does 'chmod 755' do?"
viby chat "difference between 'rm' and 'rm -rf'"

# Coding help
viby chat "how to debug python import errors"
viby chat "best practices for git branching"
```

### Advanced Usage with Context Recording

For the most powerful experience, use recording to give Viby context about your current work:

#### 1. Start Recording
```bash
viby record
```

You'll see a 🔴 indicator in your prompt showing you're recording.

#### 2. Work Normally
```bash
# Your normal workflow - all commands and output are captured
ls -la
cd my-project
python app.py
# Error occurs here...
```

#### 3. Get Contextual Help
```bash
# Viby sees the error and your project structure
viby do "fix this python import error"
viby chat "why did my script fail?"
viby do "install missing dependencies"
```

#### 4. Stop Recording
```bash
exit  # Stops recording and returns to normal terminal
```

### Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `viby do "<task>"` | Generate a shell command | `viby do "find large files"` |
| `viby chat "<question>"` | Ask AI a question | `viby chat "explain this error"` |
| `viby record` | Start recording session | `viby record` |
| `viby status` | Show recording status | `viby status` |
| `viby config` | Manage configuration | `viby config --reset` |
| `viby install` | Install shell integration | `viby install` |
| `viby help` | Show detailed help | `viby help` |

## 📖 Examples

### Real-World Scenarios

#### Scenario 1: Docker Troubleshooting
```bash
viby record
docker build -t myapp .
# Build fails with error...

viby do "fix this docker build error"
# Output: docker system prune -f && docker build --no-cache -t myapp .

viby chat "why did the build fail?"
# Explains the error and suggests improvements
```

#### Scenario 2: Git Workflow
```bash
viby do "create feature branch for user authentication"
# Output: git checkout -b feature/user-authentication

viby do "stage only python files"
# Output: git add *.py

viby chat "should I rebase or merge this feature branch?"
# Explains the differences and best practices
```

#### Scenario 3: System Administration
```bash
viby record
df -h
# Shows disk usage...

viby do "find what's using the most disk space"
# Output: du -sh */ | sort -rh | head -10

viby do "safely clean up log files older than 7 days"
# Output: find /var/log -name "*.log" -mtime +7 -exec rm {} \;
```

## 🔧 Configuration Options

### Config File Location
- `~/.config/viby/.env` (primary)
- `.env` in current directory (fallback)

### Available Settings
```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional (set via environment)
VIBY_MODEL=gpt-4.1-mini  # Default model
VIBY_LOG_LEVEL=INFO      # Logging level
```

### Shell Integration Features

When you run `viby install`, it adds these features to your shell:

- **🔴 Recording Indicator**: Visual prompt when recording
- **📁 Auto Log Management**: Logs stored in `~/.local/share/viby/logs/`
- **⚡ Context Commands**: `viby do` and `viby chat` automatically use session context
- **📊 Status Commands**: `viby status` shows current recording state

## 🛠️ Troubleshooting

### Common Issues

#### "OpenAI API key not found"
```bash
# Check configuration
viby config

# Or set environment variable
export OPENAI_API_KEY="your_key_here"
```

#### "Command not found: viby"
```bash
# Ensure ~/.local/bin is in PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or reinstall
curl -LsSf https://raw.githubusercontent.com/kaleab-ayenew/viby/main/install.sh | sh
```

#### "Shell integration not working"
```bash
# Reinstall shell integration
viby install
source ~/.bashrc

# Check if functions are loaded
type viby
```

#### "Recording not working"
```bash
# Check if script command is available
which script

# Install if missing (Ubuntu/Debian)
sudo apt install util-linux

# Install if missing (macOS)
# script is built-in on macOS
```

### Debug Mode

Enable verbose logging:
```bash
export VIBY_LOG_LEVEL=DEBUG
viby do "test command"
```

### Reset Configuration

```bash
# Reset all settings
viby config --reset

# Remove shell integration
# Edit ~/.bashrc and remove the "# Viby shell integration" section
```

## 🔒 Privacy & Security

- **API Key Storage**: Stored locally in `~/.config/viby/.env`
- **Terminal History**: Only sent when using `-f` flag or during recording
- **No Persistent Storage**: Viby doesn't store your commands or data
- **Local Processing**: All processing happens locally except OpenAI API calls

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/kaleab-ayenew/viby.git
cd viby

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black src/
ruff src/
```

### Building from Source

```bash
# Build package
python -m build

# Install locally
pip install dist/viby-*.whl
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [OpenAI API](https://openai.com/api/)
- Inspired by modern CLI tools like [uv](https://github.com/astral-sh/uv)
- Terminal recording powered by the `script` command

---

**Need help?** Open an issue on [GitHub](https://github.com/kaleab-ayenew/viby/issues) or run `viby help` for more information.
