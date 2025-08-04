# ESO Logs Python - Project Structure

## Repository Layout
```
esologs-python/
├── esologs/                    # Main package
│   ├── __init__.py            # Package initialization, exports
│   ├── client.py              # Main client class (86 lines)
│   ├── client_factory.py      # Client instantiation
│   ├── auth.py                # OAuth2 authentication
│   ├── user_auth.py           # User authentication flows
│   ├── method_factory.py      # Dynamic method generation
│   ├── validators.py          # Input validation functions
│   ├── param_builders.py      # Parameter processing
│   ├── queries.py             # GraphQL query definitions
│   ├── py.typed               # PEP 561 type hint marker
│   ├── mixins/                # API method mixins
│   │   ├── __init__.py
│   │   ├── game_data.py       # Game data methods
│   │   ├── character.py       # Character methods
│   │   ├── guild.py           # Guild methods
│   │   ├── report.py          # Report methods
│   │   ├── world_data.py      # World data methods
│   │   ├── progress_race.py   # Progress race methods
│   │   └── user.py            # User methods
│   └── _generated/            # Auto-generated GraphQL code
│       ├── *.py               # 30+ generated files
│       └── ...
├── tests/                     # Test suites
│   ├── __init__.py
│   ├── conftest.py           # Shared fixtures
│   ├── README.md             # Test documentation
│   ├── unit/                 # Unit tests (164 tests)
│   ├── integration/          # Integration tests (129 tests)
│   ├── sanity/               # Sanity tests (18 tests)
│   └── docs/                 # Documentation tests (117 tests)
├── docs/                     # MkDocs documentation
│   ├── index.md             # Home page
│   ├── installation.md      # Installation guide
│   ├── quickstart.md        # Getting started
│   ├── api-reference/       # API documentation
│   ├── examples/            # Code examples
│   └── assets/              # Images, logos
├── scripts/                  # Utility scripts
│   ├── generate_client.sh   # GraphQL code generation
│   ├── post_codegen.py      # Post-generation processing
│   └── quick_api_check.py   # API health check
├── .github/                  # GitHub configuration
│   ├── workflows/           # CI/CD workflows
│   └── ISSUE_TEMPLATE/      # Issue templates
├── .serena/                  # Serena MCP configuration
│   ├── project.yml          # Project config
│   └── memories/            # Project memories
├── pyproject.toml           # Package configuration
├── mkdocs.yml               # Documentation config
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .gitignore              # Git ignore rules
├── .readthedocs.yml        # ReadTheDocs config
├── LICENSE                 # MIT license
├── README.md               # Project README
├── MANIFEST.in             # Package manifest
├── schema.graphql          # ESO Logs GraphQL schema
└── queries.graphql         # GraphQL queries

## Key Directories

### `/esologs` - Main Package
- Core implementation with modular architecture
- Mixins organize 42 API methods into logical groups
- Generated code isolated in `_generated/` subdirectory

### `/tests` - Comprehensive Test Suite
- 428 total tests across 4 complementary suites
- Each suite has specific purpose and requirements
- Shared fixtures in conftest.py

### `/docs` - Documentation
- MkDocs-based documentation site
- Comprehensive API reference
- Examples and guides

### `/scripts` - Development Tools
- Code generation automation
- API testing utilities
- Build and deployment scripts

## Important Files
- `pyproject.toml` - Package metadata and dependencies
- `mkdocs.yml` - Documentation configuration
- `.pre-commit-config.yaml` - Code quality automation
- `esologs/queries.py` - All GraphQL queries
- `tests/conftest.py` - Shared test fixtures
