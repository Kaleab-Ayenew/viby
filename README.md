# 🤖 Vity - AI Terminal Assistant

Vity is an AI-powered terminal assistant that helps you generate shell commands and get coding help directly from your terminal. Stop googling commands and start describing what you want to do!

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
curl -LsSf https://raw.githubusercontent.com/kaleab-ayenew/vity/main/install.sh | sh
```

### Manual Installation
If you prefer manual installation:

```bash
# Install via pipx (recommended)
pipx install vity

# Or via pip
pip install vity

# Install shell integration
vity install
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
vity config
```

This will:
1. Prompt you for your OpenAI API key
2. Save it securely to `~/.config/vity/.env`
3. Verify the connection

### Manual Configuration

You can also set up the API key manually:

```bash
# Create config directory
mkdir -p ~/.config/vity

# Add your API key
echo "OPENAI_API_KEY=your_api_key_here" > ~/.config/vity/.env
```

### Environment Variable

Alternatively, export the API key in your shell:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Shell Integration

To enable recording and enhanced features:

```bash
vity install
source ~/.bashrc  # or restart your terminal
```

## 🎯 Usage

### Basic Commands

#### Generate Commands
```bash
# File operations
vity do "find all python files larger than 1MB"
vity do "compress all images in this directory"
vity do "delete files older than 30 days"

# System operations  
vity do "show disk usage by directory"
vity do "kill process using port 3000"
vity do "create a backup of this folder"

# Git operations
vity do "undo last commit but keep changes"
vity do "create new branch from current state"
vity do "show files changed in last commit"
```

#### Chat with AI
```bash
# Error explanations
vity chat "what does 'permission denied' mean?"
vity chat "explain this docker error message"

# Command explanations
vity chat "what does 'chmod 755' do?"
vity chat "difference between 'rm' and 'rm -rf'"

# Coding help
vity chat "how to debug python import errors"
vity chat "best practices for git branching"
```

### Advanced Usage with Context Recording

For the most powerful experience, use recording to give Vity context about your current work:

#### 1. Start Recording
```bash
vity record
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
# Vity sees the error and your project structure
vity do "fix this python import error"
vity chat "why did my script fail?"
vity do "install missing dependencies"
```

#### 4. Stop Recording
```bash
exit  # Stops recording and returns to normal terminal
```

### Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `vity do "<task>"` | Generate a shell command | `vity do "find large files"` |
| `vity chat "<question>"` | Ask AI a question | `vity chat "explain this error"` |
| `vity record` | Start recording session | `vity record` |
| `vity status` | Show recording status | `vity status` |
| `vity config` | Manage configuration | `vity config --reset` |
| `vity install` | Install shell integration | `vity install` |
| `vity help` | Show detailed help | `vity help` |

## 📖 Examples

### Real-World Scenarios

#### Scenario 1: Docker Troubleshooting
```bash
vity record
docker build -t myapp .
# Build fails with error...

vity do "fix this docker build error"
# Output: docker system prune -f && docker build --no-cache -t myapp .

vity chat "why did the build fail?"
# Explains the error and suggests improvements
```

#### Scenario 2: Git Workflow
```bash
vity do "create feature branch for user authentication"
# Output: git checkout -b feature/user-authentication

vity do "stage only python files"
# Output: git add *.py

vity chat "should I rebase or merge this feature branch?"
# Explains the differences and best practices
```

#### Scenario 3: System Administration
```bash
vity record
df -h
# Shows disk usage...

vity do "find what's using the most disk space"
# Output: du -sh */ | sort -rh | head -10

vity do "safely clean up log files older than 7 days"
# Output: find /var/log -name "*.log" -mtime +7 -exec rm {} \;
```

## 🔧 Configuration Options

### Config File Location
- `~/.config/vity/.env` (primary)
- `.env` in current directory (fallback)

### Available Settings
```bash
# Required
OPENAI_API_KEY=your_api_key_here

# Optional (set via environment)
VITY_MODEL=gpt-4.1-mini  # Default model
VITY_LOG_LEVEL=INFO      # Logging level
```

### Shell Integration Features

When you run `vity install`, it adds these features to your shell:

- **🔴 Recording Indicator**: Visual prompt when recording
- **📁 Auto Log Management**: Logs stored in `~/.local/share/vity/logs/`
- **⚡ Context Commands**: `vity do` and `vity chat` automatically use session context
- **📊 Status Commands**: `vity status` shows current recording state

## 🛠️ Troubleshooting

### Common Issues

#### "OpenAI API key not found"
```bash
# Check configuration
vity config

# Or set environment variable
export OPENAI_API_KEY="your_key_here"
```

#### "Command not found: vity"
```bash
# Ensure ~/.local/bin is in PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Or reinstall
curl -LsSf https://raw.githubusercontent.com/kaleab-ayenew/vity/main/install.sh | sh
```

#### "Shell integration not working"
```bash
# Reinstall shell integration
vity install
source ~/.bashrc

# Check if functions are loaded
type vity
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
export VITY_LOG_LEVEL=DEBUG
vity do "test command"
```

### Reset Configuration

```bash
# Reset all settings
vity config --reset

# Remove shell integration
# Edit ~/.bashrc and remove the "# Vity shell integration" section
```

## 🔒 Privacy & Security

- **API Key Storage**: Stored locally in `~/.config/vity/.env`
- **Terminal History**: Only sent when using `-f` flag or during recording
- **No Persistent Storage**: Vity doesn't store your commands or data
- **Local Processing**: All processing happens locally except OpenAI API calls

## 🤝 Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/kaleab-ayenew/vity.git
cd vity

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
pip install dist/vity-*.whl
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [OpenAI API](https://openai.com/api/)
- Inspired by modern CLI tools like [uv](https://github.com/astral-sh/uv)
- Terminal recording powered by the `script` command

---

**Need help?** Open an issue on [GitHub](https://github.com/kaleab-ayenew/vity/issues) or run `vity help` for more details.
