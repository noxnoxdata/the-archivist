# Image Prompts: The Archive of Quiet Things

*For a local image model (SDXL, Flux, or a manga-tuned checkpoint in ComfyUI). Monochrome interiors. B5 page ratio, 2:3. No baked-in text. Add lettering later.*

Honest note: no local image model is installed on this machine yet. These prompts are ready for ComfyUI, Draw Things, or DiffusionBee when you set one up.

---

## Global style prompt (append to every panel)

```
monochrome Japanese manga panel, clean black ink line art, varied line weight, screentone shading, hatching, subtle grain, quiet slice-of-life atmosphere, rainy seaside town, soft lantern light, detailed background, expressive but restrained faces, right-to-left panel composition, no color, no text, no speech bubbles
```

## Global negative prompt

```
color, glossy digital painting, oversaturated, airbrush gradients, lens flare, cinematic blur, chibi, moe, generic anime face, extra fingers, deformed hands, bad anatomy, text, watermark, signature, speech bubble, photorealistic, 3d render
```

---

## Character prompts

### Hina Aizawa

```
17-year-old Japanese girl, 160 cm, small and upright, straight black hair tied back with a plain dark ribbon, grey eyes, round serious face, small mole under left eye, faded navy work apron over cream sweater, dark trousers, worn sandals, ink-stained fingers, quiet and observant expression, monochrome manga line art, screentone
```

### Ren

```
17-year-old Japanese boy, 178 cm, tall and still, black hair falling over one eye, dark brown eyes, angular gentle face, small scar on right jaw, faded blue coat too big for him, white shirt, barefoot, calm tired expression, monochrome manga line art, screentone
```

### Obaasan

```
Japanese grandmother in her 70s, 150 cm, small and rounded, silver hair in a low bun, dark brown eyes, tea-coloured cardigan, dark skirt, house slippers, reading glasses, gentle knowing expression, monochrome manga line art, screentone
```

---

## Key panel prompts

### Panel: the Kura in the rain

```
wide establishing shot, old Japanese cedar storehouse converted into an archive, wooden engawa, paper shouji screens, low stone step, heavy typhoon rain, grey sea in the distance, fishing boats on a breakwater, single vending machine glow, monochrome manga, screentone rain, quiet melancholy, no people
```

### Panel: the boy at the gate

```
medium shot, 17-year-old boy standing at a wooden gate in heavy rain, faded blue coat open over white shirt, black hair plastered to his forehead, dark brown eyes, barefoot, no umbrella, looking at an old archive house, rain passing through him, monochrome manga, screentone, eerie calm
```

### Panel: the shadow lag

```
wide shot from behind, boy turned toward a gate in the rain, his shadow on the wet path still facing the opposite direction, a half second behind, subtle and unsettling, no monster imagery, monochrome manga, screentone, quiet horror, detailed rain
```

### Panel: tea at the archive table

```
interior, warm dim archive, low wooden table, tatami, two teenagers and an old woman with tea, shelves of old books to the rafters, single lantern light, rain on paper screens, monochrome manga, screentone, intimate quiet composition
```

### Panel: the quiet books go silent

```
close-up of a hand hovering over rows of dull old books on a wooden shelf, faint dust motes in lantern light, no hum lines, absolute stillness, monochrome manga, screentone, quiet tension
```

---

## Local model notes

- **Base model:** SDXL or Flux. Add a manga line-art LoRA if you have one. Keep the style consistent across panels.
- **Sampler:** DPM++ 2M Karras or Euler a. 30 to 40 steps.
- **CFG:** 5 to 7. Too high makes faces harsh.
- **Resolution:** 832 x 1248 (2:3) per panel, then composite onto a B5 page.
- **Consistency:** reuse the same seed family and the exact character descriptors. Generate a character turnaround first, then panels.
- **Lettering:** add bubbles and SFX in a vector editor or Clip Studio Paint. Do not let the model draw text.
- **Tone:** keep interiors black and white. Colour only the cover and chapter title page.
