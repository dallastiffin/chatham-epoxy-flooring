# Chatham Epoxy Flooring — Website

Static site for **Chatham Epoxy Flooring**, Chatham, Ontario, covering all of
Chatham-Kent. No framework, no build server, no monthly hosting cost.

```
Chatham-Epoxy-Flooring-Website-Content.md   <- all copy lives here (source of truth)
build.py                                    <- turns the markdown into the site
wrangler.toml                               <- Cloudflare deploy config
site/                                       <- generated output, THIS is what deploys
tools/make-logo.py                          <- draws the logo and favicon assets
*.png                                       <- original photos (tracked, never served)
```

20 pages: home, services index, **12 service pages**, about, FAQ, contact,
privacy policy, terms and a 404. 17 are indexable; privacy, terms and 404 are
`noindex, follow` and excluded from `sitemap.xml` on purpose.

Initial load on the home page is about 277 KB — two eager images, everything
else lazy-loaded.

---

## Still to do before this goes live

### 1. Wire up lead delivery

**The forms validate and show a success message, but nothing is delivered
until this is done.** `SHEET_ENDPOINT` in `site/script.js` is currently the
placeholder `YOUR-APPS-SCRIPT-EXEC-URL-HERE`.

1. Go to <https://sheets.new>. That URL always creates a *native* Google Sheet.
   Do not upload an `.xlsx` — uploaded files have no Extensions menu and Apps
   Script cannot read them. If you see an `.XLSX` badge by the filename, start
   again.
2. Name it *Chatham Epoxy Flooring — Leads*.
3. **Extensions → Apps Script**. Delete the placeholder function, then paste in
   the whole of `google-apps-script.gs` from this repo.
4. Set `NOTIFY_EMAIL` if you want an alert per lead.
5. Run `testWrite` from the function dropdown, approve the permission prompt,
   confirm a row lands in a **Leads** tab, then delete the test row.
6. **Deploy → New deployment → Web app**, Execute as **Me**, Who has access
   **Anyone**. "Anyone" is required — visitors are not signed in to Google.
   They can only POST in; they cannot read the sheet.
7. Copy the Web app URL (it ends in `/exec`) into `SHEET_ENDPOINT` in
   `site/script.js`.
8. Run `python build.py` again. **This step is not optional** — `_headers`
   caches JS hard, and without the rebuild the `?v=` fingerprint stays stale
   and returning visitors keep the old file.

Apps Script sends mail as whichever Google account authorised it, regardless of
`NOTIFY_EMAIL`. Create the sheet signed in as the account the mail should come
from.

After any later edit to `google-apps-script.gs`: **Deploy → Manage deployments
→ pencil → Version: New version → Deploy.** Saving alone leaves the live
endpoint on old code.

### 2. Swap in real prices

Every price on the site is 2026 Ontario **market research**, not this
business's rates. Roughly $5–9/sq ft epoxy, $6–10 flake, $6–12 polyaspartic,
$8–12 metallic, $1,600–3,200 for a 400 sq ft double garage, plus $1–3/sq ft for
heavy preparation. Replace them in the markdown and rebuild.

### 3. Replace the metallic photo

`greyscale bathroom marbled epoxy.png` is the only metallic image in the shared
pool, and Sarnia, Sudbury and Welland all run it on their metallic page. Sarnia
is 90 km away and competes for the same searches. It ships here with the
tightest, most off-centre crop in the `CROP` table so the framing differs, but
this one wants a genuinely new photograph.

### 4. Consider a real logo

`tools/make-logo.py` **draws** the lockup rather than cropping a supplied file,
because no Chatham artwork existed. It is a graphite tile with an amber-topped
three-bar mark and reads down to 16px, but it is generated, not designed. To
replace it, rewrite that script or drop in your own assets using the same
filenames in `site/images/`.

---

## Editing the site

**Copy:** edit `Chatham-Epoxy-Flooring-Website-Content.md`, then `python build.py`.
Never hand-edit the HTML in `site/` — it is overwritten on the next build.

**Photos:** drop PNGs in the root, update `PAGE_PHOTOS` / `GALLERY_PHOTOS` and
the `CROP` table in `build.py`, then `python build.py --images` (needs Pillow).

**Design and behaviour:** `site/style.css` and `site/script.js` are hand-written
and never regenerated. Edit them directly — then **rerun `build.py`** so the
cache fingerprint updates.

