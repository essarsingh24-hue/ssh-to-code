# SSH Authentication Guide

## Handling Different Authentication Scenarios

This guide explains how to connect when you have different types of SSH keys and authentication methods.

---

## 📋 Table of Contents

1. [Encrypted PEM Files (Password-Protected Keys)](#encrypted-pem-files)
2. [Unencrypted PEM Files](#unencrypted-pem-files)
3. [No PEM File - Password Authentication](#password-authentication)
4. [Using SSH Agent](#using-ssh-agent)
5. [Troubleshooting](#troubleshooting)

---

## 🔐 Encrypted PEM Files (Password-Protected Keys)

### Scenario: You have a PEM file but it requires a passphrase

When you try to use an encrypted key, the tool will automatically detect it and prompt for the passphrase:

```bash
./ssh_dir_browser.py user@hostname -i ~/keys/my-encrypted-key.pem
```

**What happens:**
```
🔑 Using key file: /Users/you/keys/my-encrypted-key.pem
🔐 Key file is encrypted: /Users/you/keys/my-encrypted-key.pem
Enter passphrase for key (attempt 1/3): ********
✓ Key decrypted successfully
✓ Connected successfully!
```

### Features:
- ✅ Automatically detects encrypted keys
- ✅ Prompts for passphrase when needed
- ✅ Supports multiple key formats (RSA, Ed25519, ECDSA, DSS)
- ✅ 3 attempts to enter correct passphrase
- ✅ Falls back to password auth if key fails

---

## 🔓 Unencrypted PEM Files

### Scenario: You have a PEM file without password protection

Simply provide the path to your key file:

```bash
./ssh_dir_browser.py user@hostname -i ~/keys/my-key.pem
```

**What happens:**
```
🔑 Using key file: /Users/you/keys/my-key.pem
✓ Connected successfully!
```

### Common Locations:
```bash
# AWS EC2 key
./ssh_dir_browser.py ec2-user@example.com -i ~/Downloads/aws-key.pem

# Custom key in .ssh
./ssh_dir_browser.py user@server.com -i ~/.ssh/production_key

# Relative path
./ssh_dir_browser.py user@server.com -i ./keys/server.pem
```

---

## 🔑 Password Authentication

### Scenario: You don't have a PEM file, only username/password

Use the `--password` flag:

```bash
./ssh_dir_browser.py user@hostname --password
```

**What happens:**
```
Connecting to user@hostname:22...
Password for user@hostname: ********
✓ Connected successfully!
```

### Automatic Fallback:

Even if you specify a key, the tool will fall back to password auth if the key fails:

```bash
./ssh_dir_browser.py user@hostname -i ~/nonexistent.pem
```

**What happens:**
```
✗ Key file not found: /Users/you/nonexistent.pem

Options:
  1. Check the path to your PEM/key file
  2. Use password authentication with --password flag
  3. Use SSH agent authentication (ssh-add your key)

🔐 Key authentication not available. Trying password authentication...
Password for user@hostname: ********
✓ Connected successfully!
```

---

## 🎯 Using SSH Agent (Recommended!)

### Best Practice: Add your key to SSH agent

This is the most secure and convenient method:

### Step 1: Start SSH agent (usually already running)
```bash
eval "$(ssh-agent -s)"
```

### Step 2: Add your key to the agent

**For unencrypted keys:**
```bash
ssh-add ~/.ssh/id_rsa
# or
ssh-add ~/path/to/your-key.pem
```

**For encrypted keys:**
```bash
ssh-add ~/.ssh/id_rsa
# You'll be prompted for the passphrase ONCE
Enter passphrase for ~/.ssh/id_rsa: ********
Identity added: ~/.ssh/id_rsa
```

### Step 3: Verify keys are loaded
```bash
ssh-add -l
```

### Step 4: Connect WITHOUT specifying the key
```bash
./ssh_dir_browser.py user@hostname
```

The tool will automatically use keys from your SSH agent!

### Benefits:
- ✅ Enter passphrase only once
- ✅ More secure (keys stay in memory)
- ✅ Works with all SSH tools
- ✅ No need to specify `-i` flag

---

## 🔧 Troubleshooting

### Problem 1: "Key file is encrypted" but you don't know the passphrase

**Solutions:**

1. **Use password authentication instead:**
   ```bash
   ./ssh_dir_browser.py user@hostname --password
   ```

2. **Generate a new key pair:**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Don't set a passphrase, or use one you'll remember
   
   # Copy to server
   ssh-copy-id -i ~/.ssh/id_ed25519.pub user@hostname
   
   # Connect
   ./ssh_dir_browser.py user@hostname
   ```

3. **Ask server admin for new key:**
   - Request a new key file
   - Or ask to add your public key to the server

---

### Problem 2: "Permission denied (publickey)"

**Solutions:**

1. **Check key permissions:**
   ```bash
   chmod 600 ~/path/to/your-key.pem
   chmod 700 ~/.ssh
   ```

2. **Verify key is authorized on server:**
   ```bash
   # Your public key must be in server's ~/.ssh/authorized_keys
   # Test with verbose output:
   ssh -v -i ~/path/to/key.pem user@hostname
   ```

3. **Try password authentication:**
   ```bash
   ./ssh_dir_browser.py user@hostname --password
   ```

---

### Problem 3: "Key file not found"

**Solutions:**

1. **Check the path:**
   ```bash
   # Use absolute path
   ./ssh_dir_browser.py user@hostname -i /Users/you/keys/key.pem
   
   # Or expand ~
   ./ssh_dir_browser.py user@hostname -i ~/.ssh/id_rsa
   ```

2. **List your keys:**
   ```bash
   ls -la ~/.ssh/
   ls -la ~/Downloads/*.pem
   ```

3. **Use find command:**
   ```bash
   find ~ -name "*.pem" 2>/dev/null
   ```

---

### Problem 4: Multiple keys, not sure which one to use

**Solutions:**

1. **Let the tool try default keys:**
   ```bash
   # It will automatically try:
   # - ~/.ssh/id_rsa
   # - ~/.ssh/id_ed25519
   # - ~/.ssh/id_ecdsa
   ./ssh_dir_browser.py user@hostname
   ```

2. **Try each key manually:**
   ```bash
   ./ssh_dir_browser.py user@hostname -i ~/.ssh/id_rsa
   ./ssh_dir_browser.py user@hostname -i ~/.ssh/id_ed25519
   ./ssh_dir_browser.py user@hostname -i ~/Downloads/aws-key.pem
   ```

3. **Check your SSH config:**
   ```bash
   cat ~/.ssh/config
   # Look for entries matching your hostname
   ```

---

## 📚 Complete Examples

### Example 1: AWS EC2 Instance
```bash
# You downloaded key.pem from AWS
chmod 600 ~/Downloads/my-aws-key.pem
./ssh_dir_browser.py ec2-user@ec2-12-34-56-78.compute.amazonaws.com -i ~/Downloads/my-aws-key.pem
```

### Example 2: DigitalOcean Droplet (Password)
```bash
./ssh_dir_browser.py root@your-droplet-ip --password
```

### Example 3: Corporate Server (Encrypted Key)
```bash
./ssh_dir_browser.py employee@corp-server.company.com -i ~/.ssh/company_key
# Will prompt for passphrase
```

### Example 4: GitHub Codespaces / Dev Server
```bash
# Add key to agent first (do this once)
ssh-add ~/.ssh/id_ed25519

# Then connect without specifying key
./ssh_dir_browser.py user@dev-server.company.com
```

### Example 5: Multiple Servers with Different Keys
```bash
# Production (encrypted key)
./ssh_dir_browser.py deploy@prod.example.com -i ~/.ssh/prod_key

# Staging (password)
./ssh_dir_browser.py dev@staging.example.com --password

# Development (SSH agent)
ssh-add ~/.ssh/dev_key
./ssh_dir_browser.py developer@dev.example.com
```

---

## 🎓 Quick Reference

| Scenario | Command |
|----------|---------|
| Unencrypted key | `./ssh_dir_browser.py user@host -i ~/key.pem` |
| Encrypted key | `./ssh_dir_browser.py user@host -i ~/key.pem` (will prompt) |
| Password only | `./ssh_dir_browser.py user@host --password` |
| SSH agent | `ssh-add ~/key.pem && ./ssh_dir_browser.py user@host` |
| Default keys | `./ssh_dir_browser.py user@host` (auto-tries ~/.ssh/id_*) |
| Custom port | `./ssh_dir_browser.py user@host -p 2222 -i ~/key.pem` |

---

## 🔒 Security Best Practices

1. **Protect your keys:**
   ```bash
   chmod 600 ~/.ssh/id_rsa
   chmod 600 ~/path/to/any-key.pem
   chmod 700 ~/.ssh
   ```

2. **Use encrypted keys for sensitive servers:**
   ```bash
   # Generate with passphrase
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Enter a strong passphrase when prompted
   ```

3. **Use SSH agent to avoid re-entering passphrases:**
   ```bash
   ssh-add ~/.ssh/id_ed25519
   # Enter passphrase once, then forget about it
   ```

4. **Don't commit keys to git:**
   ```bash
   # Already in .gitignore but be careful!
   echo "*.pem" >> .gitignore
   echo "*.key" >> .gitignore
   ```

5. **Rotate keys regularly:**
   ```bash
   # Generate new key
   ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_new
   
   # Copy to servers
   ssh-copy-id -i ~/.ssh/id_ed25519_new.pub user@server
   
   # Test, then remove old key
   ```

---

## 💡 Pro Tips

1. **Test SSH connection first:**
   ```bash
   ssh -v user@hostname
   # If this works, the tool will work too
   ```

2. **Create SSH config for easier access:**
   ```bash
   # ~/.ssh/config
   Host myserver
       HostName example.com
       User myuser
       IdentityFile ~/.ssh/my_key.pem
       Port 22
   
   # Then just:
   ./ssh_dir_browser.py myserver
   ```

3. **List loaded keys in agent:**
   ```bash
   ssh-add -l
   # Shows fingerprints of all loaded keys
   
   ssh-add -L
   # Shows full public keys
   ```

4. **Remove keys from agent:**
   ```bash
   ssh-add -d ~/.ssh/id_rsa  # Remove specific key
   ssh-add -D                # Remove all keys
   ```

---

## 🆘 Still Having Issues?

If you're still stuck:

1. **Enable verbose SSH output:**
   ```bash
   ssh -vvv user@hostname
   # Look for "debug" lines about authentication
   ```

2. **Check server logs:**
   ```bash
   # On the server:
   sudo tail -f /var/log/auth.log
   # or
   sudo tail -f /var/log/secure
   ```

3. **Verify your username:**
   ```bash
   # Common usernames:
   # - ec2-user (AWS EC2)
   # - ubuntu (Ubuntu)
   # - root (many VPS providers)
   # - your actual username
   ```

4. **Contact your server admin:**
   - Ask them to add your public key
   - Or request access credentials
   - Or ask about authentication method

---

## 🎉 Quick Start for Each Cloud Provider

### AWS EC2
```bash
chmod 600 ~/Downloads/your-key.pem
./ssh_dir_browser.py ec2-user@your-instance.amazonaws.com -i ~/Downloads/your-key.pem
```

### DigitalOcean
```bash
./ssh_dir_browser.py root@your-droplet-ip --password
# or with key:
./ssh_dir_browser.py root@your-droplet-ip -i ~/.ssh/digitalocean
```

### Google Cloud
```bash
# GCP usually uses SSH keys from metadata
./ssh_dir_browser.py your-username@your-instance-ip
```

### Azure
```bash
./ssh_dir_browser.py azureuser@your-vm.cloudapp.azure.com -i ~/.ssh/azure_key
```

### Linode
```bash
./ssh_dir_browser.py root@your-linode-ip --password
# or with key:
./ssh_dir_browser.py root@your-linode-ip -i ~/.ssh/linode_key
```

---

Happy connecting! 🚀
