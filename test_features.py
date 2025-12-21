#!/usr/bin/env python3
"""
Feature Test Script
Demonstrates the new features: Create Folder and Refresh
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_features():
    """Print all available features"""
    print("=" * 60)
    print("SSH Directory Browser - Features")
    print("=" * 60)
    print()
    print("🚀 NAVIGATION")
    print("  ↑/↓         Navigate up and down through items")
    print("  Enter       Open selected directory")
    print("  h           Jump to home directory")
    print("  ..          Go to parent directory")
    print()
    print("📁 FILE OPERATIONS")
    print("  n           Create new folder (NEW!)")
    print("  r           Refresh directory listing")
    print()
    print("💻 VS CODE INTEGRATION")
    print("  o           Open current directory in VS Code")
    print()
    print("⚙️  OTHER")
    print("  q           Quit the application")
    print()
    print("=" * 60)
    print()
    print("NEW IN VERSION 1.1.0:")
    print("  ✨ Create folders directly from the browser (press 'n')")
    print("  ✨ Manual refresh to see external changes (press 'r')")
    print("  ✨ Improved help text and status messages")
    print()
    print("=" * 60)
    print()
    print("USAGE:")
    print("  ./ssh_dir_browser.py user@hostname")
    print("  ./ssh_dir_browser.py user@hostname -p 2222")
    print("  ./ssh_dir_browser.py user@hostname --start-path /var/www")
    print()
    print("INTERACTIVE MODE:")
    print("  1. Connect to your server")
    print("  2. Navigate to desired location")
    print("  3. Press 'n' to create a new folder")
    print("  4. Enter folder name and press Enter")
    print("  5. The directory refreshes automatically")
    print("  6. Navigate into the new folder and press 'o' to open in VS Code")
    print()

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from ssh_handler import SSHHandler
        print("  ✓ ssh_handler")
    except ImportError as e:
        print(f"  ✗ ssh_handler: {e}")
    
    try:
        from ssh_dir_browser import DirectoryBrowser
        print("  ✓ ssh_dir_browser")
    except ImportError as e:
        print(f"  ✗ ssh_dir_browser: {e}")
    
    try:
        from vscode_integration import VSCodeRemote
        print("  ✓ vscode_integration")
    except ImportError as e:
        print(f"  ✗ vscode_integration: {e}")
    
    try:
        from config_manager import ConfigManager
        print("  ✓ config_manager")
    except ImportError as e:
        print(f"  ✗ config_manager: {e}")
    
    try:
        from host_selector import HostSelector
        print("  ✓ host_selector")
    except ImportError as e:
        print(f"  ✗ host_selector: {e}")
    
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    try:
        import paramiko
        print(f"  ✓ paramiko {paramiko.__version__}")
    except ImportError:
        print("  ✗ paramiko (required)")
        print("    Install with: pip install paramiko")
    
    try:
        import curses
        print("  ✓ curses (built-in)")
    except ImportError:
        print("  ✗ curses (should be built-in)")
    
    print()

def check_vscode():
    """Check VS Code installation"""
    print("Checking VS Code...")
    
    import subprocess
    try:
        result = subprocess.run(['code', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"  ✓ VS Code CLI installed (version {version})")
            
            # Check Remote-SSH extension
            result = subprocess.run(['code', '--list-extensions'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=10)
            if 'ms-vscode-remote.remote-ssh' in result.stdout.lower():
                print("  ✓ Remote-SSH extension installed")
            else:
                print("  ✗ Remote-SSH extension not found")
                print("    Install with: code --install-extension ms-vscode-remote.remote-ssh")
        else:
            print("  ✗ VS Code CLI not accessible")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  ✗ VS Code CLI not found in PATH")
        print("    Make sure 'code' command is available")
    
    print()

if __name__ == "__main__":
    print()
    print_features()
    print()
    test_imports()
    check_dependencies()
    check_vscode()
    print()
    print("Ready to use! Connect with: ./ssh_dir_browser.py user@hostname")
    print()
