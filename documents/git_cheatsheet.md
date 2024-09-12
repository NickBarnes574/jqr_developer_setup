# These are the typical `git` commands I use on a day-to-day basis:

1. **`git checkout -b branch_name`**
   - **Description**: This command is used to create a new branch and switch to it immediately. `branch_name` is the name of the new branch.
   - **When to Use**: When you want to start working on a new feature or a bug fix and need a separate branch for it.

2. **`git checkout branch`**
   - **Description**: This command switches your working directory to the branch specified by `branch`. It doesn't create a new branch, just switches to an existing one.
   - **When to Use**: When you need to switch your focus to a different branch that already exists, for example, from `develop` to `feature-x`.

3. **`git add .`**
   - **Description**: Adds all changed files in your current directory (and all subdirectories) to the staging area.
   - **When to Use**: When you have made changes to your code and are ready to stage these changes for a commit.

4. **`git commit -m "commit message"`**
   - **Description**: Commits the staged changes to your local repository with a message describing what the commit is about.
   - **When to Use**: After staging your changes with `git add`, and you want to record your changes in the repository's history.

5. **`git push -u origin branch_name`**
   - **Description**: Pushes the commits from your local branch `branch_name` to the remote repository (typically named `origin`). The `-u` flag sets the upstream for the branch, which makes future pushes and pulls easier.
   - **When to Use**: When you want to update the remote repository with commits you have made locally and you're pushing this branch for the first time.

6. **`git push`**
   - **Description**: Pushes your committed changes to the remote repository. This is typically used after the initial push with `-u`.
   - **When to Use**: When you have new commits in your local branch that you want to be available in the remote repository.

7. **`git merge --no-ff branch_to_merge -m "merge message"`**
   - **Description**: Merges the specified branch (`branch_to_merge`) into your current branch. The `--no-ff` flag creates a merge commit even if a fast-forward merge is possible, preserving history of the merged branch.
   - **When to Use**: When you have finished working on a feature or fix in a separate branch and want to merge it back into a main branch (like `master` or `develop`).

8. **`git pull`**
   - **Description**: Fetches changes from the remote repository and merges them into your current branch.
   - **When to Use**: To update your local branch with changes that others have made in the remote repository.

9. **`git pull --all`**
   - **Description**: Fetches changes from all branches from the remote repository but merges only into the current branch.
   - **When to Use**: When you want to update your local repository with all the changes from the remote, across all branches.

10. **`git stash`**
    - **Description**: Temporarily stores all modified tracked files and staged changes in a stash, and reverts the working directory to match the HEAD commit.
    - **When to Use**: When you need to switch branches, but you're not ready to commit your current work.

11. **`git stash pop`**
    - **Description**: Applies the changes from the most recent stash to your current working directory and then removes the stashed changes.
    - **When to Use**: After completing work on another branch and you want to go back and continue working on your stashed changes.

# This is a sample git workflow I would probably use if I was starting the JQR from scratch:

1. **Create and Switch to `dev` Branch**
   - Start from the `main` branch.
     ```
     git checkout main
     ```
   - Create and switch to a new branch called `dev`.
     ```
     git checkout -b dev
     ```

2. **Make Infrastructure-Related Commits**
   - Make the necessary changes for the infrastructure setup.
   - Stage and commit these changes. For example:
     ```
     git add .
     git commit -m "Set up initial project infrastructure"
     ```

3. **Create and Switch to `simple_calc` Branch**
   - Create and switch to a new branch called `simple_calc` based off `dev`.
     ```
     git checkout -b simple_calc
     ```

4. **Create and Switch to `cli_handler` Branch**
   - Create and switch to a new branch called `cli_handler` for your feature.
     ```
     git checkout -b cli_handler
     ```

5. **Make Commits on `cli_handler` Branch**
   - Implement the command line input functions.
   - Stage and commit your changes. For instance, make two commits:
     ```
     git add .
     git commit -m "Add basic CLI structure"
     git add .
     git commit -m "Implement argument parsing"
     ```

6. **Push `cli_handler` Branch to Remote**
   - Push the `cli_handler` branch to the remote repository.
     ```
     git push -u origin cli_handler
     ```

7. **Merge `cli_handler` into `simple_calc`**
   - Switch back to the `simple_calc` branch.
     ```
     git checkout simple_calc
     ```
   - Merge the `cli_handler` branch. Since it's a feature branch, a non-fast-forward merge (`--no-ff`) could be appropriate to preserve the feature branch history.
     ```
     git merge --no-ff cli_handler -m "Merge CLI handler feature"
     ```

8. **Push the Merged `simple_calc` Branch**
   - Push the changes from the `simple_calc` branch, including the merged commits from `cli_handler`, to the remote repository.
     ```
     git push origin simple_calc
     ```
