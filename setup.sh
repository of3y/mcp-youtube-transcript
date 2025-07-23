#!/bin/bash

# 🚀 MCP YouTube Transcript Server - Easy Setup Script
# This script helps set up the YouTube Video Intelligence Suite quickly

set -e  # Exit on any error

echo "🎥 YouTube Video Intelligence Suite - Setup Script"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if we're in the right directory
if [[ ! -f "main.py" ]] || [[ ! -f "streamlined_server.py" ]]; then
    print_error "This script must be run from the mcp-youtube-transcript directory"
    print_info "Please cd to the project directory first"
    exit 1
fi

# Get absolute path
PROJECT_PATH=$(pwd)
print_info "Project path: $PROJECT_PATH"

# Step 1: Check Python version
echo ""
echo "Step 1: Checking Python version..."
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
REQUIRED_VERSION="3.10"

if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"; then
    print_success "Python $PYTHON_VERSION ✓"
else
    print_error "Python $PYTHON_VERSION found, but Python 3.10+ is required"
    exit 1
fi

# Step 2: Check/Install uv
echo ""
echo "Step 2: Checking uv package manager..."
if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version | cut -d' ' -f2)
    print_success "uv $UV_VERSION is installed ✓"
else
    print_warning "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.zshrc 2>/dev/null || source ~/.bashrc 2>/dev/null || true
    
    if command -v uv &> /dev/null; then
        print_success "uv installed successfully ✓"
    else
        print_error "Failed to install uv. Please install manually:"
        print_info "curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
fi

# Step 3: Install dependencies
echo ""
echo "Step 3: Installing project dependencies..."
if uv sync; then
    print_success "Dependencies installed successfully ✓"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Step 4: Run quick test
echo ""
echo "Step 4: Running quick validation test..."
if python3 quick_test.py; then
    print_success "All tests passed! ✓"
else
    print_warning "Some tests failed, but the basic setup seems to work"
    print_info "You can still proceed with Claude Desktop configuration"
fi

# Step 5: Claude Desktop configuration
echo ""
echo "Step 5: Claude Desktop Configuration"
echo "====================================="

CLAUDE_CONFIG_PATH="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

print_info "Claude Desktop config should be at:"
print_info "$CLAUDE_CONFIG_PATH"

if [[ -f "$CLAUDE_CONFIG_PATH" ]]; then
    print_info "Config file exists. You'll need to add this configuration:"
else
    print_warning "Config file doesn't exist. You'll need to create it."
fi

echo ""
echo "Add this to your Claude Desktop configuration:"
echo ""
echo "{"
echo "    \"mcpServers\": {"
echo "        \"youtube-transcript\": {"
echo "            \"command\": \"uv\","
echo "            \"args\": ["
echo "                \"run\","
echo "                \"--directory\","
echo "                \"$PROJECT_PATH\","
echo "                \"python\","
echo "                \"main.py\""
echo "            ]"
echo "        }"
echo "    }"
echo "}"

# Step 6: Create a helper script for the config
echo ""
echo "Step 6: Creating helper files..."

# Create a config snippet file
cat > claude_config_snippet.json << EOF
{
    "mcpServers": {
        "youtube-transcript": {
            "command": "uv",
            "args": [
                "run",
                "--directory",
                "$PROJECT_PATH",
                "python",
                "main.py"
            ]
        }
    }
}
EOF

print_success "Created claude_config_snippet.json with your specific path"

# Step 7: Final instructions
echo ""
echo "🎉 Setup Complete!"
echo "=================="
print_success "The MCP YouTube Transcript Server is ready!"
echo ""
print_info "Next steps:"
echo "1. Copy the configuration from claude_config_snippet.json"
echo "2. Add it to your Claude Desktop config at:"
echo "   $CLAUDE_CONFIG_PATH"
echo "3. Restart Claude Desktop completely"
echo "4. Test with: 'Get transcript from: https://www.youtube.com/watch?v=jNQXAC9IVRw'"
echo ""
print_info "📖 For detailed instructions, see DEPLOYMENT_GUIDE.md"
print_info "🔧 For troubleshooting, see docs/troubleshooting.md"

echo ""
print_success "Happy transcript extracting! 🎥✨"
