# Changelog

All notable changes to the YouTube Video Intelligence Suite will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-07-06

### 🎯 VTT→SRV1 Migration with Enhanced Quality Analysis

#### 🚀 Major Enhancements
- **Smart Format Fallback System**: Implemented SRV1 → JSON3 → TTML → VTT priority chain for superior transcript quality
- **Enhanced Quality Analysis**: Comprehensive safety validation with quality scoring, warnings, and recommendations
- **Advanced Deduplication**: Intelligent duplicate detection with effectiveness tracking and reporting
- **HTML Entity Support**: Proper decoding across all subtitle formats for clean text output
- **Context-Aware Validation**: Video metadata integration for enhanced quality assessment

#### Added
- **SRV1 Parser**: Native support for YouTube's highest-quality SRV1 (XML) subtitle format
- **JSON3 Parser**: Support for YouTube's JSON3 format with detailed timing information
- **Quality Metrics Dashboard**: Comprehensive quality scoring with safety penalties and warnings
- **Deduplication Effectiveness Tracking**: Measurement and reporting of duplicate removal efficiency
- **Enhanced Metadata Integration**: Video duration and context used for quality validation
- **Safety Validation System**: Multi-layer content quality checks with actionable warnings

#### Enhanced
- **All MCP Tools**: Updated to use enhanced extraction with metadata integration and quality analysis
- **Streamlined Server**: Applied VTT→SRV1 migration with full quality analysis pipeline
- **Script Consistency**: Aligned `scripts/youtube_to_mcp.py` with main server implementation
- **Error Handling**: Improved diagnostics with quality metrics and detailed error reporting
- **Output Quality**: Superior transcript quality through intelligent format selection

#### Technical Improvements
- **Format Priority System**: Automatic fallback ensures best available quality while maintaining compatibility
- **HTML Entity Decoding**: Consistent `html.unescape()` usage across all subtitle parsers
- **Quality Score Calculation**: Advanced algorithm considering line count, punctuation, timestamps, and safety factors
- **Content Safety Validation**: Detection of gibberish, excessive repetition, and language inconsistencies
- **Duration-Based Validation**: Transcript length validation using video metadata context

#### Fixed
- **VTT Duplication Issues**: Eliminated through preference for higher-quality SRV1/JSON3 formats
- **Text Encoding Problems**: Proper HTML entity decoding across all formats
- **Quality Assessment Gaps**: Comprehensive safety validation with actionable recommendations
- **Inconsistent Output**: Unified quality standards across both script and server implementations

#### Breaking Changes
- **Enhanced Function Signatures**: `extract_transcript_ytdlp()` now accepts optional metadata parameter
- **Quality Metrics Format**: Enhanced quality analysis includes new safety validation fields
- **Tool Response Format**: Updated to include deduplication effectiveness and quality warnings

#### Migration Notes
- **Automatic Enhancement**: Existing tools automatically benefit from improved quality
- **Backward Compatibility**: All existing MCP integrations work seamlessly with enhanced output
- **Quality Improvements**: Users will see better transcript quality and detailed quality reporting
- **No Configuration Changes**: Enhancement is transparent to end users

**🎉 This release delivers professional-grade transcript quality with comprehensive analysis capabilities!**

## [0.4.0] - 2025-07-01

### 🎯 Complete Migration to yt-dlp Only Approach

#### 🚨 BREAKING CHANGES
- **Removed youtube-transcript-api dependency**: All transcript extraction now uses yt-dlp exclusively
- **API Method Deprecation**: `extract_transcript_api()` function now returns deprecation error
- **System Status Format**: Updated response format to reflect new architecture

#### 🚀 Major Improvements
- **Universal Reliability**: Eliminated cloud server blocking issues that plagued youtube-transcript-api
- **Enhanced Quality**: Applied proven VTT parsing and deduplication logic from standalone script
- **Simplified Architecture**: Removed dual-method complexity for easier maintenance
- **Better Performance**: Single extraction pipeline with improved error handling

#### Added
- **Advanced VTT Processing**: Sophisticated timestamp parsing and text cleanup
- **Enhanced Deduplication**: Advanced algorithms to remove caption overlaps and repetitions
- **Migration Documentation**: Comprehensive documentation in `docs/migration/`
- **Deprecation Stubs**: Graceful deprecation of old API methods with clear error messages

