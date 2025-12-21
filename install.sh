#!/bin/bash
# Installation script for SSH Directory Browser

set -e

echo "SSH Directory Browser - Installation"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || {
    echo "Error: Python 3 is required but not found"
    exit 1
}

# Check pip
echo "Checking pip..."
python3 -m pip --version || {
    echo "Error: pip is required but not found"
    exit 1
}

# create virtual environment (optional)
echo ""
read -p "Would you like to create a virtual environment for this project? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Activated virtual environment"
fi


# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check VS Code
echo ""
echo "Checking VS Code installation..."
if command -v code &> /dev/null; then
    echo "✓ VS Code CLI found"
    
    # Check Remote-SSH extension
    if code --list-extensions | grep -q "ms-vscode-remote.remote-ssh"; then
        echo "✓ Remote-SSH extension installed"
    else
        echo "⚠ Remote-SSH extension not found"
        echo "  Please install it from VS Code marketplace:"
        echo "  code --install-extension ms-vscode-remote.remote-ssh"
    fi
else
    echo "⚠ VS Code CLI not found"
    echo "  Make sure 'code' command is in your PATH"
    echo "  For macOS: Open VS Code → Cmd+Shift+P → 'Shell Command: Install code command in PATH'"
fi

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x ssh_dir_browser.py
chmod +x host_selector.py
chmod +x ssh_handler.py
chmod +x vscode_integration.py
chmod +x config_manager.py

# Optional: Create symlink
echo ""
echo "Installation complete!"
echo ""
echo "You can now use the tool with:"
echo "  ./ssh_dir_browser.py user@hostname"
echo ""
echo "Or select from saved hosts:"
echo "  ./host_selector.py"
echo ""
read -p "Would you like to add ssh_dir_browser to your PATH? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Detect shell
    if [[ "$SHELL" == *"zsh"* ]]; then
        SHELL_RC="$HOME/.zshrc"
    else
        SHELL_RC="$HOME/.bashrc"
    fi
    
    # Add to PATH
    echo "" >> "$SHELL_RC"
    echo "# SSH Directory Browser" >> "$SHELL_RC"
    echo "export PATH=\"\$PATH:$SCRIPT_DIR\"" >> "$SHELL_RC"
    
    echo "✓ Added to $SHELL_RC"
    echo "  Run 'source $SHELL_RC' or restart your terminal"
    echo "  Then you can use: ssh_dir_browser.py user@hostname"
fi

echo ""
echo "Setup complete! Happy browsing! 🚀"
