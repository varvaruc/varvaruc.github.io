---
layout: post
title: Bash command line snippets
---

Searches for a file pattern and renames the part in the middle.

Tip: Use `rename -n` when first trying this out, the replace with `rename -v`.

```
avarvaruc@work-pc:~/$ find . -type f -iname '*_any_any_domestic_managed.str' -exec rename -v 's/(.)_domestic_(.)/$1_any$2/i' {} \;
./es_any_any_domestic_managed.str renamed as ./es_any_any_any_managed.str
./fr_any_any_domestic_managed.str renamed as ./fr_any_any_any_managed.str
./en_any_any_domestic_managed.str renamed as ./en_any_any_any_managed.str

```