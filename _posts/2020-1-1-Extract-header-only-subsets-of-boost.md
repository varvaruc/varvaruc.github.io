Download boost and untar.
```
./bootstrap.sh 
./b2 tools/bcp
mkdir ../myboost
# This for example extract the tokenizer header and deps
./dist/bin/bcp tokenizer ../myboost/
```
Now `cd ../myboost` copy the boost directory and drop it into your project workspace.
