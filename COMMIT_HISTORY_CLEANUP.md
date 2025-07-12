# Commit History Cleanup Instructions

## Overview
This document provides explicit instructions for cleaning up commit history to remove Claude attributions and ensure single-line commit messages throughout the repository.

## ⚠️ CRITICAL WARNINGS
- **This will rewrite ALL commit history**
- **All commit SHAs will change**
- **Anyone with local copies will need to re-clone**
- **This is a DESTRUCTIVE operation - create backups first**
- **Only execute when ALL active development is merged**

## Prerequisites
- All active feature branches merged into main development branches
- All pending work committed and pushed
- Team notified of upcoming history rewrite
- Backup repository created

## What Will Be Removed
- `Co-Authored-By: Claude <noreply@anthropic.com>`
- `🤖 Generated with [Claude Code](https://claude.ai/code)`
- Any references to `claude.ai/code`
- Any references to `noreply@anthropic.com`
- Multi-line commit messages converted to single line

## Step-by-Step Instructions

### Phase 1: Backup Everything
```bash
# Navigate to repository root
cd /path/to/esologs-python

# Create backup branch of current state
git branch backup-original-history

# Create backup remote (replace with actual backup repository URL)
git remote add backup-origin https://github.com/yourusername/esologs-python-backup.git
git push backup-origin --all --tags

# Verify backup was created
git branch -a
```

### Phase 2: Verify Current State
```bash
# Check for Claude attributions in commit messages
echo "=== Current Claude attributions found ==="
git log --all --grep="Claude" --oneline
git log --all --grep="anthropic" --oneline
git log --all --grep="🤖" --oneline

# Count total commits that will be affected
echo "=== Commits with multi-line messages ==="
git log --pretty=format:"%H %s" | grep -v "^[a-f0-9]\{40\} [^[:space:]].*[^[:space:]]$" | wc -l

# Show example of problematic commits
echo "=== Example problematic commit ==="
git log --format=fuller -1 $(git log --grep="Claude" --format="%H" | head -1)
```

### Phase 3: Clean Commit Messages
```bash
# Clean all branches with filter-branch
git filter-branch --msg-filter '
    # Remove Claude attributions line by line
    sed "/Co-Authored-By: Claude <noreply@anthropic\.com>/d" |
    sed "/🤖 Generated with \[Claude Code\]/d" |
    sed "/claude\.ai\/code/d" |
    sed "/noreply@anthropic\.com/d" |
    sed "/^\s*$/d" |  # Remove empty lines
    
    # Take only the first line (single-line commit message)
    head -1 |
    
    # Clean up whitespace
    sed "s/^[[:space:]]*//" |
    sed "s/[[:space:]]*$//"
' --all

# Alternative if the above fails (more conservative):
git filter-branch --msg-filter '
    head -1 | sed "s/Co-Authored-By: Claude.*//g" | sed "s/🤖 Generated.*//g" | sed "s/^[[:space:]]*//" | sed "s/[[:space:]]*$//"
' --all
```

### Phase 4: Clean Up Git Internals
```bash
# Remove filter-branch backup refs
git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d

# Clean up repository
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Phase 5: Verification
```bash
# Verify Claude attributions are gone
echo "=== Checking for remaining Claude references ==="
git log --all --grep="Claude" --oneline
git log --all --grep="anthropic" --oneline
git log --all --grep="🤖" --oneline

# Check commit message format
echo "=== Sample of cleaned commit messages ==="
git log --oneline -10

# Verify no multi-line commit messages remain
echo "=== Checking for multi-line commits ==="
git log --pretty=format:"%H|||%B" | grep -c "|||.*\\n.*\\n"

# Show statistics
echo "=== Cleanup Statistics ==="
echo "Total commits: $(git rev-list --all --count)"
echo "Branches: $(git branch -a | wc -l)"
echo "Size before cleanup: $(du -sh .git)"
```

### Phase 6: Force Push (POINT OF NO RETURN)
```bash
# ⚠️ WARNING: This step cannot be undone easily
# Verify you have backups before proceeding

echo "=== FINAL WARNING ==="
echo "This will force-push rewritten history to all branches"
echo "Type 'YES I HAVE BACKUPS' to continue:"
read confirmation

if [ "$confirmation" = "YES I HAVE BACKUPS" ]; then
    # Force push all branches
    git push origin --force --all
    
    # Force push tags
    git push origin --force --tags
    
    echo "✅ History cleanup complete"
    echo "📧 Notify all team members to re-clone the repository"
else
    echo "❌ Cleanup aborted - create backups first"
    exit 1
fi
```

### Phase 7: Team Notification
After force pushing, immediately notify all team members:

```bash
# Send notification (adapt to your communication method)
echo "🚨 REPOSITORY HISTORY REWRITTEN 🚨
- All commit SHAs have changed
- Please re-clone the repository: git clone <repo-url>
- Delete old local copies to avoid confusion
- All Claude attributions have been removed
- All commit messages are now single-line format"
```

## Recovery Instructions (If Something Goes Wrong)

### If cleanup fails partway through:
```bash
# Reset to backup branch
git checkout backup-original-history
git branch -D main v2-dev  # Delete broken branches
git checkout -b main backup-original-history
git checkout -b v2-dev backup-original-history

# Or restore from backup remote
git fetch backup-origin
git reset --hard backup-origin/main
```

### If force push was successful but issues discovered:
```bash
# Restore from backup remote
git fetch backup-origin
git reset --hard backup-origin/main
git push origin --force main

# Notify team of restoration
echo "Repository restored to pre-cleanup state"
```

## Alternative Approach (If filter-branch fails)

### Using BFG Repo Cleaner:
```bash
# Download BFG (Java required)
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

# Create replacement file
cat > claude-removals.txt << 'EOF'
Co-Authored-By: Claude <noreply@anthropic.com>===>
🤖 Generated with [Claude Code](https://claude.ai/code)===>
claude.ai/code===>
noreply@anthropic.com===>
EOF

# Run BFG cleaner
java -jar bfg-1.14.0.jar --replace-text claude-removals.txt .git

# Clean up
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# Force push
git push origin --force --all
```

## Validation Checklist
- [ ] All backups created and verified
- [ ] No Claude attributions in commit messages
- [ ] All commit messages are single-line
- [ ] All branches pushed successfully
- [ ] Team notified to re-clone
- [ ] Documentation updated (if needed)
- [ ] CI/CD pipelines still working
- [ ] All critical branches preserved

## Timing Considerations
- **Best time**: After major release or milestone
- **Avoid**: During active development periods
- **Notify**: Give team 24-48 hour notice
- **Schedule**: Weekend or low-activity period

## Support Information
- **Backup location**: [Document where backups are stored]
- **Emergency contact**: [Who to contact if issues arise]
- **Rollback plan**: Follow recovery instructions above

---

**Note**: This cleanup should only be performed when:
1. All active development is merged and stable
2. All team members are notified and prepared
3. Complete backups are verified and accessible
4. You have tested the process on a clone first

**Remember**: Once history is rewritten and force-pushed, there's no easy way back. The backup branches and remote repositories are your only safety net.