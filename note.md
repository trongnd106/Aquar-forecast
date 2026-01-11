### Xu ly sub-module handle-file
```
git rm --cached handle-file
rm -rf .git/modules/handle-file
git config -f .gitmodules --remove-section submodule.handle-file
git add handle-file
git commit -m "Convert handle-file from submodule to normal directory"
```
