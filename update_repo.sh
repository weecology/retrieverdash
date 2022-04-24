changed=0
git remote update && git status -uno | grep -q 'Your branch is behind' && changed=1
if [ $changed = 1 ]; then
    git reset --hard origin/main && git pull
    retriever ls 
    echo "Updated $(date), Commit $(git log -n 1 --pretty=format:"%h")"
else
    echo "Up-to-date $(date), Commit $(git log -n 1 --pretty=format:"%h")"
fi
