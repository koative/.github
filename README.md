# Koative organization profile

The compact public profile displayed at **[github.com/koative](https://github.com/koative)** lives in [`profile/README.md`](profile/README.md).

It introduces Koative using the studio’s existing blue–coral mark and “Software, made together.” line, then links to the studio and repository directory. There are no external badge services or automated activity feeds.

## Maintaining the profile

- Edit `profile/README.md` to update the studio and repository-directory links.
- Keep the header shallow so repositories remain easy to reach.
- Keep individual project listings out of the profile; GitHub shows the repositories below.
- The banner has light and dark variants, and its four-second line animation stops after one pass. Reduced-motion preferences disable the animation.

To regenerate the SVG headers:

```sh
python3 -m pip install fonttools brotli
python3 scripts/generate_header.py
```

The SVGs contain outlined lettering and need no remote fonts or JavaScript. Asset provenance and font licensing are documented in [`assets/README.md`](assets/README.md).
