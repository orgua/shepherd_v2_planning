Create branch from current active branch

    git branch newfeature
    git checkout newfeature

Overwrite master with feature-branch

    git checkout feature
    git merge -s ours master
    git checkout master
    git merge feature

Show branches

    git show-branch

Delete feature-Branch

git branch -D feature

Overwrite "faulty" feature-branch with remote one

    .. delete local branch NOT remote
    git fetch --all
    git checkout feature
