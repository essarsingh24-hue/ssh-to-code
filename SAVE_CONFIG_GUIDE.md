# 💾 Saving Frequently Used SSH Configurations

## Quick Answer

Save your SSH connection so you can connect with just a nickname instead of typing the full connection details every time!

**Before** (typing everything):
```bash
./ssh-browse ubuntu@ec2-12-34-56-78.compute.amazonaws.com -i "~/.ssh/my-aws-key.pem" --start-path /home/ubuntu
```

**After** (just the nickname):
```bash
./ssh-browse my-aws-server
```

---

## 🚀 Quick Start - 3 Ways to Save

### Method 1: Interactive Mode (Easiest)
```bash
python save_config.py add
```

Follow the prompts:
```
Enter the SSH connection details:

Host nickname (e.g., 'my-ec2', 'production'): myserver
Hostname or IP (e.g., 'example.com', '1.2.3.4'): example.com
Username (e.g., 'ubuntu', 'ec2-user', 'root'): ubuntu
Port (default: 22): 22
Path to SSH key file (optional, press Enter to skip): ~/.ssh/my-key.pem
Default starting directory (optional, press Enter to skip): /var/www

✅ Configuration 'myserver' saved successfully!

You can now connect with:
  ./ssh-browse myserver
```

### Method 2: Quick Command Line
```bash
python save_config.py quick myserver ubuntu@example.com -i ~/.ssh/key.pem --path /var/www
```

### Method 3: Python Script
```python
from config_manager import ConfigManager

config = ConfigManager()
config.add_host(
    name='myserver',
    hostname='example.com',
    username='ubuntu',
    port=22,
    key_file='~/.ssh/my-key.pem',
    default_path='/var/www'
)
```

---

## 📋 Real Examples

### Example 1: AWS EC2 Instance

```bash
# Save your AWS EC2 instance:
python save_config.py quick my-aws-ec2 ubuntu@ec2-12-34-56-78.amazonaws.com -i ~/.ssh/my-aws-key.pem --path /home/ubuntu

# Connect with just:
./ssh-browse my-aws-ec2
```

### Example 2: Save Another AWS EC2
```bash
python save_config.py quick production ubuntu@ec2-12-34-56-78.amazonaws.com -i ~/Downloads/prod-key.pem --path /var/www/production
```

### Example 3: DigitalOcean Droplet
```bash
python save_config.py add
# Then enter:
# Name: mydroplet
# Hostname: 159.65.123.45
# Username: root
# Port: 22
# Key: ~/.ssh/digitalocean_key
# Path: /var/www
```

### Example 4: Development Server
```bash
python save_config.py quick devserver developer@dev.company.com -p 2222 -i ~/.ssh/dev_key
```

### Example 5: Multiple Servers at Once
```python
# save_multiple_servers.py
from config_manager import ConfigManager

config = ConfigManager()

servers = [
    {
        'name': 'web1',
        'hostname': 'web1.example.com',
        'username': 'deploy',
        'key_file': '~/.ssh/web_key.pem'
    },
    {
        'name': 'web2',
        'hostname': 'web2.example.com',
        'username': 'deploy',
        'key_file': '~/.ssh/web_key.pem'
    },
    {
        'name': 'database',
        'hostname': 'db.example.com',
        'username': 'admin',
        'port': 2222,
        'key_file': '~/.ssh/db_key.pem',
        'default_path': '/var/lib/mysql'
    }
]

for server in servers:
    config.add_host(**server)
    print(f"✅ Saved: {server['name']}")
```

---

## 🛠️ Managing Your Configurations

### List All Saved Configs
```bash
python save_config.py list
```

Output:
```
Found 2 saved configuration(s):

1. my-aws-ec2
   Connection: ubuntu@ec2-12-34-56-78.compute.amazonaws.com:22
   Key file:   ~/.ssh/my-aws-key.pem
   Start path: /home/ubuntu

2. production
   Connection: deploy@prod.example.com:22
   Key file:   ~/.ssh/prod_key.pem
```

### Remove a Config
```bash
python save_config.py remove
# Then select the config to remove
```

### Edit Configuration File Directly
```bash
nano ~/.ssh-dir-browser.json
```

---

## 📂 Configuration File Format

Location: `~/.ssh-dir-browser.json`

```json
{
  "version": "1.0",
  "hosts": [
    {
      "name": "my-aws-ec2",
      "hostname": "ec2-12-34-56-78.compute.amazonaws.com",
      "username": "ubuntu",
      "port": 22,
      "key_file": "~/.ssh/my-aws-key.pem",
      "default_path": "/home/ubuntu"
    },
    {
      "name": "production",
      "hostname": "prod.example.com",
      "username": "deploy",
      "port": 22,
      "key_file": "~/.ssh/prod_key.pem",
      "default_path": "/var/www"
    }
  ],
  "preferences": {
    "default_start_path": "~",
    "save_last_path": true
  }
}
```

