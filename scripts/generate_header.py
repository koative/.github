"""Build koative's GitHub profile headers: the brand logo and headline, with type outlined to paths.

The logo is embedded from the brand SVG files and the lettering is outlined from the studio's
Clash Grotesk and Switzer TTFs. Neither lives in this repository; point the script at them with
--brand/--fonts or KOATIVE_BRAND_DIR/KOATIVE_FONT_DIR. The published SVGs contain only paths.
"""
import argparse
import os
import re
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
HEADLINE = 'We build software products, most of them open source.'
LABEL = 'Independent software studio'
THEMES = {
    # ground, ink, muted, logo file (wordmark colour that reads on the ground), glow strength
    'light': ('#f2f1ee', '#08080a', '#5c5b58', 'logo-void.svg', .34),
    'dark': ('#08080a', '#f2f1ee', '#a3a29e', 'logo-light.svg', .5),
}
GLOW = ('#2F3BFF', '#B44BD6', '#FF5B45')
# width, height, padding, logo height, headline size, headline lines, label size or None,
# and a (cx, cy, r) glow per GLOW colour, kept clear of the lettering
LAYOUTS = {
    '': (1000, 288, 56, 34, 50, ['We build software products,', 'most of them open source.'], 15,
         [(790, 350, 240), (915, 300, 220), (1010, 190, 200)]),
    '-mobile': (512, 240, 32, 26, 35, ['We build software', 'products, most of', 'them open source.'], None,
                [(320, -70, 170), (440, -40, 160), (530, 40, 150)]),
}


def number(value):
    return f'{value:.2f}'.rstrip('0').rstrip('.')


class Face:
    """A static TTF with pair kerning from its GPOS 'kern' feature."""

    def __init__(self, path):
        self.font = TTFont(path)
        self.glyphs, self.cmap = self.font.getGlyphSet(), self.font.getBestCmap()
        self.units = self.font['head'].unitsPerEm
        gpos = self.font['GPOS'].table
        lookups = {i for record in gpos.FeatureList.FeatureRecord if record.FeatureTag == 'kern'
                   for i in record.Feature.LookupListIndex}
        self.subtables = [table.ExtSubTable if lookup.LookupType == 9 else table
                          for i, lookup in enumerate(gpos.LookupList.Lookup) if i in lookups
                          for table in lookup.SubTable]

    def kern(self, left, right):
        for table in self.subtables:
            if left not in table.Coverage.glyphs:
                continue
            if table.Format == 1:
                pairs = table.PairSet[table.Coverage.glyphs.index(left)].PairValueRecord
                for pair in pairs:
                    if pair.SecondGlyph == right:
                        return getattr(pair.Value1, 'XAdvance', 0) or 0
            else:
                first = table.ClassDef1.classDefs.get(left, 0)
                second = table.ClassDef2.classDefs.get(right, 0)
                value = table.Class1Record[first].Class2Record[second].Value1
                return getattr(value, 'XAdvance', 0) or 0
        return 0

    def layout(self, text, tracking=0):
        names = [self.cmap[ord(char)] for char in text]
        x, placed = 0, []
        for i, name in enumerate(names):
            placed.append((name, x))
            x += self.glyphs[name].width + tracking * self.units
            if i + 1 < len(names):
                x += self.kern(name, names[i + 1])
        return placed, x - tracking * self.units

    def width(self, text, size, tracking=0):
        return self.layout(text, tracking)[1] * size / self.units

    def path(self, text, size, x, y, fill, tracking=0):
        scale = size / self.units
        pen = SVGPathPen(self.glyphs, ntos=number)
        for name, advance in self.layout(text, tracking)[0]:
            self.glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x + advance * scale, y)))
        return f'<path fill="{fill}" d="{pen.getCommands()}"/>'


def logo(brand, file, x, y, height):
    """Place a brand logo SVG unchanged, scaled to the given height."""
    source = (brand / file).read_text()
    box = [float(v) for v in re.search(r'viewBox="([^"]+)"', source).group(1).split()]
    inner = re.search(r'<svg[^>]*>(.*)</svg>', source, re.S).group(1)
    inner = re.sub(r'<title>.*?</title>', '', inner)
    scale = height / box[3]
    return (f'<g transform="translate({number(x)} {number(y)}) scale({scale:.6f}) '
            f'translate({number(-box[0])} {number(-box[1])})">{inner}</g>')


def header(fonts, brand, theme, layout):
    ground, ink, muted, logo_file, glow = THEMES[theme]
    width, height, pad, logo_height, size, lines, label_size, glows = LAYOUTS[layout]
    display, text = fonts['display'], fonts['text']
    mark = logo(brand, logo_file, pad, pad, logo_height)
    assert ' '.join(lines) == HEADLINE
    leading = size * 1.12
    last = height - pad - size * .06
    body = [display.path(line, size, pad, last - (len(lines) - 1 - i) * leading, ink, -.012)
            for i, line in enumerate(lines)]
    for line in lines:
        assert pad + display.width(line, size, -.012) <= width - pad, f'{line!r} overflows {layout or "desktop"}'
    if label_size:
        label_x = width - pad - text.width(LABEL, label_size)
        body.append(text.path(LABEL, label_size, label_x, pad + logo_height * .985, muted))
    gradients = '\n'.join(
        f'<radialGradient id="glow{i}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'
        f'<stop stop-color="{colour}" stop-opacity="{glow}"/><stop offset="1" stop-color="{colour}" stop-opacity="0"/>'
        '</radialGradient>' for i, (colour, (cx, cy, r)) in enumerate(zip(GLOW, glows)))
    fills = '\n'.join(f'<rect width="{width}" height="{height}" fill="url(#glow{i})"/>' for i in range(len(GLOW)))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">koative. {HEADLINE}</title>
<desc id="desc">The koative logo, a two-lobe mark in a blue, violet and coral gradient beside the lowercase wordmark, above the headline. A soft glow in the same gradient fills one corner.</desc>
<defs>
<clipPath id="card"><rect width="{width}" height="{height}" rx="18"/></clipPath>
{gradients}
</defs>
<g clip-path="url(#card)">
<rect width="{width}" height="{height}" fill="{ground}"/>
{fills}
{mark}
{chr(10).join(body)}
</g>
</svg>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--fonts', type=Path, default=Path(os.environ.get(
        'KOATIVE_FONT_DIR', '/home/hermes/dev/koative/src/assets/fonts')))
    parser.add_argument('--brand', type=Path, default=Path(os.environ.get(
        'KOATIVE_BRAND_DIR', '/home/hermes/dev/koative/brand/svg')))
    args = parser.parse_args()
    fonts = {'display': Face(args.fonts / 'ClashGrotesk-500.ttf'), 'text': Face(args.fonts / 'Switzer-400.ttf')}
    for theme in THEMES:
        for layout in LAYOUTS:
            out = ROOT / f'assets/koative-header-{theme}{layout}.svg'
            out.write_text(header(fonts, args.brand, theme, layout))
            print(f'{out.relative_to(ROOT)}  {out.stat().st_size:,} bytes')


if __name__ == '__main__':
    main()
