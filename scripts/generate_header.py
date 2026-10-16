"""Build compact SVG headers from Koative's public mark and licensed outlined type."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
ROOT = Path(__file__).resolve().parents[1]
MARK = 'M28 26A24 24 0 0 0 28 74C38 74 44 62 50 62C56 62 62 74 72 74A24 24 0 0 0 72 26C62 26 56 38 50 38C44 38 38 26 28 26Z'

def lettering(text, size, weight, x, y, color, tracking=0):
    font = TTFont(ROOT / 'assets/manrope.woff2')
    if 'fvar' in font:
        font = instantiateVariableFont(font, {'wght': weight})
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    units, advance, paths = font['head'].unitsPerEm, 0, []
    for char in text:
        glyph = glyphs[cmap[ord(char)]]
        pen = SVGPathPen(glyphs)
        glyph.draw(pen)
        paths.append(f'<path transform="translate({advance} 0)" d="{pen.getCommands()}"/>')
        advance += glyph.width + units * tracking
    scale = size / units
    return f'<g fill="{color}" transform="translate({x} {y}) scale({scale} {-scale})">'+''.join(paths)+'</g>'

for mode, paper, ink, secondary in [('light', '#f5f6fa', '#171820', '#505362'), ('dark', '#0d1017', '#f3f4f9', '#b4bacb')]:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 128" role="img" aria-labelledby="title desc">
<title id="title">Koative — Software, made together.</title>
<desc id="desc">The Koative blue and coral mark, with a brief animated connecting line. Motion stops after four seconds and is disabled for reduced-motion preferences.</desc>
<defs>
  <linearGradient id="brand" x1="4" x2="96" y1="0" y2="0" gradientUnits="userSpaceOnUse"><stop offset=".36" stop-color="#2F3BFF"/><stop offset=".5" stop-color="#B44BD6"/><stop offset=".64" stop-color="#FF5B45"/></linearGradient>
  <clipPath id="frame"><rect width="1000" height="128" rx="12"/></clipPath>
</defs>
<style>
.trace {{stroke-dasharray:18 82;stroke-dashoffset:0;animation:connect 4s cubic-bezier(.16,1,.3,1) 1;}}
@keyframes connect {{from {{stroke-dashoffset:100}} to {{stroke-dashoffset:0}}}}
@media(prefers-reduced-motion:reduce){{.trace{{animation:none}}}}
</style>
<g clip-path="url(#frame)">
<rect width="1000" height="128" fill="{paper}"/>
<g transform="translate(25 17) scale(.56)"><path d="{MARK}" fill="url(#brand)"/></g>
{lettering('koative', 36, 700, 91, 59, ink, -.035)}
{lettering('Software, made together.', 21, 450, 28, 99, secondary, -.01)}
<g transform="translate(681 -88) scale(3)">
  <path d="{MARK}" fill="url(#brand)" opacity=".09"/>
  <path d="{MARK}" fill="none" stroke="url(#brand)" stroke-width=".7" opacity=".34"/>
  <path class="trace" d="{MARK}" pathLength="100" fill="none" stroke="url(#brand)" stroke-width="1.4" stroke-linecap="round"/>
</g>
</g>
</svg>'''
    (ROOT / f'assets/profile-header-{mode}.svg').write_text(svg)
    mobile = svg.replace('0 0 1000 128', '0 0 512 128').replace('width="1000"', 'width="512"').replace('translate(681 -88)', 'translate(390 -88)')
    (ROOT / f'assets/profile-header-{mode}-mobile.svg').write_text(mobile)
print('Generated both 1000 × 128 headers.')
