# Git Worktree Setup for Parallel Development

## Overview
Git worktrees have been created to allow 5 agents to work independently on different API documentation sections without conflicts.

## Worktree Structure

### Main Repository
- **Location**: `/home/nknowles/projects/esologs-python/esologs-python/`
- **Branch**: `v2/update-main-before-refactor`
- **Status**: Main development branch (do not work here during parallel development)

### Agent Worktrees

| Agent | Worktree Location | Branch | Plan File | Task |
|-------|-------------------|--------|-----------|------|
| Agent 1 | `/home/nknowles/projects/esologs-python/character-data-worktree/` | `character-data-work` | `plan-character-data.md` | Character Data API |
| Agent 2 | `/home/nknowles/projects/esologs-python/guild-data-worktree/` | `guild-data-work` | `plan-guild-data.md` | Guild Data API |
| Agent 3 | `/home/nknowles/projects/esologs-python/world-data-worktree/` | `world-data-work` | `plan-world-data.md` | World Data API |
| Agent 4 | `/home/nknowles/projects/esologs-python/report-analysis-worktree/` | `report-analysis-work` | `plan-report-analysis.md` | Report Analysis API |
| Agent 5 | `/home/nknowles/projects/esologs-python/report-search-worktree/` | `report-search-work` | `plan-report-search.md` | Report Search API |

## Instructions for Agents

### 1. Navigate to Your Assigned Worktree
```bash
cd /home/nknowles/projects/esologs-python/[your-worktree-name]
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Set Environment Variables
```bash
export ESOLOGS_ID="9f59cb5f-fabd-47e6-9529-f9797d5b38b2"
export ESOLOGS_SECRET="6hpMm9nbbfPKqF589dg8l16kxNV8jzFlERDXQIhl"
```

### 4. Read Your Plan File
Each worktree contains its specific plan file with complete instructions:
- `character-data-worktree/plan-character-data.md`
- `guild-data-worktree/plan-guild-data.md`
- `world-data-worktree/plan-world-data.md`
- `report-analysis-worktree/plan-report-analysis.md`
- `report-search-worktree/plan-report-search.md`

### 5. Work Independently
- Each agent works in their own worktree
- All changes are isolated to your branch
- No conflicts between agents
- Follow the 5-phase workflow in your plan file

### 6. Commit and Push When Complete
```bash
# Stage your changes
git add docs/api-reference/[section]-data.md tests/docs/test_[section]_examples.py

# Commit with single-line message (NO AI attribution)
git commit -m "Add [section] data API reference documentation"

# Push your branch
git push origin [your-branch-name]
```

## Expected Output Files (Per Agent)

Each agent should create:
- `docs/api-reference/[section]-data.md` - Complete API reference documentation
- `tests/docs/test_[section]_examples.py` - Comprehensive test suite

## Files to Create by Section

| Section | Documentation File | Test File |
|---------|-------------------|-----------|
| Character | `docs/api-reference/character-data.md` | `tests/docs/test_character_data_examples.py` |
| Guild | `docs/api-reference/guild-data.md` | `tests/docs/test_guild_data_examples.py` |
| World | `docs/api-reference/world-data.md` | `tests/docs/test_world_data_examples.py` |
| Report Analysis | `docs/api-reference/report-analysis.md` | `tests/docs/test_report_analysis_examples.py` |
| Report Search | `docs/api-reference/report-search.md` | `tests/docs/test_report_search_examples.py` |

## Quality Standards

All agents must follow the established patterns:
- ✅ **Table format**: Follow `docs/api-reference/game-data.md` exactly
- ✅ **Type validation**: Verify ALL types against live API responses
- ✅ **Executable examples**: Every code block must be copy-pasteable
- ✅ **Real outputs**: Include actual command results
- ✅ **Complete imports**: All examples must work without modification
- ✅ **Test coverage**: Every example must have corresponding tests

## Conflict Prevention

Since each agent works in a separate worktree:
- **No file conflicts** - each agent creates different files
- **No merge conflicts** - branches are independent
- **No coordination needed** - agents can work simultaneously
- **Clean integration** - all branches can be merged independently

## Integration After Completion

Once all agents complete their work:
1. Each branch gets merged independently into `v2/update-main-before-refactor`
2. Worktrees can be cleaned up
3. All documentation will be integrated seamlessly

## Support Information

- **Virtual Environment**: Each worktree has its own `venv/` directory
- **API Credentials**: Working credentials provided in all plan files
- **Reference Examples**: Existing `game-data.md` and `system.md` for patterns
- **CSS Styling**: Already configured in `docs/stylesheets/extra.css`

## Verification Commands

Each agent should run these before committing:
```bash
# Test your documentation
pytest tests/docs/test_[section]_examples.py -v

# Build documentation
mkdocs build --clean

# Run all doc tests to ensure no regressions
pytest tests/docs/ -v
```

This setup enables true parallel development with zero coordination overhead between agents.