# Design Brief

## Hairline.app

Marketing Website — UI/UX Design Brief

Prepared for: Lead Product Designer  
Prepared by: Samasu Digital LTD

Version 2.0 — May 2026

## The One-Line Brief

Design Hairline.app to feel like a premium consumer health-tech brand (in the spirit of Hims) layered with the editorial authority of a medical publisher — clear enough that a patient downloads the app in under 60 seconds and a clinic books a demo without scrolling twice.

## 1. Project Context

### 1.1 What Hairline Is

Hairline is a digital platform that connects people experiencing hair loss with vetted hair restoration providers worldwide. It is built around four product pillars:

1. Patient–provider matching with consultation, booking and 3D head-scan diagnostics.
2. Hairline Aftercare — post-procedure recovery tracking, symptom monitoring, video follow-ups.
3. Hairline Travel — flights, hotels, transfers and visa support for medical travel.
4. A provider platform — lead generation, scheduling and patient management for clinics.

### 1.2 The Strategic Job of the Website

The website is not a brochure. It is a three-job machine:

- Convert consumers to app downloads (primary).
- Convert clinics to provider demo requests (secondary).
- Own organic search for hair-loss intent queries — the long-term moat.

#### Strategic North Star

Within 24 months, hairline.app should be the first organic result a person sees when they Google any meaningful hair-loss query — and the design system must support that ambition from day one.

### 1.3 Brand Positioning

Hairline sits at the intersection of three categories. The design must reconcile all three:

| Category                       | Reference Brand                              | What We Borrow                                                                                                            |
|--------------------------------|----------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| Consumer health<br>tech        | Hims, Manual, Ro                             | Confident, lifestyle-led product<br>photography; bold typography;<br>clear conversion architecture;<br>aspirational hero. |
| Editorial medical<br>authority | Healthline, Cleveland Clinic, Mayo<br>Clinic | Article templates, structured<br>information hierarchy, expert<br>review signals, citation patterns.                      |
| Marketplace UX                 | Zocdoc, Airbnb                               | Provider discovery, filtering,<br>profile pages, trust signals<br>(ratings, verification badges).                         |

*Hairline must never look like:*

- A generic SaaS startup landing page.
- A cosmetic clinic chain (the category we are disrupting).
- A WebMD-style ad-stuffed publisher.

## 2. Audiences & User Journeys

### 2.1 Primary Audience — Patients (B2C)

Demographics: men and women aged 25–50, with growing share in 25–35 due to early-intervention shift. Heavily mobile (70%+ of traffic expected on phones).

#### Emotional Context

- Hair loss is often the first medical concern these users have actively researched online.
- They are anxious, self-conscious and skeptical of marketing.
- They have already encountered low-trust competitors (Turkey clinics with stock photos, Instagram ads, etc).

#### Design Implications

- Tone must be reassuring, not aspirational-bro.
- Avoid clichéd 'before and after' shock imagery in hero positions.
- Lead with education and authority before commerce.
- Use real, diverse, photographed people — no stock illustrations of bald men shrugging.

### 2.2 Secondary Audience — Clinics & Providers (B2B)

Decision-makers: clinic owners, marketing directors, hair-restoration surgeons running independent practices, and operations leads at chains.

#### What They Need to See in 10 Seconds

