#!/usr/bin/env python3
"""Builds the Flatfish GNV site. Run it, then open ../index.html."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *   # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.normpath(os.path.join(HERE, '..', os.environ.get('OUTDIR', '.')))
CSS  = open(os.path.join(HERE, '_css.css'), encoding='utf-8').read()

PAGES = [('index', 'Home', 'index.html'),
         ('menu',  'Flavours', 'menu.html'),
         ('reviews', 'Reviews', 'reviews.html'),
         ('visit', 'Visit', 'visit.html'),
         ('about', 'Our Story', 'about.html')]

# ---------------------------------------------------------------- icons
I = {
 'pin':   '<path d="M12 2C8.1 2 5 5.1 5 9c0 5.2 7 13 7 13s7-7.8 7-13c0-3.9-3.1-7-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/>',
 'clock': '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm.9 10.6-3.6 2.3-.8-1.3 3-1.9V6.5h1.4v6.1z"/>',
 'star':  '<path d="m12 17.3-6.2 3.7 1.7-7-5.4-4.7 7.1-.6L12 2l2.8 6.7 7.1.6-5.4 4.7 1.7 7z"/>',
 'dir':   '<path d="M21.7 11.3 12.7 2.3a1 1 0 0 0-1.4 0l-9 9a1 1 0 0 0 0 1.4l9 9a1 1 0 0 0 1.4 0l9-9a1 1 0 0 0 0-1.4zM13 15v-2.5h-3V15l-3-3.5L10 8v2.5h4V15h-1z"/>',
 'ig':    '<path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.3 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2 0-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.8A6 6 0 1 0 12 18a6 6 0 0 0 0-12zm0 9.9A3.9 3.9 0 1 1 12 8.2a3.9 3.9 0 0 1 0 7.7zm7.6-10.3a1.4 1.4 0 1 1-2.8 0 1.4 1.4 0 0 1 2.8 0z"/>',
 'fb':    '<path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.7-3.9 1.1 0 2.2.2 2.2.2v2.4h-1.2c-1.2 0-1.6.8-1.6 1.6V12h2.7l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z"/>',
 'menu':  '<path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/>',
 'leaf':  '<path d="M20 3C9 3 4 8.5 4 15c0 2 .6 3.7 1.6 5L4 21.6 5.4 23l1.7-1.7C8.4 22.4 10.1 23 12 23c6.5 0 12-5 12-16 0-2-2-4-4-4zM12 21c-1.4 0-2.6-.4-3.5-1.1l9-9-1.4-1.4-9 9A5.9 5.9 0 0 1 6 15c0-5.3 4-10 14-10 1 0 2 1 2 2 0 10-4.7 14-10 14z"/>',
 'bolt':  '<path d="M13 2 4.5 13.5H11l-1 8.5L19.5 10H13z"/>',
}
def ico(k): return '<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % I[k]


def stars(n=5, of=5):
    out = []
    for i in range(of):
        out.append('<svg viewBox="0 0 24 24" aria-hidden="true"%s>%s</svg>'
                   % ('' if i < n else ' class="off"', I['star']))
    return '<span class="stars">%s</span>' % ''.join(out)


def tag(kind):
    if kind == 'vegan':
        return '<span class="card__tag card__tag--vegan flav__t">Plant-based</span>'
    if kind == 'savory':
        return '<span class="card__tag card__tag--savory flav__t">Savoury</span>'
    return ''


def flavour_list(items):
    rows = ''.join(
        '<div class="flav"><div class="flav__n">%s</div>'
        '<div class="flav__d">%s</div>%s</div>' % (n, d, tag(k))
        for n, d, k in items)
    return '<div class="flavours">%s</div>' % rows


# ----------------------------------------------------------------- shell
def head(key):
    nav = ''.join('<a href="%s"%s>%s</a>'
                  % (h, ' aria-current="page"' if k == key else '', l)
                  for k, l, h in PAGES)
    return """<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap topbar__in">
  <span class="topbar__i">{pin} {a1}, Gainesville</span>
  <span class="topbar__i">{clock} {hrs}</span>
  <span class="topbar__sp"></span>
  <a class="topbar__i" href="{ig}" target="_blank" rel="noopener">{igi} {handle}</a>
