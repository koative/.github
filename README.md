# koative organization profile

The public profile displayed at **[github.com/koative](https://github.com/koative)** lives in [`profile/README.md`](profile/README.md).

It opens with a header carrying the koative logo and the line “We build software products, most of them open source.”, then lists the studio's public products with links to each website and repository, and ends with links to the studio, the founder and the contact page. There are no external badge services or automated activity feeds.

## Maintaining the profile

- Edit `profile/README.md` to update copy, products or links. Product one-liners come from https://koative.com/products.json. [`PRODUCT.md`](PRODUCT.md) has the content rules and [`DESIGN.md`](DESIGN.md) the visual ones.
- The header has light and dark variants, each with a desktop and a mobile layout. It is static.

To regenerate the SVG headers (font and brand paths are covered in [`assets/README.md`](assets/README.md)):

```sh
python3 -m pip install fonttools
python3 scripts/generate_header.py
```

The SVGs contain outlined lettering and need no remote fonts or JavaScript.
