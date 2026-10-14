#!/usr/bin/env python3
"""Everything the Flatfish site says, with a note on where each fact came from.

Sources, all checked 13-14 Oct 2026:
  G  = the shop's Google Business listing (maps.google.com)
  IG = instagram.com/flatfish_gnv - bio, pinned post, and the flavour posts
  P  = the shop's own printed flavour poster, photographed on Instagram
"""

# ---------------------------------------------------------------- facts
NAME        = "Flatfish GNV"
WORDMARK_A  = "FLATFISH"
WORDMARK_B  = "DOUGHNUTS"
TAGLINE     = "From-scratch doughnuts, cream filled brioche and vegan glazed."  # IG bio
ADDR1       = "308 NW 5th Ave"
ADDR2       = "Gainesville, FL 32601"                                           # G
OWNERS      = "Patty and Michael"                       # IG, they sign their posts
OPENED      = "September 2023"        # IG 29 Sep 2026: "just passed our 3 year anniversary"

# Set this once the site has a real home (e.g. "https://flatfishgnv.com"). While it is
# empty the pages ship no canonical/og:url, which is correct for an unpublished draft.
SITE_URL    = ""

IG_URL      = "https://www.instagram.com/flatfish_gnv/"
IG_HANDLE   = "@flatfish_gnv"
IG_FOLLOWS  = "7,000+"                                                   # IG: 7,071
FB_URL      = "https://www.facebook.com/FlatFishGNV/"
MAPS_PLACE  = ("https://www.google.com/maps/place/Flatfish+GNV+(Doughnuts+and+Bakery)/"
               "@29.6557358,-82.3282616,17z/data=!4m6!3m5"
               "!1s0x88e8a31e4b9456b9:0x67ece38feb391fee!8m2!3d29.6557358!4d-82.3282616")
MAPS_DIR    = ("https://www.google.com/maps/dir/?api=1&destination="
               "Flatfish+GNV+308+NW+5th+Ave+Gainesville+FL+32601")
MAPS_EMBED  = ("https://www.google.com/maps?q=Flatfish+GNV+308+NW+5th+Ave+Gainesville+FL+32601"
               "&z=16&output=embed")
LAT, LON    = 29.6557358, -82.3282616                                           # G

# Google rating, read off the listing on 13 Oct 2026
G_RATING    = "4.7"
G_COUNT     = 185
G_BREAKDOWN = [(5, 167), (4, 6), (3, 1), (2, 3), (1, 8)]
G_PCT5      = round(167 / 185 * 100)        # 90%

# Hours. Google, the Instagram bio and the 6 Oct 2026 post all agree: weekends only.
# Monday-Friday are dark. "or sellout" is their own wording and matters - see REVIEWS.
HOURS = [("Monday", None), ("Tuesday", None), ("Wednesday", None), ("Thursday", None),
         ("Friday", None), ("Saturday", "10:00am – 1:30pm"), ("Sunday", "10:00am – 1:30pm")]
HOURS_SHORT = "Saturday &amp; Sunday, 10am – 1:30pm or sellout"

# ------------------------------------------------------- the doughnuts
# Current rotation, from the 29 Sep + 3 Oct 2026 posts and the poster photographed
# with them. Flatfish change the whole brioche line every two weeks.
ROTATION_LABEL = "October 2 – 18"
ROTATION_NOTE  = ("Flatfish change every filled flavour on a two-week rotation — four sweet "
                  "and one savoury. The list below is the current board.")

BRIOCHE = [
    ("Chocolate Velvet", "Rich chocolate cream with house-made crème fraîche and Callebaut 55% dark chocolate.", ""),
    ("Lemon Curd", "Strong, tart fresh lemon curd over a light vanilla filling.", ""),
    ("Pecan Praline", "Pecans caramelised with vanilla, folded into whipped pastry cream.", ""),
    ("Butternut Squash", "Roasted and puréed smooth with honey custard cream and nutmeg.", ""),
    ("Scallion Dagel", "Whipped cream cheese, scallions and everything seasoning. Savoury, not sweet.", "savory"),
]

GLAZED_NEW = [
    ("Sour Pomegranate", "Fresh pomegranate glaze with a lemon drizzle — earthy, then bright.", "vegan"),
    ("Biscoff Cookie Butter", "The classic cookie puréed with vegan butter and pie spice.", "vegan"),
    ("Cherry Chocolate", "Summer cherry preserves folded into the Thicc Chocolate glaze.", "vegan"),
]