</div></div>
<header class="mast"><div class="wrap mast__in">
  <a class="brand" href="index.html" aria-label="{name} — home">
    <img src="img/flounder.png" alt="" width="1129" height="311">
    <span class="brand__txt">
      <span class="brand__a">{wa}</span>
      <span class="brand__b">{wb}</span>
    </span>
  </a>
  <span class="mast__sp"></span>
  <button class="navtoggle" id="navtoggle" aria-expanded="false" aria-controls="nav">{mn} Menu</button>
  <nav class="nav" id="nav" aria-label="Main">{nav}</nav>
</div></header>""".format(nav=nav, a1=ADDR1, hrs=HOURS_SHORT, ig=IG_URL, handle=IG_HANDLE,
                          name=NAME, wa=WORDMARK_A, wb=WORDMARK_B,
                          pin=ico('pin'), clock=ico('clock'), igi=ico('ig'), mn=ico('menu'))


FOOT = """<section class="cta"><div class="wrap">
  <div>
    <h2>Weekends only. Until they&rsquo;re gone.</h2>
    <p>Doors at 10am Saturday and Sunday. The board changes every two weeks — Instagram has
       what&rsquo;s on it right now.</p>
  </div>
  <div class="btnrow">
    <a class="btn btn--ink btn--lg" href="{maps}" target="_blank" rel="noopener">{dir} Get directions</a>
    <a class="btn btn--ghost btn--lg" href="{ig}" target="_blank" rel="noopener">{igi} See this week</a>
  </div>
