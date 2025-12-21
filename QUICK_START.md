# Quick Start Guide - New Features

## 🎯 What's New in v1.1.0

Two powerful new features to enhance your workflow!

---

## 📁 Feature 1: Create New Folder

### Press `n` to create folders on the fly!

```
┌──────────────────────────────────────────────────────────┐
│ SSH Directory Browser - user@server                      │
│ Path: /var/www                                           │
│ ↑/↓: Navigate | Enter: Open | 'o': VS Code | 'n': New..│
├──────────────────────────────────────────────────────────┤
│  📁 project1/                                            │
│  📁 project2/                                            │
│  📁 shared/                                              │
│  📄 index.html                                           │
│                                                          │
│              Press 'n' to create new folder              │
└──────────────────────────────────────────────────────────┘

                          ↓ Press 'n'

┌──────────────────────────────────────────────────────────┐
│                                                          │
│  ┌────────────────────────────────────────────────┐     │
│  │ Create New Folder:                              │     │
│  │ Name: my-new-project_                           │     │
│  │                                                 │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
└──────────────────────────────────────────────────────────┘

                        ↓ Press Enter

┌──────────────────────────────────────────────────────────┐
│ SSH Directory Browser - user@server                      │
│ Path: /var/www                                           │
│ ↑/↓: Navigate | Enter: Open | 'o': VS Code | 'n': New..│
├──────────────────────────────────────────────────────────┤
│  📁 my-new-project/  ← NEW!                              │
│  📁 project1/                                            │
│  📁 project2/                                            │
│  📁 shared/                                              │
│  📄 index.html                                           │
├──────────────────────────────────────────────────────────┤
│ Created folder: my-new-project                           │
└──────────────────────────────────────────────────────────┘
```

### Usage:
1. Navigate to desired parent directory
2. Press `n`
3. Type folder name
4. Press Enter
5. ✨ Folder created and visible immediately!

---

## 🔄 Feature 2: Manual Refresh

### Press `r` to reload the directory listing!

Useful when:
- Files uploaded via SFTP/FTP
- Changes made by other users
- External processes created/deleted files
- You want to verify the current state

```
┌──────────────────────────────────────────────────────────┐
│ SSH Directory Browser - user@server                      │
│ Path: /var/www/uploads                                   │
│ ↑/↓: Navigate | Enter: Open | 'r': Refresh | 'q': Quit │
├──────────────────────────────────────────────────────────┤
│  📄 old_file.txt                                         │
│  📄 document.pdf                                         │
│                                                          │
│         (Files uploaded externally via SFTP)             │
│                                                          │
│              Press 'r' to see new files                  │
└──────────────────────────────────────────────────────────┘

                          ↓ Press 'r'

┌──────────────────────────────────────────────────────────┐
│ SSH Directory Browser - user@server                      │
│ Path: /var/www/uploads                                   │
│ ↑/↓: Navigate | Enter: Open | 'r': Refresh | 'q': Quit │
├──────────────────────────────────────────────────────────┤
│  📄 new_upload.zip     ← NEW!                            │
│  📄 old_file.txt                                         │
│  📄 document.pdf                                         │
│  📄 image.jpg          ← NEW!                            │
├──────────────────────────────────────────────────────────┤
│ Refreshed                                                │
└──────────────────────────────────────────────────────────┘
```

---

## 🎮 Complete Keyboard Reference

```
╔══════════════════════════════════════════════════════════╗
║                    NAVIGATION                            ║
╠══════════════════════════════════════════════════════════╣
║  ↑ / ↓       Navigate through items                      ║
║  Enter       Open selected directory                     ║
║  h           Jump to home directory                      ║
╠══════════════════════════════════════════════════════════╣
║                  FILE OPERATIONS                         ║
╠══════════════════════════════════════════════════════════╣
║  n           Create new folder           ⭐ NEW!         ║
║  r           Refresh directory listing                   ║
╠══════════════════════════════════════════════════════════╣
║               VS CODE INTEGRATION                        ║
╠══════════════════════════════════════════════════════════╣
║  o           Open current dir in VS Code                 ║
╠══════════════════════════════════════════════════════════╣
║                      OTHER                               ║
╠══════════════════════════════════════════════════════════╣
║  q           Quit application                            ║
╚══════════════════════════════════════════════════════════╝
```

---

## 🚀 Quick Workflow Examples

### Example 1: Start a New Project

```bash
# 1. Connect
./ssh_dir_browser.py user@dev-server.com --start-path ~/projects

# 2. Create project folder (press 'n')
#    Type: "my-awesome-app"
#    Press Enter

# 3. Navigate into folder (press Enter on it)

# 4. Create subdirectories (press 'n' for each):
#    - src
#    - public
#    - tests

# 5. Open in VS Code (press 'o')
```

### Example 2: Check for Updates

```bash
# 1. Connect to deployment directory
./ssh_dir_browser.py deploy@prod.com --start-path /var/www/app

# 2. Check if deployment finished (press 'r' to refresh)

# 3. Navigate to updated code (arrow keys)

# 4. Open in VS Code to review (press 'o')
```

### Example 3: Organize Files

```bash
# 1. Connect to messy directory
./ssh_dir_browser.py user@server.com --start-path /home/user/downloads

# 2. Create organization folders:
#    Press 'n', type "documents", Enter
#    Press 'n', type "images", Enter
#    Press 'n', type "videos", Enter
#    Press 'n', type "archives", Enter

# 3. Press 'r' to ensure all folders visible

# 4. Open in VS Code to move files (press 'o')
```

---

## ⚡ Pro Tips

1. **Chain operations**: Create folder (`n`) → Navigate into it (Enter) → Open in VS Code (`o`)

2. **Verify creation**: After pressing `n`, the directory auto-refreshes. No need to press `r`!

3. **Quick refresh**: If anything seems outdated, just tap `r`

4. **Home shortcut**: Lost? Press `h` to jump to home directory

5. **Cancel creation**: Press Escape or just Enter with empty name to cancel folder creation

---

## 📋 Installation Reminder

If you haven't installed yet:

```bash
# Install dependencies
pip install paramiko

# Make executable
chmod +x ssh_dir_browser.py

# Run
./ssh_dir_browser.py user@your-server.com
```

---

## 🆘 Troubleshooting

**Q: I press 'n' but nothing happens**  
A: Make sure you have write permissions in the current directory

**Q: Folder creation fails**  
A: Check if folder name contains invalid characters (no `/` allowed)

**Q: New folders don't appear**  
A: They should auto-refresh, but try pressing `r` if needed

**Q: Can I create nested folders?**  
A: Yes! Create a folder, navigate into it (Enter), then create another (n)

---

## 🎉 Get Started Now!

```bash
./ssh_dir_browser.py user@hostname
```

Press `n` to create your first folder!  
Press `r` to refresh anytime!  
Press `o` to open in VS Code!

Happy browsing! 🚀