# The year-round glazed line, straight off their printed poster. All plant-based.
GLAZED_CORE = [
    ("Salted Brown Butter", "Toasted vegan butter, salted, with vanilla. Their signature glazed.", "vegan"),
    ("Cardamom Sugar", "A classic sugar doughnut tossed with cardamom and a lil' cinnamon.", "vegan"),
    ("Thicc Chocolate", "Rich chocolate glaze with cocoa powder and dark chocolate.", "vegan"),
    ("Pink Sprinkles", "Sprinkle doughnut with a fresh raspberry glaze.", "vegan"),
    ("Passionfruit", "Passionfruit nectar glaze. Tart and citrusy.", "vegan"),
    ("Hummingbird", "Banana and pineapple glaze with candied pecans. Like the cake.", "vegan"),
]

# Flavours they have actually run, gathered from a year of their flavour posts.
PAST_FLAVOURS = [
    "Banana Puddin'", "Tiramisu", "Fruity Pebbles", "Orange Creamsicle", "Earl Grey",
    "Peaches n' Cream", "Snickerdoodle", "Piña Colada", "Pistachio", "Strawberry Cream",
    "Chocolate Brownie", "Honey Caramel", "Salted Pistachio", "Elote Dagel",
    "Smoked Salmon Dagel", "Pimento Cheese", "Mango Lime", "PB&amp;J", "Cold Brew Coffee",
    "Fresh Cherry", "Blueberry Buttermilk", "Salted Watermelon", "Bananas Foster",
    "Raspberry Cream", "Maritozzi",
]

# ------------------------------------------------------------ pictures
# Every photograph is the shop's own, pulled from instagram.com/flatfish_gnv.
SHOTS = [
    ("f-chocolate-velvet.jpg",  "A tray of Chocolate Velvet brioche doughnuts"),
    ("f-lemon-curd.jpg",        "Lemon Curd doughnuts, filling piped on top"),
    ("f-pecan-praline.jpg",     "Pecan Praline doughnuts in their tray"),
    ("f-butternut-squash.jpg",  "Butternut Squash doughnuts dusted with sugar"),
    ("f-strawberry-cream.jpg",  "Strawberry Cream doughnuts topped with fresh fruit"),
    ("f-pistachio.jpg",         "Pistachio doughnuts with chopped nuts on the cream"),
    ("f-chocolate-brownie.jpg", "Chocolate Brownie doughnuts, each with a brownie on top"),
    ("f-honey-caramel.jpg",     "Honey Caramel doughnuts with honeycomb candy"),
]

# ------------------------------------------------------------- reviews
# Verbatim extracts from the shop's public Google reviews, read 13 Oct 2026.
# Trimmed to whole sentences; nothing reworded.
REVIEWS = [
    ("Nicole Diaz", "Local Guide", "a year ago", 5,
     "WOW! I&rsquo;ve been waiting to try this place for well over a year &amp; it&rsquo;s probably the "
     "only place i can say was well worth the wait!! Smiling husband/wife duo operating it with "
     "the best donuts i&rsquo;ve ever had in my entire life. Be sure to give them a try &amp; get there "
     "EARLY!!"),
    ("Breton Homewood", "", "4 months ago", 5,
     "Best doughnuts in town. It feels like a secret speakeasy and I love telling new people "
     "about them when they come to Gainesville. Their quality is the highest I&rsquo;ve ever "
     "experienced."),
    ("The Lorac", "Local Guide", "4 months ago", 5,
     "BEST DONUTS IN GAINESVILLE. They have a variety of donuts and drinks as well that are very "
     "tasty and unique. You will have to wake up early and wait in line for around 40 minutes."),
    ("Jordan Capwell", "Local Guide", "a month ago", 5,
     "Finally made it to this GEM of a donut shop in Gainesville! Flatfish GNV is a donut shop "
     "that specializes in brioche filled donuts and vegan glazed donuts."),
    ("Neil Greishaw", "Local Guide", "a year ago", 5,
     "Get here early. All they had left by 10:30 on a Saturday were three lemon curd and "
     "Devonshire-ish creme Maritozzi. I had one, which was fabulous. Great coffee, too!"),
    ("Karlie Foster", "Local Guide", "a year ago", 5,
     "Absolutely delicious donuts!! Get there right at opening because the line forms fast. "
     "We got an assortment and every single one was so good."),
    ("Helen", "Local Guide", "10 months ago", 5,
     "Cute little spot that features homemade cream-filled brioche donuts. They have a menu "
     "that changes every few weeks so make sure to check out their social media to see their "
     "flavors."),
    ("Vincent Kong", "Local Guide", "a year ago", 5,
     "Sprint don&rsquo;t run to Flatfish Doughnuts. Heard a ton about them and finally found myself "
     "in the area and I stopped by. The shop is not big by any means but felt warm and inviting."),
    ("Birdie", "", "a year ago", 5,
     "i&rsquo;ve been coming to flatfish for some time now, and it has never disappointed!"),
]
