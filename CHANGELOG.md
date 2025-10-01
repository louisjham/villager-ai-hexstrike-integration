# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub issue templates for bug reports and feature requests
- Comprehensive CI/CD pipeline with automated testing
- Security scanning with Trivy vulnerability scanner
- Docker image building and caching
- Code coverage reporting with Codecov
- Organized folder structure for better maintainability

### Changed
- Reorganized project structure for better GitHub presentation
- Moved core files to `src/villager_ai/` directory
- Moved scripts to `scripts/` directory
- Moved Docker files to `docker/` directory

### Security
- Added security scanning to CI/CD pipeline
- Added security issue template for responsible disclosure

## [1.0.0] - 2024-10-01

### Added
- Initial release of Villager AI Framework
- AI-driven cybersecurity automation platform
- TaskNode for intelligent task decomposition
- MCP Client for external tool access
- Agent Scheduler for LLM orchestration
- Kali Driver for containerized security tools
- Browser Automation service
- GitHub integration tools
- Comprehensive test suite
- Docker containerization support
- 24-hour self-destruct container mechanism
- Kali Linux Docker container integration
- Real security tools integration (MSFVenom, Nmap, SQLMap, etc.)
- Uncensored AI model support via Ollama
- MCP (Model Context Protocol) integration
- Task-based command and control architecture
- Forensic evasion capabilities
- SSH-based command execution
- Pre-installed security tools in containers

### Features
- **AI Orchestration**: Intelligent task decomposition and agent scheduling
- **Containerized Security**: Isolated Kali Linux environments for safe tool execution
- **MCP Integration**: Seamless Model Context Protocol integration for tool access
- **Real Security Tools**: Access to 150+ specialized cybersecurity tools
- **GitHub Integration**: Repository management and tool discovery capabilities
- **Uncensored AI**: Local Ollama integration with unrestricted cybersecurity capabilities
- **Task Management**: Sophisticated task-based C2 system through FastAPI
- **Agent Scheduling**: LLM orchestration for complex operations
- **Tools Manager**: Function registry for tool execution
- **Forensic Evasion**: Ephemeral containers with randomized ports and 24-hour self-destruct

### Architecture
- **Villager Server** (Port 37695): Task management and orchestration
- **MCP Client** (Port 25989): Service communication and streaming responses
- **Kali Driver** (Port 1611): Security tools execution
- **Browser Automation** (Port 8080): Web automation capabilities

### Security Tools
- MSFVenom payload generation
- Nmap network scanning
- SQLMap vulnerability testing
- Hydra password attacks
- John the Ripper hash cracking
- Gobuster directory enumeration
- Nikto web vulnerability scanning
- And 150+ other Kali Linux tools

### Documentation
- Comprehensive README with setup instructions
- AI Assistant Guide for MCP integration
- Setup Guide with detailed configuration
- Troubleshooting guide for common issues
- API documentation for all MCP tools
- Architecture documentation
- Usage examples and best practices

### Testing
- Comprehensive test suite with 12 test categories
- Unit tests for individual components
- Integration tests for service interactions
- End-to-end tests for complete workflows
- RAT payload generation testing
- MCP tools integration testing
- Security tools availability testing
- Docker availability testing
- Complete workflow testing

### Dependencies
- Python 3.8+ (3.13 recommended)
- Docker for containerized execution
- Ollama for local AI models
- FastAPI for web services
- LangChain for AI orchestration
- MCP for tool integration
- And 50+ other Python packages

---

## Version History

- **1.0.0**: Initial release with full Villager AI Framework functionality
- **Unreleased**: GitHub organization and contribution improvements

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Security

For security vulnerabilities, please report privately to security@villager-ai.com.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