---

## 🎯 Using Saved Configurations

### Method 1: Direct Connection
```bash
./ssh-browse my-aws-server
```

### Method 2: Interactive Selector
```bash
python host_selector.py
```

Output:
```
SSH Directory Browser - Select Host

Select a host to connect (2 available)
↑/↓: Navigate | Enter: Connect | 'q': Quit

  my-aws-ec2            → ubuntu@ec2-12-34-56-78.compute.amazonaws.com:22
  production            → deploy@prod.example.com:22
```

Use arrow keys to select, press Enter to connect!

---

## 💡 Pro Tips

### 1. Use Descriptive Names
```bash
# Good names:
- my-aws-ec2
- production-web1
- staging-db
- dev-backend

# Avoid:
- server1
- test
- temp
```

### 2. Group Related Servers
```bash
prod-web1
prod-web2
prod-db
staging-web
staging-db
dev-server
```

### 3. Include Default Paths
Save time by setting where you usually work:
```bash
python save_config.py quick web1 user@host -i ~/key.pem --path /var/www/myapp
```

### 4. Backup Your Config
```bash
cp ~/.ssh-dir-browser.json ~/.ssh-dir-browser.json.backup
```

### 5. Share Config with Team (Edit for your machines)
```bash
# Export (remove sensitive paths first!)
cat ~/.ssh-dir-browser.json

# Share with team, they edit hostnames/paths for their setup
```

---

## 🔧 Command Reference

```bash
# Interactive mode
python save_config.py

# Add new host (interactive)
python save_config.py add

# Quick add from command line
python save_config.py quick <name> <user@host> [options]

# List all saved hosts
python save_config.py list

# Remove a host
python save_config.py remove

# Show help
python save_config.py help
```

---

## 📝 Complete Workflow Example

Let's save all your common servers:

### Step 1: Save Your Servers
```bash
# Add your AWS EC2
python save_config.py quick my-aws-ec2 ubuntu@ec2-12-34-56-78.amazonaws.com -i ~/.ssh/my-aws-key.pem --path /home/ubuntu

# Add staging server
python save_config.py add
# Name: staging
# Host: staging.example.com
# User: ubuntu
# Port: 22
# Key: ~/.ssh/staging_key.pem
# Path: /home/ubuntu/app

# Add production server
python save_config.py add
# Name: production
# Host: prod.example.com
# User: deploy
# Port: 22
# Key: ~/.ssh/prod_key.pem
# Path: /var/www/production
```

### Step 2: Verify They're Saved
```bash
python save_config.py list
```

### Step 3: Connect Easily
```bash
# Connect to any server by name
./ssh-browse my-aws-ec2
./ssh-browse staging
./ssh-browse production

# Or use the selector
python host_selector.py
```

### Step 4: Navigate and Open in VS Code
1. Browser starts in your default path
2. Navigate to desired directory (arrow keys)
3. Press `o` to open in VS Code
4. Done! 🎉

---

## 🎁 What You Can Do

You can save multiple servers with descriptive names:

Example saved configurations:
- **my-aws-ec2** - Your AWS EC2 instance
- **dev-server** - Development server
- **production** - Production server

Connect with:
```bash
./ssh-browse my-aws-ec2
./ssh-browse dev-server
./ssh-browse production
```

---

## 🆘 Troubleshooting

### "Host already exists"
```bash
python save_config.py remove
# Then add it again with correct details
```

### "Config file not found"
It will be created automatically when you add the first host.

### "Want to edit existing config"
```bash
# Option 1: Edit file directly
nano ~/.ssh-dir-browser.json

# Option 2: Remove and re-add
python save_config.py remove
python save_config.py add
```

### "Want to use same key for multiple servers"
No problem! Just specify the same key file for each:
```bash
python save_config.py quick web1 user@host1.com -i ~/.ssh/shared_key.pem
python save_config.py quick web2 user@host2.com -i ~/.ssh/shared_key.pem
python save_config.py quick web3 user@host3.com -i ~/.ssh/shared_key.pem
```

---

## 🎉 Summary

**You Asked:** "How to save frequently used config?"

**Answer:**
1. **Save** with: `python save_config.py add`
2. **List** with: `python save_config.py list`
3. **Connect** with: `./ssh-browse <name>`

**Quick Example:**
```bash
# Save your server
python save_config.py quick my-server user@example.com -i ~/.ssh/key.pem

# Connect easily
./ssh-browse my-server
```

No more typing long hostnames and key paths! 🚀
