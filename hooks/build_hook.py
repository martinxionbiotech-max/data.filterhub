"""Remove CJK search-tokenizer assets after build (site is English-only)."""
import os
import logging

log = logging.getLogger("mkdocs")

def on_post_build(config, **kwargs):
    removed = []
    for name in ("lunr.zh.min.js", "lunr.ja.min.js", "tinyseg.js"):
        p = os.path.join(config.site_dir, "assets", "javascripts", "lunr", "min", name)
        p2 = os.path.join(config.site_dir, "assets", "javascripts", "lunr", name)
        for path in (p, p2):
            if os.path.isfile(path):
                os.remove(path)
                removed.append(name)
    if removed:
        log.info("CJK search assets removed: %s", ", ".join(removed))