---

## Photography — read before changing `PAGE_PHOTOS`

Every photo in the shared pool was already live on another city site before
this build. The rule applied here is that **no photo holds a role it already
holds elsewhere** — a Sarnia hero became a gallery item, a Welland hero became
the services-page image, a Sudbury hero became a service card. On top of that,
the `CROP` table in `build.py` shifts the focal point and zoom of every shared
photo so the delivered crop differs even where the source file cannot.

Measured result: **1.6% verbatim body-prose overlap** against all six other
city sites, and **zero** duplicated alt strings.

Four photos are gitignored and must never be used:

| File | Why |
|---|---|
| `warehouse.png` | Another flooring company's logo on a hi-vis shirt |
| `warehouse grey epoxy.png` | WOODSTOCK EPOXY FLOORING on the crew shirt and resin pail |
| `blue epoxy spread.png` | Same wordmark on the crew shirt |
| `grey spready.png` | Same wordmark on the crew shirt |

`warehouse-industrial-chatham.png` **is** tracked and used — it is a crop of
`warehouse.png` framed to drop the branded worker out of shot entirely. It is a
different box to Sarnia's crop of the same original, so it is unique to this
site.

---

## Design notes

This site deliberately does not look like the others in the network. Grimsby
and Sudbury are green with a safety-orange CTA; Sarnia and Welland are blue
with the same orange; Cape Breton is navy with teal. All of them put a
saturated colour in the header, the hero and the buttons, run a gradient hero,
and set the copy hard left with the estimate form in a sidebar.

Chatham is monochrome first: graphite `#22262c`, a single amber accent drawn
from aisle-marking yellow, and a lot of white. The hero is a single centred
column with the business name over the place it serves; the estimate form moved
out into its own band below. No gradients. Dark buttons rather than orange.
Section padding is 7rem against the template's 4rem.

The hero uses a **measured scrim** rather than the layered text-shadow the other
sites use. WCAG gives text shadows no credit, so white type on a photograph is
formally under 4.5:1 no matter how heavy the shadow. Worst case here — pure
white photo under an 82% graphite wash — computes to 10.27:1.

All 26 text-on-background pairs were computed numerically from the CSS
variables. None fall below threshold. If you change the colour variables at the
top of `site/style.css`, recompute them.

---

## Deploying

`wrangler.toml` is already in the repo, so Cloudflare knows to serve `site/`.

1. [Cloudflare dashboard](https://dash.cloudflare.com) → **Workers & Pages** →
   **Create application** → **Import a repository**
2. Pick `dallastiffin/chatham-epoxy-flooring`
3. Settings:

   | Field | Value |
   |---|---|
   | Worker name | `chatham-epoxy-flooring` — **must match `name` in `wrangler.toml`** |
   | Build command | *(leave empty)* |
   | Deploy command | `npx wrangler deploy` |
   | Root directory | `/` |

4. **Save and Deploy**

A name mismatch is the most common failure. Leave the build command empty — the
HTML is already generated and committed.

Then the domain: Cloudflare → **Add a domain** → `chathamepoxyflooring.com` →
Free plan → copy the two nameservers → set them as Custom DNS at Namecheap.
Once active, **delete any leftover Namecheap parking A record (`192.64.x.x`)
but keep the MX and TXT records** — those are email forwarding.

Add both the bare domain and `www` as custom domains on the Worker, pick one as
canonical, and redirect the other with a 301. `DOMAIN` in `build.py` is
currently `https://chathamepoxyflooring.com` (no `www`). It must match the
hostname actually served, with no redirect in between, or Google indexes a URL
that bounces. If you choose `www`, change it and rebuild.

Do not add links from this site to the other city sites. Ten sites linking to
each other is a recognisable doorway-network pattern.

---

## After launch

- Bare domain loads with a padlock; the non-canonical hostname 301s to the canonical one
- A deep link like `/garage-floor-coating` loads with no redirect
- `/nope` shows the styled 404
- Mobile: hamburger opens, dropdown expands, sticky call bar shows
- Submit a real form entry and confirm both the sheet row and the email
- `/sitemap.xml` shows the correct domain, then submit it in
  [Google Search Console](https://search.google.com/search-console)
- Run the live URL through [PageSpeed Insights](https://pagespeed.web.dev)