- Patient lead-flow volume and quality.
- Cost-per-acquisition vs. their current channels.
- Clinical credibility of the platform (it won't embarrass them).
- Geographic reach and exclusivity terms.

### 2.3 The Two Journeys — Visual Separation

From the first viewport, the homepage must split cleanly into two pathways. This is the single most important UX decision in the entire site.

#### The Two-Door Principle

Above the fold: one dominant hero positioned for patients (app download), and one secondary but unambiguous entry for providers ("For Clinics →").

Never mix the two value propositions in the same hero. Hims, Manual, Ro and every successful health-tech brand has resisted the temptation. We will too.

### 2.4 Conversion Targets

| Audience    | Primary Action                  | Secondary Action                              |
|-------------|---------------------------------|-----------------------------------------------|
| Patient     | Download the app                | Start hair-loss assessment / find a<br>clinic |
| Clinic      | Book a demo                     | Download provider deck                        |
| SEO visitor | Read article →<br>email capture | Begin assessment                              |

## 3. Design Direction

### 3.1 Primary Reference — Hims.com

Hims.com is the closest existing reference for what we want Hairline.app to feel like as a consumer experience. The designer should study hims.com end-to-end before starting layout work.

#### Specifically Borrow

- **Hero composition —** large, confident sans-serif headline; layered, premium product/device photography; brand-coloured accent panels rather than flat hero images.
- **Tile-based section grouping —** see the Hims homepage where 'Start your weight loss today' and 'See how much weight you can lose' live as adjacent rounded tiles. Hairline should adopt this modular tile system for routes into different journeys (e.g., 'Start your hair assessment', 'Find a clinic near you', 'Track your recovery').
- **Mega-menu navigation —** see the attached screenshot of the Hims 'Hair Regrowth' panel. The flyout has four clear sections: a featured CTA card (with phone mockup), an 'Explore' list (top-level treatment areas), a 'Get support for' list (symptom-based entry), and 'Hair loss treatments' (product/service list). Hairline's mega-menu should use the same four-zone pattern for each category.
- **Trust through specificity —** Hims uses confident headlines like 'The care you've always deserved'. Hairline should match that tone: declarative, calm, never gimmicky.

#### Hims Mega-Menu Reference (Attached Screenshot)

The provided Hims screenshot shows the menu structure to replicate. Treat it as a structural reference, not a visual copy:

| Hims Menu Zone                                                                                                                       | Hairline Equivalent                                                                                                                                 |
|--------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| Featured card with phone<br>mockup ('Start your hair loss<br>assessment')                                                            | Featured card linking to the hair-loss assessment flow with<br>an iPhone mockup of the assessment screen                                            |
| EXPLORE —<br>top-level<br>treatment routes                                                                                           | EXPLORE —<br>'Hair loss treatments', 'Hair transplant', 'Find a<br>clinic'                                                                          |
| GET SUPPORT FOR —<br>symptom-based entry<br>(Receding hairline, Overall<br>thinning, Thinning at the<br>crown, Preventing hair loss) | GET SUPPORT FOR —<br>same condition labels. These are<br>SEO landing pages, see Section 5.                                                          |
| HAIR LOSS TREATMENTS<br>—<br>product list with 'New',<br>'Rx', 'Popular' tags                                                        | TREATMENTS —<br>Hair Transplant (FUE/FUT/DHI), PRP,<br>Finasteride, Minoxidil, Scalp Micropigmentation, etc. Use the<br>same small pill-style tags. |

| Hims Menu Zone                          | Hairline Equivalent                                               |
|-----------------------------------------|-------------------------------------------------------------------|
| HAIR CARE — adjacent<br>product category | AFTERCARE — Hairline Aftercare, Recovery tracking,<br>Travel packages |

### 3.2 Dynamic Scroll-Synced Phone Mockups (Attached Screenshots)

The two additional attached screenshots demonstrate a scroll-driven 'phone in hand' module we want to adopt. The Function Health / Hims pattern works like this:

5. A static 'hand holding phone' image is anchored to the centre of a tall section.
6. As the user scrolls, the screen inside the phone cross-fades or slides between sequential app screens.
7. Either side of the phone, large headline + supporting copy fades in/out, synchronised to the screen currently visible on the phone.
8. Surrounding background cards (biomarker cards, etc.) drift in parallax to add depth.

#### Hairline Application

Build this exact scroll-synced module to showcase the Hairline app journey. Recommended sequence (4–6 screens, one per scroll-stop):

1. 'Start your assessment' — onboarding screen with hair-loss pattern selector.
2. 'Get your 3D scan' — phone showing 3D head-scan capture.
3. 'Meet your matched providers' — provider list / map view.
4. 'Plan your treatment' — treatment plan / cost breakdown.
5. 'Track your recovery' — Hairline Aftercare dashboard with symptom log.
6. 'Your hair, restored' — progress photo timeline.

Each screen pairs with a left-aligned headline (e.g., 'Find your baseline', 'Plan your breakthrough') and a single sentence of support copy, exactly as the reference screenshots demonstrate.

#### Technical Note for the Designer

- Design all 4–6 phone screens at full resolution as standalone artboards — engineering will assemble the scroll-sync interaction.
- Provide a Lottie or sequenced PNG export plan.
- Specify scroll-stop offsets so headline copy syncs precisely.
- Build a mobile fallback: on small viewports, convert to a vertical stack of phone-screen tiles.

### 3.3 Visual Style — Specifics

| Element       | Direction                                                                       | Notes                                                                                                                                                                                                                                          |
|---------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Palette       | Restrained, premium, healthcare<br>adjacent                                     | Off-white / warm-neutral<br>backgrounds; one confident brand<br>accent; deep ink for type. Avoid<br>medical blue (over-used) and<br>clinic-green (over-used). A warm<br>earthy/terracotta or sophisticated<br>forest tone would differentiate. |
| Typography    | One geometric/humanist sans +<br>one editorial serif (for long-form<br>content) | Suggested pairings: Söhne or<br>Inter (UI) + Tiempos<br>or GT Sectra<br>(editorial). Type scale must work<br>from 12px footnote to 96px hero<br>headline.                                                                                      |
| Imagery       | Real photography of diverse<br>people. Lifestyle, not clinical.                 | Commission a shoot if budget<br>allows. Avoid stock photos of bald<br>men touching their heads —<br>the<br>entire category is poisoned with<br>this.                                                                                           |
| Iconography   | Custom 1.5px stroke line icons                                                  | No emoji, no Material Icons, no<br>Lucide-default. Hairline needs a<br>proprietary icon set as an<br>authority signal.                                                                                                                         |
| Motion        | Subtle, purposeful, never<br>decorative                                         | Scroll-synced modules (3.2), fade<br>ins on enter, micro-interactions on<br>CTA hover. No bouncy parallax.                                                                                                                                     |
| Corner radius | Generous (12–24px) on tiles and<br>cards                                        | Matches Hims, Function Health,<br>modern health-tech.                                                                                                                                                                                          |
| Shadows       | Soft, low-spread, brand-tinted                                                  | Avoid Material elevation. Closer to<br>Linear/Vercel diffuse shadows.                                                                                                                                                                          |
| Spacing       | Generous. Breathing room signals<br>premium.                                    | Default vertical section padding:<br>120px desktop / 64px mobile.                                                                                                                                                                              |

## 4. Sitemap & Page Inventory

The site is organised into five top-level zones. Pages marked with ★ are SEO-critical and must be templated first.

### 4.1 Marketing

- / — Homepage ★
- /how-it-works — Patient journey, step-by-step
- /about, /careers, /press, /contact

### 4.2 Patient (B2C)

- /for-patients — Consumer landing
- /find-a-clinic — Provider directory + map ★
- /find-a-clinic/[city] — City pages (London, Dubai, Istanbul, Doha, etc.) ★
- /providers/[clinic-slug] — Clinic profile pages ★
- /aftercare — Hairline Aftercare service page
- /travel — Hairline Travel service page
- /assessment — Hair-loss assessment flow entry (links to app)

### 4.3 Treatments Hub ★

Each treatment page is a pillar/cluster SEO asset. Templated identically for consistency.

- /treatments — Hub
  - /treatments/hair-transplant
    - /treatments/hair-transplant/fue
    - /treatments/hair-transplant/fut
    - /treatments/hair-transplant/dhi
  - /treatments/finasteride
  - /treatments/minoxidil
  - /treatments/prp
  - /treatments/scalp-micropigmentation
  - /treatments/laser-therapy

### 4.4 Hair-Loss Conditions Hub ★

- /hair-loss — Pillar page
  - /hair-loss/male-pattern-baldness
  - /hair-loss/female-pattern-hair-loss
  - /hair-loss/alopecia-areata
  - /hair-loss/postpartum-hair-loss
  - /hair-loss/stress-related-hair-loss

- /hair-loss/traction-alopecia
- /hair-loss/receding-hairline
- /hair-loss/crown-thinning

### 4.5 Resources / Editorial Hub ★

- /resources — Article index, filterable by category
- /resources/[category] — Category pages
- /resources/[slug] — Individual article template
- /resources/comparisons/[slug] — Comparison template (e.g., FUE vs FUT)

### 4.6 Provider (B2B)

- /for-providers — B2B landing
- /for-providers/features
- /for-providers/enterprise
- /for-providers/case-studies
- /for-providers/pricing (future)
- /for-providers/book-demo

## 5. Page-by-Page Specifications

### 5.1 Homepage

The homepage is a sequence of distinct, mostly full-width sections. Each section has one job. No section should attempt to convert both audiences simultaneously.

#### Section 1 — Hero (Patient-Focused)

- Confident headline (~6–9 words). Working draft: 'Hair restoration, finally done right.'
- Sub-headline (1 sentence) — what Hairline is.
- Primary CTA: 'Download the app' (App Store + Google Play badges).
- Secondary text link: 'Find a clinic near you →'.
- Tertiary, smaller link top-right: 'For clinics →' (the second door).
- Visual: layered phone mockup of the assessment screen, brand-coloured background panel à la Hims.
- Trust strip below the fold: 'Verified providers in 14 countries · 4.9 ★ App Store · Medically reviewed content'.

#### Section 2 — Tile Grid: Routes In

Four rounded tiles (2×2 on desktop, stacked on mobile) styled after the Hims homepage tile grid:

- Tile 1: 'Start your hair assessment' (links to assessment flow).
- Tile 2: 'Find a verified clinic' (links to /find-a-clinic).
- Tile 3: 'Compare treatments' (links to /treatments).
- Tile 4: 'Track your recovery' (Aftercare).

#### Section 3 — Scroll-Synced App Showcase

The phone-in-hand scroll module specified in Section 3.2. This is the homepage's emotional core.

#### Section 4 — How It Works

Four-step horizontal sequence: Assess → Match → Treat → Recover. Each step is a short illustration + one line.

#### Section 5 — Provider Network

World map with clinic pins, hover-reveal of clinic name. Headline: 'A network you can trust.' Stats strip: number of providers, countries, procedures booked.

#### Section 6 — Editorial / Resource Showcase

Three featured articles in editorial-card format (image, category tag, headline, reading time). Signals 'we are not just an app — we are a knowledge source.' Direct lift of the New York Times / Healthline editorial card pattern.

#### Section 7 — Testimonials / Success Stories

Real patient stories. Photographic, not videographic at first. Use long-form quotes (2–3 sentences) not single-line plaudits.

#### Section 8 — For Clinics (the B2B Door)

A single full-width band, visually distinct (darker background, different palette weight). Headline: 'Are you a clinic?'. One CTA: 'Partner with Hairline →'. This is the only B2B real estate on the homepage.

#### Section 9 — Final CTA + Footer

Repeat app download. Newsletter signup. Then full sitemap footer with legal, social, language switcher.

### 5.2 Treatment Page Template ★

One template, reused across every treatment. Consistent structure is critical for both SEO and the user's ability to compare options.

9. Hero — treatment name, one-line definition, average cost range, average recovery time.
10. 'What it is' — 2–3 paragraph editorial-style explanation.
11. 'How it works' — step-by-step illustration.
12. 'Who it's for' — eligibility checklist.
13. 'What to expect' — timeline (immediate, 1 month, 6 months, 12 months).
14. 'Cost breakdown' — table with low/mid/premium ranges.
15. 'Side effects & risks' — honest, medically-reviewed.
16. 'Compare with…' — links to comparison articles.
17. 'Find a provider' — embedded clinic shortlist filtered to this treatment.
18. FAQ accordion (5–10 questions, schema-marked-up).
19. 'Reviewed by Dr. [Name]' block with date and credentials.

### 5.3 Condition Page Template ★

Mirrors the treatment template structurally but content-led toward education first, commerce second.

20. Hero — condition name, prevalence statistic, one-line description.
21. Symptoms checklist (interactive self-assessment, captures email).
22. Causes — bulleted with citations.
23. Diagnosis — what a clinician will do.
24. Treatment options — linked tiles to relevant treatment pages.
25. Prevention & lifestyle.
26. Related articles.
27. Find-a-clinic call-out.

### 5.4 Resource Article Template ★

This template will carry the SEO weight of the entire site. Treat it with the rigour of the New York Times article page.

- Sticky table of contents (desktop left rail, mobile collapsible).
- Author + medical reviewer block at top, with photos, credentials, last-reviewed date.
- Reading time, category breadcrumb, share buttons.
- Editorial typography — serif body, larger leading (1.7), max 70-character line length.
- Inline citations, hover-reveal source previews.
- Pull-quote and key-takeaway components.
- In-article CTA modules (assessment, find-a-clinic) that don't feel like ads — see how Healthline subtly inserts these.
- 'Related articles' rail at the foot.
- Comments not required at launch.

### 5.5 Clinic / Provider Profile Page ★

Marketplace-style profile. Inspired by Airbnb listing pages, not LinkedIn.

- Hero gallery — clinic photos (real, not stock).
- Clinic name, location, verification badge, star rating, total reviews.
- 'About' — 3-paragraph description.
- 'Lead surgeons' — photo, credentials, years of experience.
- Services offered — pills linking to treatment pages.
- Pricing transparency — typical cost ranges.
- Patient reviews — verified-purchase only.
- Photo gallery of facility.
- Before-and-after gallery (consent-gated, blurred faces by default).
- Map + how to get there.
- 'Book consultation' CTA — opens app deep link or in-page form.

### 5.6 For Providers (B2B Landing)

Completely separate visual treatment from the consumer site — adjacent, not identical. Closer to Stripe's B2B clarity. Slightly more dense, less white-space-luxurious, more 'metrics and proof'.

29. Hero — '[X] verified clinics use Hairline to fill their books'. CTA: 'Book a demo'.
30. Logo wall of existing partner clinics.
31. Three-pillar value prop: 'Pre-qualified patients · Lower CAC · Operational tools'.
32. Dashboard screenshot section (similar scroll-synced module to consumer side, but showing provider dashboard screens).
33. Case studies — real clinics with before/after metrics.
34. Pricing teaser (or commission model explanation).
35. Compliance & security: HIPAA, GDPR, data-protection statements.
36. FAQ for clinic owners.
37. Final CTA: 'Book your demo'.

## 6. Design System Deliverables

The deliverable is not 'screens'. It is a Figma library and design system that engineering can build a long-term platform on.

### 6.1 Required Foundations

- Colour tokens — primary, accent, neutral ramp (0–900), semantic (success, warning, error, info), surface tokens for light/dark.
- Type tokens — full scale, line-height, letter-spacing, responsive rules.
- Spacing tokens — 4px base, 8/12/16/24/32/48/64/96/128.
- Elevation/shadow tokens (4 levels).
- Radius tokens (sm/md/lg/xl/2xl/full).
- Motion tokens — durations, easings.
- Breakpoints — 360 / 768 / 1024 / 1280 / 1536.
- Grid — 12-column desktop, 4-column mobile, 24/16/12px gutters.

### 6.2 Component Library (Minimum)

- Buttons (5 variants × 3 sizes × all states).
- Form fields, selectors, radio, checkbox, toggle.
- Cards — editorial, product, clinic profile, treatment tile.
- Navigation — mega-menu (per the Hims pattern), mobile drawer, breadcrumb.
- Article components — pull-quote, key-takeaway, callout, citation, expert-reviewer block.
- Tables — pricing, comparison.
- Modals, drawers, toasts.
- FAQ accordion.
- Provider card (compact + expanded).
- App-download CTAs (multiple sizes).
- Map components with custom pins.
- Loading states + skeletons.

### 6.3 Templates To Deliver

38. Homepage
39. Treatment page
40. Condition page
41. Resource article
42. Resource hub / category index
43. Clinic profile
44. Find-a-clinic directory + map
45. For-providers landing
46. Provider demo-booking page
47. Comparison page template (e.g., FUE vs FUT)
48. 404 / empty state / search results

## 7. SEO Design Requirements

SEO is a design discipline at Hairline, not a post-launch consideration. The designer is partly responsible for the search outcome and should design accordingly.

### 7.1 Structural Requirements (Must Be In Every Template)

- Single H1, clear heading hierarchy beneath.
- Breadcrumb component in every page below the top nav.
- Internal-linking patterns — every article must surface 6–8 related links.
- FAQ block (schema-ready) on treatment, condition and comparison pages.
- Author / reviewer block (E-E-A-T signal) on every article.
- Last-reviewed and published dates surfaced.
- Sticky table-of-contents on long articles.
- Image alt-text fields specified in every component.

### 7.2 Pillar-and-Cluster Architecture

Each pillar (e.g., /hair-loss) supports a cluster of child pages. Designer must produce hub/spoke navigation patterns:

- Pillar pages have 'Explore' sections linking to all cluster children.
- Cluster pages have 'Back to [pillar]' breadcrumb + 'Related in this pillar' rail.
- Sidebar navigation on desktop showing the cluster structure.

### 7.3 Performance Targets

These are design constraints, not engineering ones. Sketching at 4K with 12 carousels guarantees failure.

- Largest Contentful Paint ≤ 2.0s on 4G mobile.
- Cumulative Layout Shift ≤ 0.05.
- Maximum hero image weight: 200KB (AVIF/WebP).
- No video autoplay above the fold.
- All fonts subset and self-hosted (no Google Fonts CDN).

## 8. Mobile-First & Accessibility

### 8.1 Mobile-First

70%+ of traffic and the overwhelming majority of conversions will happen on mobile. Designer must produce mobile screens before desktop for every template.

- Single-thumb reach — primary CTAs in the bottom 40% of the viewport.
- Sticky app-download CTA on mobile (collapses to icon on scroll).
- Avoid hover-dependent interactions entirely.
- The scroll-synced phone module (3.2) must have a designed mobile fallback — vertical stack of phone-screen tiles.
- Mega-menu collapses to a full-screen drawer with the same four-zone structure.

### 8.2 Accessibility (WCAG 2.2 AA Minimum)

- Colour contrast ≥ 4.5:1 for body text, ≥ 3:1 for large text and UI.
- All interactive elements ≥ 44×44 pt tap targets.
- Focus states designed explicitly — not browser defaults.
- Form labels visible always (no placeholder-as-label).
- Reduced-motion variant for the scroll-synced module.
- Screen-reader landmark roles documented in handoff.
- Captions for any video content.

## 9. Tone of Voice & Microcopy

Microcopy is a design deliverable. The designer should write headlines and CTAs in Figma; we will polish, not author from scratch.

### 9.1 Voice Principles

| We Are       | We Are Not           | Example                                                                                                                               |
|--------------|----------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Confident    | Boastful             | 'Hair restoration, done right.' —<br>not 'The world's #1 hair platform.'                                                              |
| Calm         | Anxious or urgent    | 'Take your time.' —<br>not 'Don't<br>wait, your hair won't!'                                                                          |
| Evidence-led | Medical-jargon-heavy | 'In clinical trials, finasteride slowed<br>hair loss in 9 out of 10 men.' —<br>not 'Finasteride is a 5-alpha<br>reductase inhibitor.' |
| Human        | Bro-y or cosmetic    | 'Hair loss is more common than<br>you think.' —<br>not 'Bald is not bold,<br>king.'                                                   |
| Direct       | Vague                | '£3,200 average cost. 9-month<br>recovery.' —<br>not 'Affordable and<br>fast.'                                                        |

### 9.2 CTA Patterns

- Primary CTA verbs: Start · Find · Download · Book · See.
- Avoid: Learn more, Click here, Submit, Get started (overused).
- Pair CTAs with specifics: 'Find a clinic near you' beats 'Find a clinic'.

## 10. Process, Milestones & Deliverables

### 10.1 Phases

| Phase                            | Output                                                                                                      | Indicative Duration |
|----------------------------------|-------------------------------------------------------------------------------------------------------------|---------------------|
| 1. Discovery &<br>moodboard      | Two distinct visual directions<br>presented as moodboards + hero<br>comps                                   | 1 week              |
| 2. Design system<br>foundation   | Tokens, typography, colour, core<br>components in Figma                                                     | 2 weeks             |
| 3. Homepage +<br>key templates   | Homepage, treatment page,<br>article template (desktop +<br>mobile)                                         | 3 weeks             |
| 4. Remaining<br>templates        | Clinic profile, find-a-clinic, for<br>providers, condition page,<br>comparison, 404, etc.                   | 3 weeks             |
| 5. Polish,<br>prototype, handoff | Interactive prototype of homepage<br>scroll module, full Figma library,<br>redlines, design tokens exported | 2 weeks             |

### 10.2 Final Deliverables Checklist

- Figma file: structured with pages for Foundations, Components, Templates, Prototypes.
- All templates in mobile (360px), tablet (768px) and desktop (1280px) breakpoints.
- Interactive prototype demonstrating: navigation mega-menu, scroll-synced phone module, mobile drawer.
- Design tokens exported (JSON or Style Dictionary format).
- Asset library: icons (SVG), illustrations (SVG), brand photography selects.
- Component documentation: anatomy, variants, usage notes, do/don't.
- Handoff annotations in Figma spacing, behaviour, animation specs.
- Loom walkthrough of the design system for the engineering team.

### 10.3 Review Cadence

- Weekly design review with founding team (Mondays).
- Bi-weekly review with medical advisor for content templates.
- Engineering shadow review at end of Phase 2 and Phase 5.

## 11. What Not To Do

Anti-patterns to actively avoid:

- No stock photos of bald men touching their scalps with concerned expressions. The category is saturated.
- No 'before-and-after' shock images in hero positions. They belong on clinic profiles, gated.
- No medical-blue or neon-green dominant palette. Used by every competitor.
- No chatbot in the corner. Use a 'Book consultation' CTA instead.
- No carousels on the homepage hero. Static or scroll-synced only.
- No '5 reasons why...' listicle homepage section. We are not BuzzFeed.
- No autoplaying video with sound.
- No 'Get \$50 off your transplant!' urgency banners. Trust > urgency.
- No mixing of B2C and B2B value props in the same section.
- No emoji in headings or CTAs.

## Appendix A — Reference Links

- hims.com — overall tone, hero composition, mega-menu (primary reference)
- manual.co — UK competitor; clean, restrained execution
- ro.co — broader telehealth, strong editorial integration
- functionhealth.com — the scroll-synced phone module reference
- headspace.com — editorial warmth in a health context
- zocdoc.com — provider discovery / directory UX
- healthline.com — article template and SEO content architecture
- clevelandclinic.org — medical authority signals (do not copy aesthetic)
- stripe.com — clarity reference for the for-providers section
- airbnb.com — listing-page reference for clinic profile

## Appendix B — Glossary of Hairline Product Terms

- **Hairline Aftercare —** the post-procedure recovery service: symptom logging, 24/7 specialist access, 3D scan progress tracking.
- **Hairline Travel —** the medical-tourism arm: flights, hotels, transfers, visa support, bundled into the treatment package.
- **3D head scan —** the proprietary diagnostic input. Used both pre-procedure (planning) and post-procedure (progress tracking).
- **Provider Portal —** the B2B clinic-facing dashboard. Different product from the marketing site, but linked from /for-providers.
- **Assessment —** the in-app questionnaire that captures hair-loss pattern, history, lifestyle. Always referred to as 'the assessment', never 'the quiz' or 'the survey'.
