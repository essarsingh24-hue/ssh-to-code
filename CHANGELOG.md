# Changelog

All notable changes to the SSH Directory Browser project will be documented in this file.

## [1.0.2] - 2026-07-13

### Added
- README guidance for Linux/Ubuntu users to install with `pipx`
- Troubleshooting note for PEP 668 `externally-managed-environment`

### Changed
- Package version bumped to `1.0.2` in `pyproject.toml`

## [1.1.0] - 2025-12-21

### Added
- **Create New Folder**: Press `n` to create a new folder in the current directory
  - Interactive prompt with input validation
  - Automatic refresh after folder creation
  - Error handling for invalid folder names

- **Explicit Refresh**: Press `r` to manually refresh the directory listing
  - Useful after external changes to the filesystem
  - Shows "Refreshed" status message

### Changed
- Updated help text to include new keyboard shortcuts
- Improved status messages for better user feedback
- Enhanced navigation experience

### UI Improvements
- New keyboard shortcuts:
  - `n` / `N`: Create new folder
  - `r` / `R`: Refresh directory listing (already existed, now documented)
- Updated help line to show all available commands concisely
- Better feedback messages for folder creation

## [1.0.0] - 2025-12-21

### Initial Release
- Terminal-based directory browser with curses UI
- SSH connection support (key-based and password authentication)
- VS Code Remote-SSH integration
- Configuration management for saved hosts
- Interactive host selector
- Visual file type indicators (directories, files, executables, symlinks)
- Keyboard navigation
- Installation script

### Features
- Browse remote directories via SSH
- Open directories in VS Code with one keystroke
- Save frequently used SSH hosts
- Navigate with arrow keys
- Home directory shortcut
- Parent directory navigation
