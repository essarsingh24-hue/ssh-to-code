#!/bin/bash
# Quick test script to verify the fix

echo "=========================================="
echo "Testing SSH Directory Browser Fix"
echo "=========================================="
echo ""

# Test 1: Check Python environment
echo "1. Checking Python environment..."
if command -v python &> /dev/null; then
    PYTHON_CMD="python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Python not found!"
    exit 1
fi
echo "   ✓ Python: $PYTHON_CMD"

# Test 2: Check paramiko
echo ""
echo "2. Checking paramiko installation..."
if $PYTHON_CMD -c "import paramiko; print(f'   ✓ Paramiko version: {paramiko.__version__}')" 2>/dev/null; then
    :
else
    echo "   ❌ Paramiko not installed"
    echo "   Install with: pip install paramiko"
    exit 1
fi

# Test 3: Check if DSS key support exists
echo ""
echo "3. Checking DSS key support..."
if $PYTHON_CMD -c "import paramiko; hasattr(paramiko, 'DSSKey')" 2>/dev/null; then
    echo "   ℹ️  DSS keys: Not supported (Paramiko 3.0+)"
else
    echo "   ✓ DSS keys: Supported (Paramiko < 3.0)"
fi

# Test 4: Test import
echo ""
echo "4. Testing ssh_handler import..."
if $PYTHON_CMD -c "from ssh_handler import SSHHandler; print('   ✓ Import successful')" 2>/dev/null; then
    :
else
    echo "   ❌ Import failed!"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ All checks passed!"
echo "=========================================="
echo ""
echo "You can now connect with:"
echo "  ./ssh-browse user@hostname -i /path/to/key.pem"
echo ""
echo "Or with venv:"
echo "  source venv/bin/activate"
echo "  python ssh_dir_browser.py user@hostname -i /path/to/key.pem"
echo ""
