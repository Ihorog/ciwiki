codex/document-ciwiki-installation-and-usage-instructions
# CiWiki

CiWiki is the knowledge base for the Cimeika ecosystem—an interactive platform for organizing time, creativity, emotional state and communication.

## Installation

1. Install dependencies:
   ```bash
   npm install
   ```
2. Preview the documentation locally:
   ```bash
   pip install mkdocs-material
   mkdocs serve
   ```

## Usage

- Run tests:
  ```bash
  npm test
  ```
- Build static documentation:
  ```bash
  mkdocs build
  ```

## Documentation, Tests and Deployment

- Documentation: see [docs/](docs/)
- Tests: see [tests/](tests/) and execute with `npm test`
- Deployment: GitHub Actions workflow in [workflows/integration.yml](workflows/integration.yml); this copies docs into the `cimeika` repository.

## Project Structure

```
.
├── docs/         # Documentation markdown sources
├── tests/        # Jest test suite
├── workflows/    # CI/CD configuration
├── mkdocs.yml    # MkDocs configuration
├── package.json  # Node.js project metadata
└── README.md
```
