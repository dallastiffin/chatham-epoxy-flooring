# Keeping city sites genuinely distinct

A network of near-identical sites for one business is the footprint Google
looks for when classifying **doorway pages** — sites built to funnel traffic
rather than serve a place. That is an explicit policy violation, and it is a
bigger risk than any "duplicate content penalty" (which is largely a myth for
navigation and button text).

This file records what the template now does for you, and what still needs a
decision per city.

---

## Measured on the Grimsby build

After the changes, non-markdown text on the home page is **384 words across 50
distinct strings** out of 3,418 rendered words. All of it is interface chrome:

```
  9x  Get a Free Quote
  3x  Request an Estimate
  3x  Call Now
  2x  Email / City / Service Interested In
  1x  Skip to main content
  1x  Why Us
```

Button labels and form fields must repeat. Google expects that. Nothing there
looks like a doorway network.

---

## Handled by the template

**All prose is in the markdown.** Headings, body copy, CTA headings and text,
form intros, hero badges, sidebar text, gallery intro, services page copy, FAQ
page copy and the 404 wording all live in the content file — in the `# SITE
COPY` block at the end. Every city writes its own.

**Alt text is in the markdown too**, under `## Photo Alt Text`, one line per
image slug. If a city omits any, `build.py` prints a warning naming the missing
images rather than silently reusing the previous city's wording.

**Privacy and terms are `noindex, follow`** and excluded from `sitemap.xml`.
They are boilerplate by nature and carry no ranking value, so they are removed
from the near-duplicate calculation entirely.

**Meta titles and descriptions** come from the markdown SEO block, written per
city.

---

## Still needs a decision per city

### 1. Photos — the strongest footprint

Identical imagery across ten domains is more detectable than identical wording,
and easier for a human reviewer to spot. In rough order of preference:

- Different photos per city — best
- Different subsets of a larger pool, so no two sites share a full set
- Same photos, different crops and ordering — weakest, but better than nothing

Whatever you choose, the alt text must describe the actual image and be written
fresh.

### 2. Genuinely rewrite the copy

Swapping city names in the same 7,900 words is the failure mode this whole
exercise exists to prevent. Each city needs:

- A different section order on the home page, and some different sections
- Local specifics that only apply there: named roads, the lake or escarpment or
  whatever the local geography is, neighbourhood names, the actual towns
  serviced
- Climate detail that is true for that city, not copied
- Different examples, different FAQ questions, different price framing
- Its own service area list

### 3. Separate NAP data

A distinct phone number per city is already the plan and it is the single most
useful differentiator. Also worth varying where possible:

- Street address, once you have one per city
- Hours, if they genuinely differ
- Latitude and longitude in `CONFIG` — set these per city, they feed schema

### 4. Do not cross-link the network

Ten sites linking to each other is a recognisable pattern. Keep them separate.
Link out to genuinely useful local resources instead if you want outbound links.

---

## Quick audit before launching a city

Ask me to run this and I will report actual numbers:

- Percentage of rendered text sourced from that city's markdown
- Any string appearing verbatim on a previously launched city site
- Photos shared with another city
- Whether every image has city-specific alt text
- Meta descriptions: length, uniqueness, and that they differ structurally from
  the previous city's

---

## What I would not bother changing

Form field labels, navigation labels, button text, service names, the skip link,
the eyebrow labels above section headings. These are interface, not content.
Varying them per city would make the sites worse for visitors and would not
change how they are classified.