</div></section>
<footer class="foot"><div class="wrap">
  <div class="foot__grid">
    <div class="foot__brand">
      <img src="img/flounder.png" alt="" width="1129" height="311">
      <div class="foot__wm">{wa} {wb}</div>
      <p>{tag}</p>
      <p>{a1}<br>{a2}</p>
      <div class="soc">
        <a href="{ig}" target="_blank" rel="noopener" aria-label="{name} on Instagram">{igi}</a>
        <a href="{fb}" target="_blank" rel="noopener" aria-label="{name} on Facebook">{fbi}</a>
        <a href="{place}" target="_blank" rel="noopener" aria-label="{name} on Google Maps">{sti}</a>
      </div>
    </div>
    <div><h4>Eat</h4><ul>
      <li><a href="menu.html">This fortnight&rsquo;s flavours</a></li>
      <li><a href="menu.html#glazed">Plant-based glazed</a></li>
      <li><a href="menu.html#dagel">The Dagel</a></li>
      <li><a href="menu.html#past">Flavours we&rsquo;ve run</a></li>
    </ul></div>
    <div><h4>Visit</h4><ul>
      <li><a href="visit.html">Hours &amp; directions</a></li>
      <li><a href="visit.html#getting-there">From campus</a></li>
      <li><a href="visit.html#tips">Beat the sellout</a></li>
      <li><a href="{maps}" target="_blank" rel="noopener">Open in Maps</a></li>
    </ul></div>
    <div><h4>More</h4><ul>
      <li><a href="about.html">Our story</a></li>
      <li><a href="reviews.html">Reviews ({rating}&#9733;)</a></li>
      <li><a href="{ig}" target="_blank" rel="noopener">Instagram {handle}</a></li>
      <li><a href="{fb}" target="_blank" rel="noopener">Facebook</a></li>
    </ul></div>
  </div>
  <div class="foot__bar">
    <span>&copy; {yr} {name}. Baked in Gainesville, Florida.</span>
    <span>{hrs}</span>
  </div>
</div></footer>
<script>
(function(){{
  var t=document.getElementById('navtoggle'),n=document.getElementById('nav');
  if(t&&n){{t.addEventListener('click',function(){{
    var o=n.classList.toggle('is-open');t.setAttribute('aria-expanded',o?'true':'false');
  }});}}
  // mark today's row in any hours table, and say whether the door is open
  var d=new Date(),day=d.getDay(),rows=document.querySelectorAll('[data-day]');
  rows.forEach(function(r){{ if(+r.dataset.day===day) r.classList.add('is-today'); }});
  var live=document.getElementById('open-now');
  if(live){{
    var mins=d.getHours()*60+d.getMinutes(), weekend=(day===0||day===6);
    var open=weekend&&mins>=600&&mins<810;
    live.textContent=open?'Open now until 1:30pm':(weekend?'Closed for today':'Closed — back Saturday 10am');
    live.className='chip '+(open?'chip--open':'chip--shut');
  }}
}})();
</script>""".format(maps=MAPS_DIR, ig=IG_URL, fb=FB_URL, place=MAPS_PLACE, name=NAME,
                    wa=WORDMARK_A, wb=WORDMARK_B, tag=TAGLINE, a1=ADDR1, a2=ADDR2,
                    handle=IG_HANDLE, rating=G_RATING, hrs=HOURS_SHORT, yr=2026,
                    dir=ico('dir'), igi=ico('ig'), fbi=ico('fb'), sti=ico('star'))


def page(key, title, desc, body):
    html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{canon}<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}img/hero-cherry.jpg">
<meta name="theme-color" content="#F89F24">
<link rel="icon" href="img/flounder.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lilita+One&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&display=swap" rel="stylesheet">
<style>{css}</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>
{head}
<main id="main">
{body}
</main>
{foot}
</body>
</html>
"""
    ld = ('{"@context":"https://schema.org","@type":"Bakery","name":"%s",'
          '"image":"%simg/hero-cherry.jpg","address":{"@type":"PostalAddress",'
          '"streetAddress":"%s","addressLocality":"Gainesville","addressRegion":"FL",'
          '"postalCode":"32601","addressCountry":"US"},'
          '"geo":{"@type":"GeoCoordinates","latitude":%s,"longitude":%s},'
          '"servesCuisine":"Doughnuts","priceRange":"$",'
          '"sameAs":["%s","%s"],'
          '"aggregateRating":{"@type":"AggregateRating","ratingValue":"%s","reviewCount":"%d"},'
          '"openingHoursSpecification":[{"@type":"OpeningHoursSpecification",'
          '"dayOfWeek":["Saturday","Sunday"],"opens":"10:00","closes":"13:30"}]}'
          % (NAME, (SITE_URL.rstrip('/') + '/') if SITE_URL else '',
             ADDR1, LAT, LON, IG_URL, FB_URL, G_RATING, G_COUNT))
    fname = dict((k, f) for k, _, f in PAGES)[key]
    base = (SITE_URL.rstrip('/') + '/') if SITE_URL else ''
    canon = ('<link rel="canonical" href="%s%s">\n<meta property="og:url" content="%s%s">\n'
             % (base, fname, base, fname)) if SITE_URL else ''
    out = html.format(title=title, desc=desc, css=CSS, head=head(key), body=body,
                      foot=FOOT, ld=ld, canon=canon, base=base)
    path = os.path.join(OUT, fname)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(out)
    print('%-14s %6.1f kb' % (os.path.basename(path), len(out) / 1024))


# ------------------------------------------------------- shared blocks
def rating_block(on_ink=True):
    bars = ''.join(
        '<div class="bar"><span>%d&#9733;</span>'
        '<span class="bar__t"><span class="bar__f" style="width:%.1f%%"></span></span>'
        '<span class="bar__n">%d</span></div>' % (s, n / G_COUNT * 100, n)
        for s, n in G_BREAKDOWN)
    return """<div class="rating">
  <div class="rating__score">
    <div class="rating__num">{r}</div>
    {st}
    <div class="rating__of">{n} Google reviews</div>
  </div>
  <div>
    <div class="rating__bars">{bars}</div>
  </div>
</div>""".format(r=G_RATING, st=stars(5), n=G_COUNT, bars=bars)


def shots_block(limit=8, tall=False):
    cells = ''.join(
        '<a href="%s" target="_blank" rel="noopener"><img src="img/%s" alt="%s" loading="lazy" '
        'width="700" height="700"></a>' % (IG_URL, f, a)
        for f, a in SHOTS[:limit])
    return '<div class="shots%s">%s</div>' % (' shots--tall' if tall else '', cells)


# ----------------------------------------------------------------- home
HOME = """
<section class="hero"><div class="wrap hero__grid">
  <div>
    <span class="hero__kicker">{bolt} Open Saturday &amp; Sunday</span>
    <h1>Gainesville&rsquo;s <em>from-scratch</em> doughnut shop.</h1>
    <p class="hero__sub">Cream-filled brioche and plant-based glazed, made by hand on
       NW 5th Ave. Four sweet flavours and one savoury, swapped out every two weeks.</p>
    <div class="hero__meta">
      <span class="chip" id="open-now">10am &ndash; 1:30pm or sellout</span>
      <span class="chip">{leaf} Vegan line, every week</span>
      <span class="chip">{pin} 8 min from campus by car</span>
    </div>
    <div class="btnrow">
      <a class="btn btn--orange btn--lg" href="menu.html">See this fortnight&rsquo;s flavours</a>
      <a class="btn btn--ghost btn--lg" href="visit.html">{dir} Plan your visit</a>
    </div>
  </div>
  <div class="hero__art">
    <img src="img/hero-cherry.jpg" alt="A cherry-topped brioche doughnut on the tray at Flatfish GNV"
         width="2000" height="2819" fetchpriority="high">
    <a class="hero__badge" href="reviews.html" aria-label="{r} stars from {n} Google reviews — read the reviews">
      <span><b>{r}</b></span>
      <span>{st}<span>{n} Google reviews</span></span>
    </a>
  </div>
</div></section>

<div class="ribbon"><div class="ribbon__in">
  <span>Brioche filled</span><span>Plant-based glazed</span><span>The Dagel</span>
  <span>New board every two weeks</span><span>Brioche filled</span><span>Plant-based glazed</span>
  <span>The Dagel</span><span>New board every two weeks</span>
</div></div>

<section class="sec sec--paper"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">What&rsquo;s in the case</p>
    <h2>Three things, done properly.</h2>
    <p class="lede">Everything is made from scratch in the shop. No shortcuts, no
       day-olds — when the trays are empty, that&rsquo;s the day.</p>
  </div>
  <div class="grid grid--3">
    <article class="card">
      <img src="img/tray.jpg" alt="Brioche doughnuts piped with cream" loading="lazy" width="1242" height="860">
      <div class="card__body">
        <span class="card__tag">Filled</span>
        <h3>Cream-filled brioche</h3>
        <p>Light, airy, slightly chewy dough rolled in gritty sugar, then filled to order with
           pastry cream, curd or custard. This is the one people queue for.</p>
      </div>
    </article>
    <article class="card">
      <img src="img/racks.jpg" alt="Racks of glazed doughnuts cooling at the shop" loading="lazy" width="1600" height="1071">
      <div class="card__body">
        <span class="card__tag card__tag--vegan">Plant-based</span>
        <h3>Vegan glazed</h3>
        <p>A whole second line with no egg and no dairy — denser, with a proper chew.
           Salted Brown Butter and Thicc Chocolate are on the board year-round.</p>
      </div>
    </article>
    <article class="card">
      <img src="img/dagel.jpg" alt="A Dagel — brioche with cream cheese, scallions and everything seasoning" loading="lazy" width="919" height="511">
      <div class="card__body">
        <span class="card__tag card__tag--savory">Savoury</span>
        <h3>The Dagel</h3>
        <p>Their doughnut-bagel: whipped cream cheese, scallions and everything seasoning
           on the same brioche. For people who want breakfast, not dessert.</p>
      </div>
    </article>
  </div>
</div></section>

<section class="sec sec--ink"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">What Gainesville says</p>
    <h2>{r} stars from {n} Google reviews.</h2>
    <p class="lede">{p5}% of them are five stars. The most common piece of advice in all
       of them: get there early.</p>
  </div>
  {rating}
  <div class="btnrow" style="margin-top:2rem">
    <a class="btn btn--orange" href="reviews.html">Read the reviews</a>
    <a class="btn btn--onink" href="{place}" target="_blank" rel="noopener">See them on Google</a>
  </div>
</div></section>

<section class="sec sec--paper"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">On the board now &middot; {rot}</p>
    <h2>This fortnight&rsquo;s flavours.</h2>
    <p class="lede">Four sweet and one savoury, all on brioche. Everything changes again
       when the rotation turns over.</p>
  </div>
  {brioche}
  <div class="btnrow" style="margin-top:1.6rem">
    <a class="btn btn--orange" href="menu.html">Full flavour list</a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">{igi} Straight from {handle}</p>
    <h2>Lately, out of the case.</h2>
    <p class="lede">{follows} people follow along for the fortnightly flavour drop.
       It is the fastest way to know what you&rsquo;re walking into.</p>
  </div>
  {shots}
  <div class="btnrow" style="margin-top:1.6rem">
    <a class="btn btn--ink" href="{ig}" target="_blank" rel="noopener">{igi} Follow {handle}</a>
  </div>
</div></section>

<section class="sec sec--paper"><div class="wrap split">
  <div class="split__art">
    <img src="img/interior.jpg" alt="The counter and display case inside Flatfish GNV"
         loading="lazy" width="1440" height="1302">
  </div>
  <div>
    <p class="eyebrow">Finding us</p>
    <h2>308 NW 5th Ave.</h2>
    <p class="lede">A small shop in Pleasant Street, a few minutes north of downtown and a
       short ride from the University of Florida. Dine in at one of the few tables, or take
       a box to go.</p>
    <table class="hours" style="margin:1.4rem 0">
      <tbody>{hours}</tbody>
    </table>
    <div class="btnrow">
      <a class="btn btn--orange" href="{maps}" target="_blank" rel="noopener">{dir} Directions</a>
      <a class="btn btn--ghost" href="visit.html">Visiting tips</a>
    </div>
  </div>
</div></section>
"""


def hours_rows():
    idx = {'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
           'Thursday': 4, 'Friday': 5, 'Saturday': 6}
    return ''.join(
        '<tr data-day="%d"><th scope="row">%s</th><td%s>%s</td></tr>'
        % (idx[d], d, '' if h else ' class="shut"', h or 'Closed')
        for d, h in HOURS)


# ----------------------------------------------------------------- menu
MENU = """
<section class="phead"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> &rsaquo; Flavours</p>
  <p class="eyebrow">The board</p>
  <h1>Flavours</h1>
  <p>Flatfish change every filled doughnut on a two-week rotation. The plant-based glazed
     line stays, mostly. Here is what that looks like.</p>
</div></section>

<section class="sec sec--paper"><div class="wrap">
  <div class="split" style="margin-bottom:2.4rem">
    <div>
      <p class="eyebrow">Brioche filled &middot; {rot}</p>
      <h2>On the board right now.</h2>
      <p class="lede">{note}</p>
    </div>
    <div class="split__art split__art--board">
      <img src="img/grid-autumn.jpg" alt="Four of this fortnight's filled flavours in their trays"
           loading="lazy" width="1400" height="1857">
    </div>
  </div>
  {brioche}

  <div class="note" style="margin-top:1.6rem">
    <strong>Rotation, not a fixed menu.</strong> This list turns over roughly every two
    weeks. Instagram <a href="{ig}" target="_blank" rel="noopener">{handle}</a> always has
    the current board first.
  </div>
</div></section>

<section class="sec" id="glazed"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">{leaf} Plant-based glazed</p>
    <h2>The vegan line.</h2>
    <p class="lede">No egg, no dairy — a denser doughnut with a proper chew, glazed rather
       than filled. These six are the year-round core.</p>
  </div>
  {glazed_core}

  <h3 style="margin:2.2rem 0 1rem">New for autumn</h3>
  {glazed_new}
</div></section>

<section class="sec sec--paper" id="dagel"><div class="wrap split split--flip">
  <div class="split__art">
    <img src="img/dagel.jpg" alt="A Dagel — brioche with cream cheese, scallions and everything seasoning"
         loading="lazy" width="919" height="511">
  </div>
  <div>
    <p class="eyebrow">The savoury one</p>
    <h2>The Dagel.</h2>
    <p class="lede">A doughnut that thinks it is a bagel. The same brioche, filled with
       whipped cream cheese and scallions and finished with everything seasoning —
       savoury, not sweet, and lighter than the bagel it is impersonating.</p>
    <p>There is one savoury slot on every board. Past versions have included Smoked Salmon,
       Elote and Pimento Cheese.</p>
  </div>
</div></section>

<section class="sec sec--ink" id="past"><div class="wrap split split--flip">
  <div class="split__art split__art--board">
    <img src="img/grid-summer.jpg" alt="Four flavours from an earlier summer board"
         loading="lazy" width="1400" height="1858">
  </div>
  <div>
    <p class="eyebrow">The archive</p>
    <h2>Flavours they&rsquo;ve run.</h2>
    <p class="lede">A year or so of boards, to give you a sense of the range. Any of these
       can come back around.</p>
    <div class="tagcloud" style="margin-top:1.4rem">{past}</div>
  </div>
</div></section>

<section class="sec sec--paper"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">{igi} From the case</p>
    <h2>What they look like.</h2>
  </div>
  {shots}
</div></section>
"""

# -------------------------------------------------------------- reviews
REVIEWS_PAGE = """
<section class="phead"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> &rsaquo; Reviews</p>
  <p class="eyebrow">What people say</p>
  <h1>{r} stars, {n} reviews</h1>
  <p>Every review below is a real one, left on the shop&rsquo;s Google listing. Nothing here
     has been reworded.</p>
</div></section>

<section class="sec sec--ink"><div class="wrap">
  {rating}
  <div class="btnrow" style="margin-top:2rem">
    <a class="btn btn--orange" href="{place}" target="_blank" rel="noopener">{sti} See all {n} on Google</a>
  </div>
</div></section>

<section class="sec sec--paper"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">In their words</p>
    <h2>A few of them.</h2>
    <p class="lede">Picked across the last year. The advice repeats itself: go early, and
       check Instagram before you leave the house.</p>
  </div>
  <div class="quotes">{quotes}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="note">
    <strong>Been in?</strong> Reviews are how a shop this small gets found.
    <a href="{place}" target="_blank" rel="noopener">Leave one on Google</a> — it takes a minute.
  </div>
</div></section>
"""


def quote_cards():
    out = []
    for name, badge, when, score, text in REVIEWS:
        meta = ' &middot; '.join(x for x in (badge, when) if x)
        out.append(
            '<figure class="quote">%s<blockquote><p>&ldquo;%s&rdquo;</p></blockquote>'
            '<figcaption class="quote__who"><span class="quote__av" aria-hidden="true">%s</span>'
            '<span><span class="quote__nm">%s</span><br>%s</span></figcaption></figure>'
            % (stars(score), text, name[0], name, meta))
    return ''.join(out)


# ---------------------------------------------------------------- visit
VISIT = """
<section class="phead"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> &rsaquo; Visit</p>
  <p class="eyebrow">Getting there</p>
  <h1>Visit the shop</h1>
  <p>308 NW 5th Ave, Gainesville. Open Saturday and Sunday from 10am until 1:30pm,
     or until the trays are empty — whichever comes first.</p>
</div></section>

<section class="sec sec--paper"><div class="wrap split">
  <div class="split__art">
    <iframe class="map" src="{embed}" title="Map showing Flatfish GNV at 308 NW 5th Ave, Gainesville"
            loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
  <div>
    <p class="eyebrow">Hours</p>
    <h2>Weekends only.</h2>
    <p class="lede">Flatfish moved to a weekend-only schedule in October 2026 so they could
       spend the extra day prepping — which also means more doughnuts on the days
       they&rsquo;re open.</p>
    <table class="hours" style="margin:1.4rem 0"><tbody>{hours}</tbody></table>
    <p class="chip" id="open-now">10am &ndash; 1:30pm or sellout</p>
    <div class="btnrow" style="margin-top:1.2rem">
      <a class="btn btn--orange btn--lg" href="{maps}" target="_blank" rel="noopener">{dir} Directions</a>
      <a class="btn btn--ghost btn--lg" href="{ig}" target="_blank" rel="noopener">{igi} Check today</a>
    </div>
  </div>
</div></section>

<section class="sec" id="getting-there"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">{pin} From campus</p>
    <h2>It&rsquo;s closer than you think.</h2>
  </div>
  <div class="grid grid--3">
    <article class="card"><div class="card__body">
      <span class="card__tag">Bike</span>
      <h3>About 10 minutes</h3>
      <p>North up NW 6th St from University Ave, then right on NW 5th Ave. Flat the whole
         way, and you can lock up out front.</p>
    </div></article>
    <article class="card"><div class="card__body">
      <span class="card__tag">Drive</span>
      <h3>About 8 minutes</h3>
      <p>Straight up Main or NW 6th from downtown. Free street parking on NW 5th Ave and
         the blocks either side — it fills up by about 10:30.</p>
    </div></article>
    <article class="card"><div class="card__body">
      <span class="card__tag">Walk</span>
      <h3>About 25 minutes</h3>
      <p>A straight shot north through the Pleasant Street historic district. Pair it with
         the Saturday farmers market at Bo Diddley Plaza.</p>
    </div></article>
  </div>
  <div class="note" style="margin-top:1.6rem">
    <strong>Travel times are estimates</strong> from the University of Florida campus —
    check your own route before you set off.
  </div>
</div></section>

<section class="sec sec--ink" id="tips"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">{bolt} Beat the sellout</p>
    <h2>How to actually get a doughnut.</h2>
    <p class="lede">The single most repeated line in their Google reviews is some version
       of &ldquo;get there early&rdquo;. Reviewers describe queues of up to 40 minutes and trays
       emptying well before closing.</p>
  </div>
  <div class="steps">
    <div class="step"><div>
      <h3>Check Instagram the night before</h3>
      <p>The flavour drop and any schedule change goes up at {handle} first. Occasional
         Saturdays are cancelled; that is where they say so.</p>
    </div></div>
    <div class="step"><div>
      <h3>Arrive before 10</h3>
      <p>Doors open at 10am and a line forms ahead of it. Reviewers report the most popular
         flavours gone within the first hour.</p>
    </div></div>
    <div class="step"><div>
      <h3>Buy for the group</h3>
      <p>Boxes travel well and the dough is best the same day. If you are going anyway,
         take enough for the house.</p>
    </div></div>
    <div class="step"><div>
      <h3>Have a second choice ready</h3>
      <p>Five flavours, one small shop. By late morning you are choosing from what is left,
         and the vegan glazed often outlast the filled.</p>
    </div></div>
  </div>
</div></section>

<section class="sec sec--paper"><div class="wrap">
  <div class="grid grid--2">
    <div>
      <p class="eyebrow">Good to know</p>
      <h2>The small print.</h2>
      <table class="hours" style="margin-top:1.2rem"><tbody>
        <tr><th scope="row">Dine in</th><td>Yes, a few tables</td></tr>
        <tr><th scope="row">Takeaway</th><td>Yes</td></tr>
        <tr><th scope="row">Delivery</th><td class="shut">No</td></tr>
        <tr><th scope="row">Vegan options</th><td>The whole glazed line</td></tr>
        <tr><th scope="row">Coffee</th><td>Yes</td></tr>
        <tr><th scope="row">Neighbourhood</th><td>Pleasant Street</td></tr>
      </tbody></table>
    </div>
    <div>
      <p class="eyebrow">{pin} Address</p>
      <h2>308 NW 5th Ave</h2>
      <p class="lede">Gainesville, FL 32601</p>
      <p>Questions about allergens, large orders or a flavour you loved? A message on
         Instagram is the way to reach them — they answer.</p>
      <div class="btnrow">
        <a class="btn btn--orange" href="{ig}" target="_blank" rel="noopener">{igi} Message on Instagram</a>
        <a class="btn btn--ghost" href="{maps}" target="_blank" rel="noopener">{dir} Open in Maps</a>
      </div>
    </div>
  </div>
</div></section>
"""

# ---------------------------------------------------------------- about
ABOUT = """
<section class="phead"><div class="wrap">
  <p class="crumb"><a href="index.html">Home</a> &rsaquo; Our Story</p>
  <p class="eyebrow">Since {opened}</p>
  <h1>A small shop that only does this.</h1>
  <p>Flatfish is {owners}, a doughnut case, and a two-week flavour rotation they have kept
     up for three years.</p>
</div></section>

<section class="sec sec--paper"><div class="wrap split">
  <div class="split__art">
    <img src="img/interior.jpg" alt="Inside Flatfish GNV — the counter, the case and the racks"
         loading="lazy" width="1440" height="1302">
  </div>
  <div>
    <p class="eyebrow">The idea</p>
    <h2>Make a few things, make them properly.</h2>
    <p>Flatfish opened on NW 5th Ave in {opened} and has stayed deliberately small ever
       since. Everything is made from scratch in the shop: the brioche, the pastry cream,
       the curds, the caramel for the pralines, the preserves that end up in the glaze.</p>
    <p>That is the reason for the short week and the short menu. Four sweet brioche, one
       savoury, and a plant-based glazed line — then the whole filled board changes again a
       fortnight later. In October 2026 they cut back to Saturdays and Sundays, writing that
       the extra prep day would mean more doughnuts and fewer unplanned closures.</p>
    <p>{owners} run it, and they sign their posts.</p>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="grid grid--3">
    <article class="card"><div class="card__body">
      <span class="card__tag">From scratch</span>
      <h3>Nothing out of a bucket</h3>
      <p>Crème fraîche whipped in-house, Callebaut 55% in the chocolate, pecans caramelised
         in vanilla, cherries preserved in summer for a glaze in October.</p>
    </div></article>
    <article class="card"><div class="card__body">
      <span class="card__tag card__tag--vegan">Plant-based</span>
      <h3>A real vegan line</h3>
      <p>Not one token flavour. The entire glazed range is egg- and dairy-free, and
         reviewers who have tried vegan doughnuts elsewhere keep saying these are better.</p>
    </div></article>
    <article class="card"><div class="card__body">
      <span class="card__tag">Two-week turn</span>
      <h3>Never quite the same twice</h3>
      <p>Butternut squash and nutmeg in autumn, peaches at the end of summer, salted
         watermelon in May. The board follows whatever is good right now.</p>
    </div></article>
  </div>
</div></section>

<section class="sec sec--ink"><div class="wrap split split--flip">
  <div class="split__art">
    <img src="img/racks.jpg" alt="Trays of doughnuts on the racks at Flatfish GNV"
         loading="lazy" width="1600" height="1071">
  </div>
  <div>
    <p class="eyebrow">The name</p>
    <h2>Why a flounder?</h2>
    <p class="lede">A flatfish is the one that looks like nothing much until you turn it
       over. The engraved flounder on the window is the shop&rsquo;s own mark, and it is on
       every box that leaves the counter.</p>
    <div class="btnrow" style="margin-top:1.4rem">
      <a class="btn btn--orange" href="menu.html">See what&rsquo;s on the board</a>
      <a class="btn btn--onink" href="reviews.html">Read the reviews</a>
    </div>
  </div>
</div></section>

<section class="sec sec--paper"><div class="wrap">
  <div class="sec__head">
    <p class="eyebrow">{igi} {handle}</p>
    <h2>Three years of doughnuts.</h2>
  </div>
  {shots}
</div></section>
"""


# ----------------------------------------------------------------- build
def build():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    page('index', '%s — From-scratch doughnuts in Gainesville, FL' % NAME,
         'Cream-filled brioche and plant-based glazed doughnuts made from scratch at '
         '308 NW 5th Ave, Gainesville. Open Saturday and Sunday, 10am until sellout. '
         '%s stars from %d Google reviews.' % (G_RATING, G_COUNT),
         HOME.format(bolt=ico('bolt'), leaf=ico('leaf'), pin=ico('pin'), dir=ico('dir'),
                     igi=ico('ig'), r=G_RATING, n=G_COUNT, st=stars(5), p5=G_PCT5,
                     rating=rating_block(), place=MAPS_PLACE, rot=ROTATION_LABEL,
                     brioche=flavour_list(BRIOCHE), shots=shots_block(8),
                     handle=IG_HANDLE, follows=IG_FOLLOWS, ig=IG_URL,
                     hours=hours_rows(), maps=MAPS_DIR))

    page('menu', 'Flavours — %s' % NAME,
         'This fortnight\'s board at Flatfish GNV: cream-filled brioche, the savoury Dagel, '
         'and the year-round plant-based glazed line.',
         MENU.format(rot=ROTATION_LABEL, note=ROTATION_NOTE, brioche=flavour_list(BRIOCHE),
                     glazed_core=flavour_list(GLAZED_CORE), glazed_new=flavour_list(GLAZED_NEW),
                     past=''.join('<span>%s</span>' % f for f in PAST_FLAVOURS),
                     shots=shots_block(8), leaf=ico('leaf'), igi=ico('ig'),
                     ig=IG_URL, handle=IG_HANDLE))

    page('reviews', 'Reviews — %s' % NAME,
         '%s stars from %d Google reviews. What Gainesville says about Flatfish GNV.'
         % (G_RATING, G_COUNT),
         REVIEWS_PAGE.format(r=G_RATING, n=G_COUNT, rating=rating_block(),
                             place=MAPS_PLACE, sti=ico('star'), quotes=quote_cards()))

    page('visit', 'Visit — %s' % NAME,
         'Flatfish GNV is at 308 NW 5th Ave, Gainesville, open Saturday and Sunday '
         '10am–1:30pm or until sellout. Directions, parking and how to beat the queue.',
         VISIT.format(embed=MAPS_EMBED, hours=hours_rows(), maps=MAPS_DIR, ig=IG_URL,
                      dir=ico('dir'), igi=ico('ig'), pin=ico('pin'), bolt=ico('bolt'),
                      handle=IG_HANDLE))

    page('about', 'Our Story — %s' % NAME,
         'Flatfish GNV has been making from-scratch brioche and plant-based glazed '
         'doughnuts on NW 5th Ave since %s.' % OPENED,
         ABOUT.format(opened=OPENED, owners=OWNERS, shots=shots_block(8),
                      igi=ico('ig'), handle=IG_HANDLE))


if __name__ == '__main__':
    build()
