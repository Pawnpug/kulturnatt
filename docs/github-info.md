# kulturnatt

## Github Flow

### 1. Pull the latest `main`

Make sure your local `main` is up to date before starting new work.

```bash
git checkout main
git pull origin main
```

### 2. Create a new branch

```bash
git checkout -b <branch-name>
```

### 3. Make your changes

Edit files, then check what you've changed.

```bash
git status
git diff
```

### 4. Stage and commit

Stage the files you want to include, then commit with a clear message.

```bash
git add <file1> <file2>
git commit -m "Short, descriptive message"
```

### 5. Push the branch to GitHub

The first time you push a new branch, use `-u` to set the upstream.

```bash
git push -u origin <branch-name>
```

On later pushes to the same branch, just run:

```bash
git push
```

### 6. Open a pull request

Go to the repository on GitHub and open a pull request from your branch into `main`. Request a review, address feedback, then merge once approved.

### 7. Clean up

After the PR is merged, sync your local `main` and delete the old branch.

```bash
git checkout main
git pull origin main
git branch -d <branch-name>
```
