#!/usr/bin/env python3
"""
SSH Authentication Troubleshooter
Helps diagnose SSH connection and key issues
"""

import os
import sys
import subprocess
import glob


def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_key_file(key_path):
    """Check a key file for common issues"""
    key_path = os.path.expanduser(key_path)
    
    if not os.path.exists(key_path):
        print(f"  ✗ File not found: {key_path}")
        return False
    
    print(f"  ✓ File exists: {key_path}")
    
    # Check permissions
    stat_info = os.stat(key_path)
    mode = oct(stat_info.st_mode)[-3:]
    
    if mode != '600':
        print(f"  ⚠️  Permissions: {mode} (should be 600)")
        print(f"     Fix with: chmod 600 {key_path}")
    else:
        print(f"  ✓ Permissions: {mode}")
    
    # Check if encrypted
    try:
        with open(key_path, 'r') as f:
            content = f.read()
            if 'ENCRYPTED' in content:
                print("  🔐 Key is ENCRYPTED (requires passphrase)")
            else:
                print("  🔓 Key is unencrypted")
    except Exception as e:
        print(f"  ⚠️  Could not read file: {e}")
    
    # Try to identify key type
    try:
        with open(key_path, 'r') as f:
            first_line = f.readline()
            if 'RSA' in first_line:
                print("  📋 Type: RSA")
            elif 'OPENSSH' in first_line:
                print("  📋 Type: OpenSSH (Ed25519/ECDSA/RSA)")
            elif 'DSA' in first_line:
                print("  📋 Type: DSA")
            elif 'EC' in first_line:
                print("  📋 Type: ECDSA")
            else:
                print(f"  📋 Type: Unknown")
    except:
        pass
    
    return True


