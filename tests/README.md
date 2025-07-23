# Test Suite for YouTube Video Intelligence Suite v0.3.0

This directory contains the comprehensive test suite for the v0.3.0 enhanced MCP architecture.

## 🧪 Test Structure

### Core Test Files

- **`test_v030_comprehensive.py`** - Overall architecture and integration tests
- **`test_tools_functionality.py`** - Individual tool functionality tests 
- **`test_resources_system.py`** - Resources module and caching tests
- **`test_prompts_system.py`** - Prompts system and schema tests
- **`test_mcp_integration.py`** - MCP protocol compliance and server tests

### Test Runner

- **`run_test_suite.py`** - Complete test suite runner with reporting

### Archived Tests

- **`archive/`** - Previous test files from earlier versions (kept for reference)

## 🚀 Running Tests

### Quick Smoke Test
```bash
# Run basic functionality check
uv run python tests/run_test_suite.py --smoke
```

### Complete Test Suite
```bash
# Run all tests with detailed reporting
uv run python tests/run_test_suite.py
```

### Individual Test Files
```bash
# Run specific test file
uv run pytest tests/test_v030_comprehensive.py -v

# Run with coverage
uv run pytest tests/ --cov=src --cov=enhanced_server
```

### Clean Environment
```bash
# Clean test environment before running
uv run python tests/run_test_suite.py --clean
```
