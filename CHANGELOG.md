# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of WeChat Official Account Auto-Writing Agent
- Intelligent article generation based on user-specified topics
- Real-time web search for latest information gathering
- Automatic image generation for article cover
- Content audit mechanism for WeChat Official Account compliance
- Auto-publish to WeChat Official Account draft box
- Multiple deployment options:
  - Coze Agent Store
  - MCP Server
  - Standalone API Service
- Docker support for containerized deployment
- One-click deployment script
- Comprehensive documentation

### Features
- **Web Search Tool**: Search for latest information from the web
- **Image Generation Tool**: Generate high-quality article cover images (2K resolution)
- **Content Audit Tool**: 
  - 7 violation type detection
  - LLM-based intelligent content review
  - Detailed audit report with modification suggestions
  - Built-in sensitive word filtering
- **WeChat Publish Tool**: 
  - Static configuration for AppId and AppSecret
  - Access token caching mechanism
  - Automatic article publishing to draft box

### Documentation
- User guide (README.md)
- Deployment guide (docs/PUBLISH_GUIDE.md)
- Contributing guide (CONTRIBUTING.md)
- Security policy (SECURITY.md)
- Code of conduct (CODE_OF_CONDUCT.md)

## [1.0.0] - 2025-01-XX

### Added
- Core Agent functionality
- LangChain + LangGraph 1.0 integration
- Doubao Seed 2.0 Pro model support
- WeChat Official Account API integration
- MCP Server implementation
- GitHub Actions CI/CD workflows
- Issue and Pull Request templates

## [Future Plans]

### Planned Features
- [ ] Multi-language article generation support
- [ ] Batch article creation
- [ ] Article template management
- [ ] Image style customization
- [ ] SEO optimization features
- [ ] Analytics dashboard
- [ ] Integration with more platforms (Zhihu, Jianshu, etc.)
- [ ] Web UI for easier usage

### Planned Improvements
- [ ] Enhanced content audit algorithms
- [ ] Better error handling and retry mechanisms
- [ ] Performance optimization
- [ ] Unit test coverage improvement
- [ ] More comprehensive documentation
- [ ] API rate limiting
- [ ] Caching mechanisms for better performance

---

## Version Format

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

## Types of Changes

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

## How to Update Changelog

When contributing to this project, please update the `[Unreleased]` section with your changes:

1. Add items under the appropriate category (Added, Changed, etc.)
2. Use the format: `- **Brief description**: Additional details if needed`
3. Reference related issues/PRs if applicable
4. Keep descriptions concise and clear

Example:
```markdown
### Added
- **Multi-language support**: Added support for English and Japanese article generation (#123)
```