def check_ssh_agent():
    """Check if SSH agent is running and what keys are loaded"""
    print_header("SSH Agent Status")
    
    # Check if agent is running
    if 'SSH_AUTH_SOCK' in os.environ:
        print("  ✓ SSH agent is running")
        
        # List loaded keys
        try:
            result = subprocess.run(['ssh-add', '-l'], 
                                  capture_output=True, 
                                  text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                print("\n  Loaded keys:")
                for line in result.stdout.strip().split('\n'):
                    print(f"    • {line}")
            else:
                print("  ℹ️  No keys loaded in agent")
                print("\n  💡 Add keys with: ssh-add /path/to/key")
        except Exception as e:
            print(f"  ⚠️  Could not list keys: {e}")
    else:
        print("  ✗ SSH agent not running")
        print("\n  💡 Start with: eval \"$(ssh-agent -s)\"")


def check_ssh_config():
    """Check SSH config file"""
    print_header("SSH Configuration")
    
    config_path = os.path.expanduser('~/.ssh/config')
    
    if os.path.exists(config_path):
        print(f"  ✓ Config file exists: {config_path}")
        
        try:
            with open(config_path, 'r') as f:
                content = f.read()
                hosts = [line.split()[1] for line in content.split('\n') 
                        if line.strip().startswith('Host ') and '*' not in line]
                
                if hosts:
                    print(f"\n  Configured hosts ({len(hosts)}):")
                    for host in hosts[:10]:
                        print(f"    • {host}")
                    if len(hosts) > 10:
                        print(f"    ... and {len(hosts) - 10} more")
                else:
                    print("  ℹ️  No hosts configured")
        except Exception as e:
            print(f"  ⚠️  Could not read config: {e}")
    else:
        print(f"  ℹ️  No SSH config file found")
        print(f"     You can create one at: {config_path}")


def find_keys():
    """Find all SSH keys"""
    print_header("Available SSH Keys")
    
    ssh_dir = os.path.expanduser('~/.ssh')
    
    if not os.path.exists(ssh_dir):
        print(f"  ✗ .ssh directory not found: {ssh_dir}")
        return
    
    print(f"  Searching in: {ssh_dir}\n")
    
    # Common key patterns
    patterns = ['id_rsa', 'id_ed25519', 'id_ecdsa', 'id_dsa', '*.pem']
    
    found_keys = []
    for pattern in patterns:
        path = os.path.join(ssh_dir, pattern)
        found = glob.glob(path)
        found_keys.extend([f for f in found if not f.endswith('.pub')])
    
    # Also check common PEM locations
    pem_locations = [
        '~/Downloads/*.pem',
        '~/keys/*.pem',
        '~/*.pem',
    ]
    
    for location in pem_locations:
        expanded = os.path.expanduser(location)
        found_keys.extend(glob.glob(expanded))
    
    if found_keys:
        print(f"  Found {len(found_keys)} key(s):\n")
        for key in found_keys:
            check_key_file(key)
            print()
    else:
        print("  ℹ️  No SSH keys found")
        print("\n  💡 Generate a new key with:")
        print("     ssh-keygen -t ed25519 -C \"your_email@example.com\"")


def test_connection(hostname, username, key_path=None):
    """Test SSH connection"""
    print_header(f"Testing Connection: {username}@{hostname}")
    
    cmd = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5']
    
    if key_path:
        cmd.extend(['-i', os.path.expanduser(key_path)])
    
    cmd.extend([f"{username}@{hostname}", 'echo', 'SUCCESS'])
    
    print(f"  Command: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              timeout=10)
        
        if 'SUCCESS' in result.stdout:
            print("  ✓ Connection successful!")
            return True
        else:
            print("  ✗ Connection failed")
            if result.stderr:
                print(f"\n  Error output:")
                for line in result.stderr.strip().split('\n')[:5]:
                    print(f"    {line}")
            return False
    except subprocess.TimeoutExpired:
        print("  ✗ Connection timeout")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def print_recommendations():
    """Print troubleshooting recommendations"""
    print_header("Recommendations")
    
    print("""
  1. If you have an ENCRYPTED key without passphrase:
     • Use password authentication: --password
     • Or generate new key: ssh-keygen -t ed25519
     • Or contact admin for new credentials

  2. For convenience with encrypted keys:
     • Add to SSH agent: ssh-add /path/to/key
     • Enter passphrase once, then connect without -i flag

  3. For AWS EC2 or cloud instances:
     • Download PEM file from provider
     • Set permissions: chmod 600 ~/path/to/key.pem
     • Use: ./ssh_dir_browser.py user@host -i ~/path/to/key.pem

  4. Check key is authorized on server:
     • Your public key must be in server's ~/.ssh/authorized_keys
     • Test: ssh -v user@hostname

  5. Common usernames by provider:
     • AWS EC2: ec2-user, ubuntu, admin
     • DigitalOcean: root
     • Google Cloud: your-username
     • Azure: azureuser
     • Most Linux: your-username or root
    """)


def main():
    print("\n" + "=" * 60)
    print("  SSH AUTHENTICATION TROUBLESHOOTER")
    print("=" * 60)
    
    import argparse
    parser = argparse.ArgumentParser(description="Diagnose SSH authentication issues")
    parser.add_argument('--test', metavar='user@host', 
                       help='Test connection to specified host')
    parser.add_argument('--key', '-i', metavar='PATH',
                       help='Key file to test')
    parser.add_argument('--check-key', metavar='PATH',
                       help='Check specific key file')
    
    args = parser.parse_args()
    
    if args.check_key:
        print_header(f"Checking Key File")
        check_key_file(args.check_key)
    elif args.test:
        if '@' not in args.test:
            print("\n  ✗ Invalid format. Use: user@hostname")
            sys.exit(1)
        
        username, hostname = args.test.split('@', 1)
        test_connection(hostname, username, args.key)
    else:
        # Full diagnostic
        find_keys()
        check_ssh_agent()
        check_ssh_config()
        print_recommendations()
    
    print("\n" + "=" * 60)
    print("\n💡 For detailed help, see: AUTH_GUIDE.md")
    print("   Or run: ./ssh_dir_browser.py user@hostname")
    print()


if __name__ == "__main__":
    main()
