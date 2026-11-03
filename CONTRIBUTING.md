# Contributing

Three people work in this repository. Each change uses one branch, one pull request, and one reviewer. Merge the pull request into `main`.

The remote is `[GitHub repository link]` until the repository exists. Add `[Luis GitHub username]` and `[Emanuel GitHub username]` as collaborators after that remote exists. From a clone of the repository, run these two commands.

```bash
gh repo add-collaborator [Luis GitHub username]
gh repo add-collaborator [Emanuel GitHub username]
```

The plan does not name a GitHub username for John Constantine C. Acuesta. In the commands below, replace `GITHUB_USERNAME_OF_JOHN` with his username. Do not invent one in this file.

## Clone the repository

Run this from the folder where you keep class work.

```bash
git clone [GitHub repository link]
```

Change into the folder that clone created. The later commands assume that folder is the current directory, and that `main` is checked out.

## Emanuel R. Ceniza on emanuel/api

John Constantine C. Acuesta is the reviewer.

```bash
git checkout -b emanuel/api
git add .
git commit -m "Add address lookup"
git push -u origin emanuel/api
gh pr create --base main --title "Add address lookup" --body "Header rules and provider fallback." --reviewer "GITHUB_USERNAME_OF_JOHN"
```

After John approves, merge into `main`.

```bash
gh pr merge --merge
```

## John Constantine C. Acuesta on john/ui

Luis Gabriel C. Araneta is the reviewer.

```bash
git checkout main
git pull
git checkout -b john/ui
git add .
git commit -m "Build the address card page"
git push -u origin john/ui
gh pr create --base main --title "Build the address card page" --body "Card, map, and quiz page." --reviewer "[Luis GitHub username]"
```

After Luis approves, merge into `main`.

```bash
gh pr merge --merge
```

## Luis Gabriel C. Araneta on luis/tests

John Constantine C. Acuesta is the reviewer.

```bash
git checkout main
git pull
git checkout -b luis/tests
git add .
git commit -m "Add pytest coverage for lookup and the page"
git push -u origin luis/tests
gh pr create --base main --title "Add pytest coverage" --body "Tests for lookup, roast, quiz, and the page." --reviewer "GITHUB_USERNAME_OF_JOHN"
```

After John approves, merge into `main`.

```bash
gh pr merge --merge
```

## John Constantine C. Acuesta on john/paper

Emanuel R. Ceniza is the reviewer.

```bash
git checkout main
git pull
git checkout -b john/paper
git add .
git commit -m "Add the project paper"
git push -u origin john/paper
gh pr create --base main --title "Add the project paper" --body "Project paper for Address Card." --reviewer "[Emanuel GitHub username]"
```

After Emanuel approves, merge into `main`.

```bash
gh pr merge --merge
```