#### Changed
- **Core Extraction Logic**: `src/youtube_transcript_server/extraction.py` fully migrated to yt-dlp
- **Resource System**: `src/youtube_transcript_server/resources.py` updated status checks
- **Dependencies**: `pyproject.toml` cleaned to require only `yt-dlp>=2023.12.30`
- **Documentation**: Updated README.md and acknowledgments to reflect yt-dlp approach

#### Fixed
- **Cloud Server Compatibility**: No more blocking issues on VPS/cloud environments
- **Extraction Consistency**: Same quality output across all components
- **Rate Limiting Issues**: Eliminated aggressive rate limiting from old API
- **Fallback Complexity**: Removed complicated dual-method fallback logic

#### Technical Details
- **File Organization**: Moved migration docs to `docs/migration/` directory
- **Code Quality**: Unified extraction pipeline based on proven implementation
- **Testing**: All modules import and function correctly with yt-dlp only
- **Error Handling**: Improved timeout and error recovery mechanisms

#### Migration Notes
- **User Impact**: Zero impact on MCP tool usage - all tools work identically
- **Developer Impact**: `extract_transcript_api()` calls will receive deprecation errors
- **Quality Improvement**: Better transcript quality with advanced deduplication
- **Reliability Boost**: Significantly reduced extraction failures

**🎉 This release marks a major milestone in reliability and maintainability!**

## [0.3.1] - 2025-06-24

### 🧹 Repository Cleanup & Production Readiness

#### Changed
- **Complete Repository Cleanup**: Systematically organized development artifacts while preserving all essential functionality
- **Streamlined Structure**: Clean, production-ready codebase with organized archive system
- **Enhanced Documentation**: Updated README.md and project documentation to reflect clean structure
- **Improved Testing**: Consolidated to core test suite with 5 essential test files
- **Optimized Scripts**: Reduced to essential utility scripts (validate_setup.py, youtube_to_mcp.py)

#### Added
- **Organized Archive System**: Created structured archive with 4 categories:
  - `archive/development-docs/` - Development planning and investigation documentation
  - `archive/debug-files/` - Debug scripts, test files, and VTT samples  
  - `archive/test-outputs/` - Historical test data and transcript outputs
  - `archive/scripts-debug/` - Development debugging scripts
- **Git History Preservation**: All file moves tracked with proper git rename detection
- **Version Tagging**: Comprehensive tagging strategy for cleanup process tracking

#### Removed (Archived)
- **44 Development Files**: Moved to organized archive structure
- **Debug Artifacts**: VTT test files, duplicate investigation scripts
- **Test Outputs**: Historical test data and development transcripts  
- **Development Scripts**: 13 debugging and investigation scripts
- **Development Documentation**: Investigation reports and transformation notes

#### Technical Improvements
- **Clean Project Structure**: Organized directories with clear separation of concerns
- **Production Ready**: Repository optimized for end-user deployment
- **Maintained Functionality**: All 11 tools + 8 resources + 6 prompts preserved
- **Enhanced Validation**: Comprehensive setup validation and testing confirmed

#### Validation Results
- ✅ **All Tests Passing**: 5 core test files executing in 1.98s
- ✅ **MCP Server**: Starts successfully with `mcp dev` command
- ✅ **Claude Desktop Integration**: Configuration validated and working
- ✅ **Architecture Intact**: 11 tools + 8 resources + 6 prompts fully functional
- ✅ **Setup Validation**: All environment checks pass

### Benefits
- 🎯 **Clean Codebase**: Professional, maintainable repository structure
- 📦 **Production Ready**: Streamlined for deployment and distribution
- 🗂️ **Organized History**: All development artifacts preserved in logical structure
- 🔍 **Easy Navigation**: Clear separation between production code and development artifacts
- 🚀 **Enhanced Performance**: Reduced repository size while maintaining full functionality

## [0.3.0] - 2025-06-03

### 🏗️ Enhanced MCP Architecture - Complete Tools + Resources + Prompts

#### Added
- **8 Dynamic Resources**: Real-time access to cached transcripts, metadata, analysis history, and system information
- **6 Guided Prompts**: Pre-built conversation starters for common video analysis workflows
- **Enhanced Caching System**: In-memory caching with analysis history tracking and performance monitoring
- **Modular Architecture**: Clean separation of concerns with dedicated modules for configuration, resources, and prompts
- **Resource Mirror Tools**: Tool-based access to all resources for MCP clients without resource support
- **New Main Entry Point**: `main.py` provides clean entry point routing to enhanced server

