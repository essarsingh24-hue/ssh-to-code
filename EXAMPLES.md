# SSH Directory Browser - Examples

## Example 1: Quick Connection

Connect to a server and browse from home directory:

## Example 10: Workflow Script

Create a custom script for your workflow:

```bash
#!/bin/bash
# deploy-browse.sh - Browse deployment directory

./ssh_dir_browser.py deploy@production.example.com \
    --start-path /var/www/myapp \
    -i ~/.ssh/deploy_key
```

## Example 11: Programmatic Usagedir_browser.py myuser@example.com
```

## Example 2: Connect with Custom Port

```bash
./ssh_dir_browser.py myuser@example.com -p 2222
```

## Example 3: Use Specific SSH Key

```bash
./ssh_dir_browser.py myuser@example.com -i ~/.ssh/my_custom_key
```

## Example 4: Start in Specific Directory

```bash
./ssh_dir_browser.py myuser@example.com --start-path /var/www/html
```

## Example 5: Password Authentication

```bash
./ssh_dir_browser.py myuser@example.com --password
```

## Example 6: Save Host Configuration

```python
#!/usr/bin/env python3
from config_manager import ConfigManager

config = ConfigManager()

# Add production server
config.add_host(
    name="prod-web",
    hostname="web.example.com",
    username="deploy",
    port=22,
    key_file="~/.ssh/production_key",
    default_path="/var/www/production"
)

# Add development server
config.add_host(
    name="dev-server",
    hostname="dev.example.com",
    username="developer",
    port=2222,
    key_file="~/.ssh/dev_key",
    default_path="/home/developer/projects"
)

# Add staging server
config.add_host(
    name="staging",
    hostname="staging.example.com",
    username="staging",
    port=22,
    default_path="/var/www/staging"
)

print("Hosts configured successfully!")
```

Save this as `setup_hosts.py` and run:
```bash
python3 setup_hosts.py
```

## Example 7: Use Host Selector

After configuring hosts, launch the interactive selector:

```bash
./host_selector.py
```

Use arrow keys to select a host and press Enter to connect.

## Example 8: Browse and Open in VS Code

1. Connect to server:
   ```bash
   ./ssh_dir_browser.py myuser@example.com
   ```

2. Navigate using arrow keys to your project directory

3. Press `n` to create a new folder if needed

4. Press `r` to refresh the directory listing

5. Press `o` to open in VS Code

6. VS Code will launch and connect via Remote-SSH

## Example 9: Create Project Structure

1. Connect to your server:
   ```bash
   ./ssh_dir_browser.py myuser@example.com --start-path /var/www
   ```

2. Press `n` to create a new project folder (e.g., "my-new-project")

3. Press `Enter` to navigate into the new folder

4. Press `o` to open it in VS Code

5. Start developing!

## Example 10: Workflow Script

Create a custom script for your workflow:

```bash
#!/bin/bash
# deploy-browse.sh - Browse deployment directory

./ssh_dir_browser.py deploy@production.example.com \
    --start-path /var/www/myapp \
    -i ~/.ssh/deploy_key
```

## Example 11: Programmatic Usage

```python
#!/usr/bin/env python3
from ssh_handler import SSHHandler
from ssh_dir_browser import DirectoryBrowser
import curses

def browse_server(hostname, username, start_path="/"):
    """Browse a remote server"""
    ssh = SSHHandler(hostname, username, port=22)
    
    if not ssh.connect():
        print(f"Failed to connect to {hostname}")
        return
    
    print(f"Connected to {hostname}")
    
    try:
        browser = DirectoryBrowser(ssh, start_path)
        curses.wrapper(browser.run)
    finally:
        ssh.disconnect()
        print("Disconnected")

if __name__ == "__main__":
    browse_server("example.com", "myuser", "/var/www")
```

## Example 12: Multiple Servers Setup

```python
#!/usr/bin/env python3
# setup_multiple_hosts.py
from config_manager import ConfigManager

config = ConfigManager()

servers = [
    {
        "name": "web1",
        "hostname": "web1.example.com",
        "username": "admin",
        "default_path": "/var/www"
    },
    {
        "name": "web2",
        "hostname": "web2.example.com",
        "username": "admin",
        "default_path": "/var/www"
    },
    {
        "name": "database",
        "hostname": "db.example.com",
        "username": "dbadmin",
        "default_path": "/var/lib/mysql"
    },
    {
        "name": "backup",
        "hostname": "backup.example.com",
        "username": "backup",
        "port": 2222,
        "default_path": "/backups"
    }
]

for server in servers:
    config.add_host(**server)
    print(f"Added: {server['name']}")

print(f"\nTotal hosts configured: {len(servers)}")
```

## Example 13: Add SSH Host to Config

```python
#!/usr/bin/env python3
from vscode_integration import VSCodeRemote

# Add host to ~/.ssh/config for easier VS Code access
success, message = VSCodeRemote.add_ssh_host_to_config(
    hostname="example.com",
    username="myuser",
    port=22,
    key_file="~/.ssh/id_rsa",
    alias="myserver"
)

print(message)

# Now you can use: ssh myserver
# Or in VS Code: Remote-SSH: Connect to Host → myserver
```

## Example 14: Check VS Code Setup

```bash
python3 vscode_integration.py
```

Output:
```
VS Code Remote Integration Test
==================================================
VS Code installed: True
Remote-SSH installed: True

Configured SSH hosts: 3
  - myserver
  - production
  - development
```

## Tips and Tricks

### Navigate Faster
- Press `h` to jump to home directory
- Press `r` to refresh the current directory
- Use `..` to go up one level

### Working with Multiple Sessions
1. Open directory in VS Code with `o`
2. Keep the terminal for browsing other directories
3. Open multiple VS Code windows for different projects

### SSH Key Management
```bash
# Generate new key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname

# Test connection
ssh -i ~/.ssh/id_ed25519 user@hostname
```

### Troubleshooting Connection
```bash
# Test SSH connection
ssh -v user@hostname

# Check SSH config
cat ~/.ssh/config

# List available keys
ssh-add -l
```
