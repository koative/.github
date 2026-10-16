# Profile assets

- **Koative mark:** the original vector geometry and blue `#2F3BFF`, violet `#B44BD6`, coral `#FF5B45` palette from the public header at [koative.com](https://koative.com), used for Koative’s own organization profile.
- **Copy:** “Software, made together.” is the studio’s existing public tagline.
- **Lettering:** Manrope, distributed under the SIL Open Font License in `Manrope-OFL.txt`. The local WOFF2 is used only by the source generator; the published SVGs contain outlined paths. Font source: https://fonts.gstatic.com/s/manrope/v20/xn7gYHE41ni1AdIRggexSg.woff2
- **Animation:** original SVG/CSS line animation, one four-second pass, with `prefers-reduced-motion` support. All graphics are local repository assets.

`profile-header-contained-light.svg` and `profile-header-contained-dark.svg` share a 1000 × 128 view box. The `-mobile` variants use 512 × 128 to keep the lettering readable on phones. Regenerate them with `scripts/generate_header.py`.
