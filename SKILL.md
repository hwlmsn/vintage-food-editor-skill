---
name: vintage-food-editor
description: Batch-edit uploaded restaurant food and tabletop snapshots into 3:4 vintage editorial still-life photos with selectable solid-color backgrounds and an optional user-supplied logo overlay. Use for food-photo restyling; do not use for inventing dishes, menus, posters, or text-heavy ads.
---

# Vintage Food Editor

Turn each uploaded food photo into a separate, appetizing 3:4 editorial still life. Preserve the actual dish and tableware while replacing visual clutter with a designed solid-color environment, purposeful cropping, negative space, and restrained vintage print texture.

## Establish the batch

- Treat each source food photo as an independent edit and return one result per source, in upload order.
- Never merge foods, plates, props, or visual details across source photos. Never make a contact sheet unless the user asks for one.
- Distinguish source photos from optional style references. Source photos control content; references control only composition, palette, lighting, grain, and print character.
- If there are no source photos, ask the user to upload them. If the role of a reference image is genuinely ambiguous, ask one concise question.
- Default to 3:4 portrait. Preserve another ratio only when the user explicitly requests it.

## Choose the background palette

Read [references/palettes.md](references/palettes.md) whenever selecting or presenting background colors.

- If the user names a palette number or name, use it.
- If the user says “直接做”, “自动匹配”, “你来选”, or equivalent, choose the most suitable palette per image. Prefer one palette across a coherent batch; vary by image only when it materially improves food/background separation.
- Otherwise, before editing, show the 10 numbered palette choices, recommend up to three based on the uploaded food colors, and ask for one choice: a single palette for the whole batch, per-image numbers, or automatic matching.
- Treat hex values as art-direction anchors rather than colorimetric output requirements. Keep saturation rich but controlled.

## Edit each source independently

Use the available image-editing tool once per source photo and reference only that target photo plus an optional shared style reference. Do not pass the entire batch into one edit call.

Construct the edit instruction from these invariants:

### Content fidelity

- Preserve dish type, ingredient identity, approximate quantity, portion structure, plating, vessels, cups, utensils, sauces, garnish, colors, cut surfaces, charred or crisp edges, steam, moisture, and oily highlights.
- Keep the food fresh, full, realistic, and appetizing. Preserve distinctive imperfections that establish authenticity.
- Do not add, delete, replace, duplicate, or redesign food, tableware, or meaningful garnish.
- Do not copy any concrete dish, plate, utensil, prop, logo, or text from a style reference.

### Composition

- Perform a real secondary composition; never settle for a centered cutout on a flat background.
- Use an editorial still-life crop with the subject biased left, right, or low. Allow a plate edge, bowl, glass, or utensil to be confidently cropped by the frame, but keep the dish recognizable and appetizing.
- Preserve generous negative space and use only existing foreground, middle-ground, and background elements to create depth.
- Keep a clear hierarchy: food is always the focal point and must not become too small, fragmented, or visually scattered.

### Background and grounding

- Simplify the restaurant scene into a clean solid tabletop or seamless tabletop/background space using the chosen palette.
- Retain believable contact shadows, perspective, scale, and grounding. Nothing may float.
- Remove irrelevant restaurant clutter, people, signage, reflections, and distracting environmental information without erasing meaningful tableware.

### Look and light

- Aim for mid-century commercial food still life, vintage magazine advertising, analog film scan, restrained halftone, slightly faded print color, designed crop, and negative space.
- Use soft studio light or restrained direct flash. Keep contours clear, food/background separation strong, and shadows short and soft.
- Add fine film grain, subtle print dots, mild color drift, and a lightly scanned-magazine character without reducing clarity or appetite appeal.

### Exclusions

- No people, hands, extra food, extra utensils, invented props, complex scenery, decorative clutter, captions, typography, generated logos, borders, or watermarks.
- Avoid cheap e-commerce styling, plastic food, illustration, CGI gloss, excessive aging, stains, dirt, heavy noise, harsh HDR, blur, crushed blacks, and muddy color.

## Optional logo overlay

When the user uploads a brand logo, apply it only after the food image has passed the quality gate. Never ask the image-generation model to redraw, spell, imitate, or bake the logo into the food image; use deterministic compositing so the supplied artwork remains exact.

- Use the same uploaded logo for every image in the batch unless the user maps different logos to specific images.
- Place the logo at the top-left. Preserve its aspect ratio, colors, transparency, lettering, and internal spacing.
- Default to 70% transparency, meaning 30% opacity. If the user instead says “70%不透明度” or provides another value, follow that value exactly.
- Default logo width is about 14% of the canvas, capped at 12% of canvas height, with a safe margin of 5% of canvas width from the top and left edges. Respect an explicit size or margin request.
- Prefer a transparent PNG or WebP logo. If the supplied logo has an opaque background, ask whether to preserve it or remove it; do not automatically erase light or white pixels that may belong to the logo.
- Run `scripts/apply_logo.py` once per final image. Write a new sibling file rather than overwriting the clean non-logo result.

Example:

```bash
python3 scripts/apply_logo.py \
  final-food.png brand-logo.png final-food-logo.png \
  --transparency 70 --width-ratio 0.14 --margin-ratio 0.05
```

Validate that the logo is fully inside the canvas, remains legible, is not distorted, and does not cover the main food subject. If the fixed top-left placement overlaps the subject, keep the top-left anchor but reduce the logo size before moving it elsewhere.

## Quality gate

Compare every result with its source before presenting it.

- Reject and retry once if dish identity, item count, vessel shape, major garnish, sauce placement, or core plating has materially changed.
- Retry once if the result is merely centered, lacks negative space, floats, contains added objects, or loses food clarity.
- On retry, state only the specific failed invariant as a correction while keeping the successful parts unchanged.
- If a second result still has a material mismatch, present the best result and clearly identify the unresolved deviation instead of repeatedly spending generation attempts.

## Delivery

- Return final images in source upload order and identify each by source filename or image number plus palette name.
- When a logo was supplied, deliver the composited logo versions as the final outputs and keep the clean versions available for correction or reuse.
- Keep notes minimal. Do not expose internal prompts unless the user asks.
- If only some images succeed, deliver those results and list the exact remaining images that need another pass.
