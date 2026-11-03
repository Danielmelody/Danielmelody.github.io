# Maintaining the published blog

GitHub Pages publishes `master` at `/` to `https://yiminghu.me/`.
This repository contains Hugo output, including older pages that remain reachable
under `/posts/` and legacy tags. Keep those URLs and their content when updating
shared assets; a new Hugo build does not necessarily replace every older file.

All pages that use jQuery load `/lib/jquery/jquery-3.7.1.min.js`. It is the
unmodified official full distribution, including its license header. The older
3.2.1 copy allowed prototype pollution through deep `jQuery.extend` merges
([upstream explanation](https://blog.jquery.com/2019/04/10/jquery-3-4-0-released/)).
3.7.1 keeps compatibility with the existing theme and plugins. jQuery 3.x receives
critical security and bug fixes; a future 4.x migration needs a separate browser
and plugin compatibility assessment
([support policy](https://jquery.com/support/),
[4.0 breaking changes](https://blog.jquery.com/2026/01/17/jquery-4-0-0/)).

After generating or copying output into this repository, run:

```sh
python3 scripts/check-jquery.py
```

Run this check before each publication. It checks every HTML script reference,
the official library's SHA-256 digest, and vendored jQuery copies, so a later
generation that restores the old library fails the check. Update
both the generator's theme/static assets and any retained published pages when
changing the dependency. Keep this check when refreshing output.
The generator's source and deployment scripts are outside this published tree;
their repository relationship still needs confirmation before claiming that
upstream regeneration is fixed.