#### Enhanced
- **Analysis History Tracking**: All tools now track usage and maintain analysis history
- **Performance Monitoring**: Memory usage tracking and system status monitoring
- **Error Handling**: Improved error handling with centralized logging
- **Configuration Management**: Centralized settings and configuration system

#### Architecture Changes
- **Enhanced Server**: `enhanced_server.py` - Complete MCP server with tools, resources, and prompts
- **Modular Components**: `src/youtube_transcript_server/` package with dedicated modules
- **Legacy Support**: Original `server.py` maintained for backward compatibility
- **Updated Entry Points**: `main.py` routes to enhanced server by default

#### Resources Added
- `transcripts://cached` - Browse all cached transcripts and metadata
- `transcripts://{video_id}/metadata` - Access specific video information
- `transcripts://{video_id}/sample` - Preview transcript samples
- `analytics://history` - View analysis history and usage patterns
- `analytics://supported_languages` - Language support information
- `analytics://memory_usage` - Memory usage and cache statistics
- `config://server` - Server configuration and settings
- `system://status` - System health and status information

#### Prompts Added
- `transcript_analysis_workshop` - Comprehensive analysis workflow guidance
- `video_comparison_framework` - Multi-video comparison methodology
- `content_extraction_guide` - Content extraction and summarization workflows
- `study_notes_generator` - Educational content and study material creation
- `video_research_planner` - Research planning and methodology guidance
- `list_available_prompts` - Browse all available prompt templates

#### Technical Improvements
- **20 Total Tools**: 11 original + 8 resource mirrors + 1 resource listing tool
- **Comprehensive Testing**: Enhanced test coverage for new architecture
- **Documentation Updates**: Updated README, project structure, and examples
- **Version Bump**: Updated to v0.3.0 reflecting major architectural enhancement

### Benefits
- ✅ **Complete MCP Implementation** following best practices
- ✅ **Dynamic Data Access** through resources
- ✅ **Guided Workflows** through prompts
- ✅ **Enhanced Caching** with history and performance tracking
- ✅ **Modular Design** for maintainability and extensibility
- ✅ **Backward Compatibility** with existing integrations

## [0.2.0] - 2025-05-29

### 🎉 Major Transformation - Claude Desktop Native Integration

#### Added
- **Direct Claude Desktop Integration**: Analysis now performed directly by Claude Desktop
- **Structured Prompt System**: Tools return formatted prompts for Claude Desktop to process
- **Zero External Dependencies**: No API keys or external AI services required
- **Enhanced Documentation**: Complete transformation guide and updated installation instructions
- **Improved Testing**: New test suite for transformation verification

#### Changed
- **Analysis Architecture**: Completely redesigned to work with Claude Desktop's built-in capabilities
- **Tool Outputs**: All analysis tools now return structured prompts instead of direct AI responses
- **Dependencies**: Removed `anthropic` and `openai` client libraries
- **Configuration**: Simplified setup process without API key requirements
- **Documentation**: Updated all guides to reflect the new approach

#### Removed
- **External AI API Calls**: No longer calls Anthropic or OpenAI APIs directly
- **API Key Management**: Eliminated need for external API key configuration
- **AI Client Abstractions**: Removed `get_ai_client()` and `analyze_with_ai()` functions

#### Technical Details
- **11 Analysis Tools Transformed**: All sophisticated analysis capabilities preserved
- **Backward Compatibility**: Core transcript extraction functionality unchanged
- **Enhanced Reliability**: No external API failures or rate limits
- **Better Integration**: Seamless experience within Claude Desktop ecosystem

### Benefits
- ✅ **Zero Setup Complexity** for AI analysis features
- ✅ **100% Reliability** - no external API dependencies
- ✅ **No Rate Limits** or API costs
- ✅ **Better User Experience** with native Claude Desktop integration
- ✅ **All Original Features Preserved** with improved reliability

## [0.1.0] - 2025-05-28

### Added
- Initial release of YouTube Video Intelligence Suite
- 11 comprehensive AI-powered analysis tools
- Multi-language transcript extraction
- Dual AI provider support (Anthropic Claude & OpenAI GPT)
- Complete MCP server implementation with FastMCP
- Comprehensive documentation suite
- Robust error handling and validation
- Multiple transcript extraction methods (youtube-transcript-api, yt-dlp)

### Features
- Basic transcript extraction and search
- AI-powered video analysis with external APIs
- Educational tools (study notes, quizzes, citations)
- Content analysis (summaries, key points, fact checking)
- Presentation analysis and multi-video comparison
- Complete Claude Desktop integration via MCP protocol
