# Flatfish GNV — website

A five-page site for **Flatfish GNV**, the from-scratch doughnut shop at
308 NW 5th Ave, Gainesville, Florida. They have no website today — only
[Instagram](https://www.instagram.com/flatfish_gnv/).

Open `index.html` in a browser. Everything is relative, so it works straight off
the disk — no server needed.

## Pages

| Page | File | What's on it |
|---|---|---|
| Home | `index.html` | Hero, Google rating, what they make, current flavours, Instagram grid, hours |
| Flavours | `menu.html` | Current rotation, the year-round vegan glazed line, the Dagel, past flavours |
| Reviews | `reviews.html` | 4.7★ breakdown and nine real Google reviews |
| Visit | `visit.html` | Map, hours, routes from campus, how to beat the sellout |
| Our Story | `about.html` | Three years, from-scratch, the flounder |

Each nav item is its own page, as asked.

## How it's built

The HTML is **generated** — don't hand-edit the `.html` files at the root, they
get overwritten.

| File | Holds |
|---|---|
| `src/content.py` | every fact, flavour and review, each with its source noted |
| `src/_css.css` | the whole stylesheet |
| `src/gen.py` | page templates and the build |

```sh
python3 src/gen.py        # rewrites the five .html files
```

No dependencies, no build tools — just Python 3.

## Where the content came from

Checked 13–14 October 2026.

- **Rating, review text, address, hours** — the shop's Google Business listing.
  4.7 stars from 185 reviews (167 five-star). Reviews are verbatim extracts,
  trimmed to whole sentences and attributed by name.
- **Flavours, hours, owners, photographs** — [@flatfish_gnv](https://www.instagram.com/flatfish_gnv/).
  The flavour descriptions are their own words from the 29 Sep and 3 Oct 2026
  posts and from the printed poster they photographed in June.
- **Photographs** — all theirs, pulled from their Instagram posts and cropped.
  `src/../img/flounder.png` is their flounder drawing lifted off that poster.

## Things to confirm with Patty and Michael

1. **Phone number.** Their Google listing has none; two aggregator sites list
   (352) 792-6773, which I could not verify, so **no phone number appears on the
   site**. Add it to `content.py` if it is right.
2. **Prices.** Not shown anywhere — I had no reliable source. Google says
   "$1–10 per person".
3. **Hours.** Google, their Instagram bio and their 6 Oct 2026 post all say
   Saturday and Sunday only, 10am–1:30pm or sellout. Friday is listed as closed.
4. **The flavour rotation** on `menu.html` is the 2–18 October board. It needs
   updating every fortnight — that is the one part of the site that goes stale.
   It lives at the top of `src/content.py` (`ROTATION_LABEL`, `BRIOCHE`,
   `GLAZED_NEW`).
5. **The flounder story** in `about.html` is written as a guess at why the shop
   is called Flatfish. Worth replacing with the real reason.

## Deploying

Repo: <https://github.com/michaeljpreviti-ops/flatfish-site>

The Vercel project is connected to that repo, so **pushing to `main` deploys**.
Nothing to run by hand:

```sh
OUTDIR=. python3 src/gen.py     # only if you changed src/
git commit -am "..." && git push
```

Import settings, if the project is ever recreated: framework **Other**, no build
command, output directory the repo root. `vercel.json` handles clean URLs and
image caching.

`src/deploy.py` is a fallback that pushes the folder straight to Vercel's REST
API without Node or the CLI — it needs `$VERCEL_TOKEN` or `~/.vercel_token`:

```sh
python3 src/deploy.py flatfish-gnv
```

## Before it goes live

- Set `SITE_URL` in `src/content.py` to the real domain and rebuild. While it is
  empty the pages deliberately ship no `canonical`/`og:url`.
