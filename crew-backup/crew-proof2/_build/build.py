#!/usr/bin/env python3
"""CREW 'Proof we send your adjuster' hook v2.  python3 _build/build.py"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
WORDS = json.loads((ROOT / "assets/words.json").read_text())
OFF_START, KEND, CTA, TOTAL = 1.5, 22.5, 29.6, 34.4
CAP_TOP = 1450
BROLL = [  # (start, end, kind, file, media_start)
    (0.0, 1.5, "stk", "st_6weeks.webp", 0),
    (3.2, 5.0, "vid", "n3.mp4", 0.0),
    (5.0, 6.3, "vid", "n3.mp4", 4.3),
    (9.5, 11.9, "stk", "st_45min.webp", 0),
    (11.9, 13.9, "vid", "a0.mp4", 0.4),
    (13.9, 15.9, "stk", "st_docs.webp", 0),
    (15.9, 19.7, "stk", "st_vs.webp", 0),
    (KEND, 24.0, "vid", "n1.mp4", 5.0),
    (24.0, 25.6, "vid", "a3.mp4", 3.2),
    (25.6, 27.6, "vid", "n2.mp4", 3.95),
    (27.6, CTA, "vid", "n0.mp4", 3.0),
]
CAM = [(1.5, 3.2, 1.0, 1.03), (6.3, 9.5, 1.0, 1.05), (19.7, KEND, 1.02, 1.06)]
GROUPS = ["Let me show you", "what we actually send", "your adjuster.", "This is 45 minutes", "of someone's time",
          "on day one.", "And it's the difference", "between your claim", "getting approved",
          "and you getting a phone call", "in six weeks", "asking for proof", "you don't have."]
HL = {"adjuster.", "45", "minutes", "day", "one.", "difference", "claim", "approved", "phone", "call", "six", "weeks", "proof", "don't"}
groups, wi = [], 0
for g in GROUPS:
    n = len(g.split()); ws = WORDS[wi:wi + n]
    assert " ".join(w["text"] for w in ws) == g, (g, [w["text"] for w in ws])
    groups.append(ws); wi += n
assert wi == len(WORDS)
cap_html, js = [], []
for gi, ws in enumerate(groups):
    a = ws[0]["start"]
    b = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else KEND
    b = min(b, ws[-1]["end"] + 0.5)
    spans = []
    for j, w in enumerate(ws):
        cls = "w hl" if w["text"] in HL else "w"
        spans.append(f'<span class="{cls}" id="w{gi}_{j}">{w["text"]}</span>')
        js.append(f'  word("#w{gi}_{j}", {w["start"]:.3f});')
    cap_html.append(f'<div class="cap" id="c{gi}"><span class="bx">{" ".join(spans)}</span></div>')
    js.append(f'  cap("#c{gi}", {a:.3f}, {b:.3f});')
shots, sfx = [], []
for i, (a, b, kind, f, ms) in enumerate(BROLL):
    nxt = BROLL[i + 1][0] if i + 1 < len(BROLL) else None
    contiguous = nxt is not None and abs(nxt - b) < 0.01
    d = b - a + (0.35 if contiguous else 0)
    if kind == "stk":
        m = (f'<div class="stbg"></div><img id="b{i}" class="clip stk" src="assets/media/{f}" alt="" data-start="{a:.2f}" '
             f'data-duration="{d:.2f}" data-track-index="{2 + i % 2}" />')
        shots.append(f'<div class="shot" id="s{i}" style="z-index:{5 + i}"><div class="kb" id="kb{i}" data-layout-allow-overflow>{m}</div></div>')
        if a == 0:
            js.append(f'  tl.set("#s{i}", {{ opacity: 1 }}, 0);')
        else:
            js.append(f'  tl.fromTo("#s{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12 }}, {a:.2f});')
        js.append(f'  tl.fromTo("#b{i}", {{ scale: 0.6, rotation: -6 }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }}, {a:.2f});')
        if f == "st_vs.webp":  # punch into APPROVED, then pan to the 6-weeks phone
            js.append(f'  tl.to("#b{i}", {{ scale: 1.32, x: 190, y: 40, duration: 0.5, ease: "power3.inOut" }}, {a + 0.6:.2f});')
            js.append(f'  tl.to("#b{i}", {{ x: -150, duration: 0.55, ease: "power3.inOut" }}, 17.3);')
            js.append(f'  tl.to("#b{i}", {{ scale: 1.0, x: 0, y: 0, duration: 0.5, ease: "power3.inOut" }}, 18.95);')
            sfx.append((a + 0.6, "whoosh-short.mp3", 0.57, 0.08)); sfx.append((17.3, "whoosh-short.mp3", 0.57, 0.08))
        else:
            js.append(f'  tl.fromTo("#b{i}", {{ y: 0 }}, {{ y: -30, duration: {b - a - 0.45:.2f}, ease: "none" }}, {a + 0.45:.2f});')
        if a > 0: sfx.append((a + 0.02, "pop.mp3", 0.7, 0.1))
    else:
        m = (f'<video id="b{i}" class="clip" src="assets/media/{f}" muted playsinline data-start="{a:.2f}" '
             f'data-duration="{d:.2f}" data-media-start="{ms}" data-track-index="{2 + i % 2}"></video>')
        shots.append(f'<div class="shot" id="s{i}" style="z-index:{5 + i}"><div class="kb" id="kb{i}" data-layout-allow-overflow>{m}</div></div>')
        js.append(f'  enter("#s{i}", {a:.2f});')
        js.append(f'  tl.fromTo("#kb{i}", {{ scale: 1.04 }}, {{ scale: 1.12, duration: {d:.2f}, ease: "none" }}, {a:.2f});')
        sfx.append((a - 0.1, "whoosh-short.mp3", 0.57, 0.09))
    if b < CTA - 0.01:
        if contiguous:
            js.append(f'  tl.set("#s{i}", {{ opacity: 0 }}, {b + 0.35:.2f});')
        else:
            js.append(f'  tl.to("#s{i}", {{ opacity: 0, duration: 0.2, ease: "power1.inOut" }}, {b - 0.05:.2f});')
for a, b, z0, z1 in CAM:
    js.append(f'  tl.fromTo("#cam", {{ scale: {z0} }}, {{ scale: {z1}, duration: {b - a:.2f}, ease: "none" }}, {a:.2f});')
sfx += [(0.05, "ring.wav", 1.4, 0.45), (6.2, "whoosh-short.mp3", 0.57, 0.08), (19.6, "whoosh-short.mp3", 0.57, 0.08),
        (15.1, "pop.mp3", 0.7, 0.12), (KEND - 0.15, "whoosh-cinematic.mp3", 1.4, 0.12), (CTA + 0.05, "chime.mp3", 2.0, 0.14)]
sfx_html = "\n".join(f'    <audio id="x{k}" src="assets/media/{f}" data-start="{t:.2f}" data-duration="{d}" data-volume="{v}" data-track-index="{20 + k}"></audio>'
                     for k, (t, f, d, v) in enumerate(sorted(sfx)))
music = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [
    {"t": 0, "v": 0.7}, {"t": 1.4, "v": 0.7}, {"t": 1.7, "v": 0.3}, {"t": KEND - 0.2, "v": 0.3}, {"t": KEND + 0.3, "v": 0.8}, {"t": TOTAL, "v": 0.8}]}]})
html = ((ROOT / "_build/template.html.tpl").read_text()
        .replace("{{TOTAL}}", f"{TOTAL:.2f}").replace("{{OFF_START}}", f"{OFF_START:.2f}").replace("{{SPK_DUR}}", f"{KEND - OFF_START:.2f}")
        .replace("{{CTA}}", f"{CTA:.2f}").replace("{{CTA_DUR}}", f"{TOTAL - CTA:.2f}").replace("{{CAP_TOP}}", str(CAP_TOP))
        .replace("{{SHOTS}}", "\n      ".join(shots)).replace("{{CAPS}}", "\n        ".join(cap_html))
        .replace("{{SFX}}", sfx_html).replace("{{MUSIC_AUTO}}", music).replace("/*{{JS}}*/", "\n".join(js)))
(ROOT / "index.html").write_text(html)
print("total", TOTAL, "groups", len(groups))
