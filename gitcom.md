
## Setup & Configuration
```bash
# Set user info
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Check configuration
git config --list
```

## Basic Workflow
```bash
# Initialize a new repository
git init

# Clone an existing repository
git clone <repository-url>

# Check status of files
git status

# Add files to staging
git add <file>           # Add specific file
git add .               # Add all files
git add *.js            # Add all JS files

# Commit changes
git commit -m "Commit message"

# View commit history
git log
git log --oneline       # Compact view
```

## Branching
```bash
# List branches
git branch

# Create new branch
git branch <branch-name>

# Switch to branch
git checkout <branch-name>

# Create and switch to new branch
git checkout -b <branch-name>

# Delete branch
git branch -d <branch-name>
```

## Remote Repositories
```bash
# Add remote repository
git remote add origin <repository-url>

# Push to remote
git push origin <branch-name>
git push -u origin main  # Set upstream branch

# Pull from remote
git pull origin <branch-name>

# Fetch changes without merging
git fetch origin
```

## Merging & Rebasing
```bash
# Merge branch into current branch
git merge <branch-name>

# Rebase current branch onto another
git rebase <branch-name>

# Resolve merge conflicts
git mergetool
```

## Undoing Changes
```bash
# Undo changes in working directory
git checkout -- <file>

# Unstage files
git reset <file>

# Amend last commit
git commit --amend

# Revert a commit
git revert <commit-hash>

# Reset to previous commit
git reset --hard <commit-hash>
```

## Stashing
```bash
# Stash changes
git stash

# List stashes
git stash list

# Apply last stash
git stash apply

# Apply and remove stash
git stash pop

# Clear all stashes
git stash clear
```

## Tagging
```bash
# Create tag
git tag <tag-name>

# Create annotated tag
git tag -a <tag-name> -m "Tag message"

# Push tags to remote
git push --tags
```

## Useful Inspection
```bash
# Show differences
git diff
git diff --staged

# Show specific commit
git show <commit-hash>

# View remote URLs
git remote -v
```

## Common Workflows

### Daily workflow:
```bash
git status
git add .
git commit -m "message"
git pull origin main    # get latest changes
git push origin main
```

### Feature branch workflow:
```bash
git checkout -b feature-branch
# make changes
git add .
git commit -m "feature description"
git push origin feature-branch
# create pull request on GitHub/GitLab
```
