<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Montserrat:wght@700;800;900&family=Playfair+Display:ital,wght@1,700&display=block" />
    <script src="assets/media/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b0b0c; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; background: #0b0b0c; font-family: "Montserrat", sans-serif; --red: #e8262b; }
      #world { position: absolute; inset: 0; }
      #cam { position: absolute; inset: 0; transform-origin: 50% 40%; }
      #spk { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      .shot { position: absolute; inset: 0; overflow: hidden; opacity: 0; }
      .kb { position: absolute; inset: 0; }
      .kb video { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: contrast(1.05) saturate(1.06); }
      .stbg { position: absolute; inset: 0; background: radial-gradient(ellipse 75% 55% at 50% 40%, #b3171c 0%, #6d0b0e 55%, #2a0507 100%); }
      .stbg::after { content: ""; position: absolute; inset: 0; background: repeating-linear-gradient(135deg, rgba(255,255,255,.035) 0 22px, transparent 22px 44px); }
      .kb img.stk { position: absolute; left: 60px; top: 230px; width: 960px; height: 960px; object-fit: contain; filter: drop-shadow(0 30px 50px rgba(0,0,0,.45)); }
      .anton { font-family: "Anton", sans-serif; text-transform: uppercase; }
      .bt { position: absolute; left: 0; right: 0; text-align: center; line-height: .9; white-space: nowrap; opacity: 0; }
      .bt .s { display: block; font-size: 100px; color: #ffd9a0; font-family: "Playfair Display", serif; font-style: italic; font-weight: 700; text-transform: none; text-shadow: 0 8px 26px rgba(0,0,0,.45); }
      .bt .b { display: block; color: #fff; text-shadow: 0 14px 40px rgba(0,0,0,.4); }
      .bt .b.red { color: #e8262b; }
      .cut { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
      .kin { position: absolute; left: 0; right: 0; text-align: center; z-index: 42; opacity: 0; white-space: nowrap; }
      .kin span { display: inline-block; padding: 16px 38px 10px; border-radius: 18px; background: #fff; color: #141416; font-size: 118px; line-height: 1; box-shadow: 0 18px 40px rgba(0,0,0,.35); }
      .kin span b { color: #e8262b; font-weight: 400; }
      #stamp { position: absolute; left: 0; right: 0; top: 1020px; text-align: center; z-index: 43; opacity: 0; }
      #stamp span { display: inline-block; padding: 14px 40px 10px; border: 10px solid #1f8f42; border-radius: 22px; color: #1f8f42; background: rgba(255,255,255,.95); font-size: 116px; letter-spacing: .04em; transform: rotate(-7deg); box-shadow: 0 18px 40px rgba(0,0,0,.35); }
      #flash { position: absolute; inset: 0; z-index: 55; background: #fff; opacity: 0; pointer-events: none; }
      #leak { position: absolute; left: -300px; top: 0; width: 1680px; height: 1920px; z-index: 54; opacity: 0; mix-blend-mode: screen; pointer-events: none;
        background: radial-gradient(ellipse 520px 900px at 30% 40%, rgba(255,90,40,.7), transparent 70%), radial-gradient(ellipse 320px 600px at 75% 30%, rgba(255,40,50,.5), transparent 70%); }
      #captions { position: absolute; left: 40px; right: 40px; top: {{CAP_TOP}}px; height: 110px; z-index: 40; }
      .cap { position: absolute; left: 0; right: 0; top: 0; text-align: center; opacity: 0; }
      .bx { display: inline-block; padding: 10px 24px 14px; border-radius: 18px; background: #fff; box-shadow: 0 16px 34px rgba(0,0,0,0.3); white-space: nowrap; }
      .w { display: inline-block; margin: 0 10px; font-weight: 900; font-size: 58px; line-height: 1.1; color: #707076; letter-spacing: -0.015em; }
      .tg { position: absolute; left: 40px; right: 40px; top: {{CAP_TOP}}px; text-align: center; z-index: 41; opacity: 0; }
      .tg .bx { font-weight: 900; font-size: 70px; color: #141416; letter-spacing: -0.02em; }
      .tg .bx b { color: var(--red); }
      #tag { position: absolute; left: 0; right: 0; top: 150px; text-align: center; z-index: 41; opacity: 0; }
      #tag span { display: inline-block; padding: 14px 30px 12px; border-radius: 12px; background: var(--red); color: #fff; font-weight: 900; font-size: 44px; letter-spacing: 0.08em; box-shadow: 0 14px 30px rgba(120,10,10,0.35); }
      #grain { position: absolute; left: -200px; top: -200px; width: 1480px; height: 2320px; z-index: 50; opacity: 0.05; mix-blend-mode: overlay; pointer-events: none;
        background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='240' height='240' filter='url(%23n)'/></svg>"); }
      #cta { position: absolute; inset: 0; overflow: hidden; z-index: 60; }
      .cream { position: absolute; inset: 0; background: radial-gradient(ellipse 70% 45% at 50% 44%, #fbf8f2 0%, rgba(251,248,242,0) 70%), linear-gradient(180deg, #f5efe5 0%, #ece3d5 100%); }
      #ec-logo { position: absolute; left: 200px; top: 420px; width: 680px; height: 428px; }
      #ec-logo img { width: 100%; height: 100%; display: block; filter: drop-shadow(0 20px 36px rgba(60,20,10,0.22)); }
      .c { position: absolute; left: 40px; right: 40px; text-align: center; white-space: nowrap; }
      #ec-line { top: 920px; font-weight: 800; font-size: 60px; color: #1d1d1f; letter-spacing: -0.015em; }
      #ec-line em { font-family: "Playfair Display", serif; font-style: italic; font-weight: 700; color: #c0161d; }
      #ec-phone { top: 1070px; }
      #ec-pill { position: relative; display: inline-flex; align-items: center; gap: 22px; padding: 22px 52px; border-radius: 80px; overflow: hidden; background: linear-gradient(180deg, #a07624 0%, #7a5510 100%); box-shadow: 0 16px 36px rgba(120,80,10,0.28), inset 0 2px 0 rgba(255,255,255,0.35); color: #fff; text-shadow: 0 2px 6px rgba(60,35,0,0.45); font-weight: 800; font-size: 70px; }
      #ec-pill svg { width: 60px; height: 60px; }
      #shine { position: absolute; top: -30px; left: 0; width: 120px; height: 200px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent); }
      #ec-tag { top: 1270px; font-family: "Playfair Display", serif; font-style: italic; font-weight: 700; font-size: 58px; color: #b5121b; }
      #ec-web { top: 1390px; font-weight: 800; font-size: 34px; letter-spacing: 0.16em; color: #5b544b; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{{TOTAL}}" data-width="1080" data-height="1920">
      <div id="world">
      <div id="cam"><video id="spk" class="clip" src="assets/media/speaker.mp4" playsinline data-has-audio="true" data-volume="1" data-start="{{OFF_START}}" data-duration="{{SPK_DUR}}" data-media-start="0.3" data-track-index="0"></video>
        <div class="bt anton" id="bt1" style="top:520px" data-layout-allow-occlusion><span class="b red" style="font-size:400px">45</span><span class="b" style="font-size:190px">Minutes</span></div>
        <div class="bt anton" id="bt2" style="top:620px" data-layout-allow-occlusion><span class="s">asking for</span><span class="b red" style="font-size:225px">Proof?</span></div>
        <video id="ck1" class="clip cut" src="assets/media/cut_s1.webm" muted playsinline data-start="6.30" data-duration="3.30" data-track-index="5"></video>
        <video id="ck2" class="clip cut" src="assets/media/cut_s2.webm" muted playsinline data-start="19.60" data-duration="2.90" data-track-index="5"></video>
      </div>
      {{SHOTS}}
      </div>
      <div class="kin anton" id="k-denied" style="top:1260px"><span>Claim <b>Denied?</b> 😳</span></div>
      <div id="stamp"><span class="anton">Approved ✓</span></div>
      <div id="leak"></div>
      <div id="flash"></div>
      <div id="tag"><span>WHAT WE SEND YOUR ADJUSTER</span></div>
      <div id="captions">
        {{CAPS}}
      </div>
      <div class="tg" id="tg1"><span class="bx">All of it. <b>Day 1.</b></span></div>
      <div class="tg" id="tg2"><span class="bx">Claim <b>approved.</b> ✅</span></div>
      <div id="cta" class="clip" data-start="{{CTA}}" data-duration="{{CTA_DUR}}" data-track-index="4">
        <div class="cream"></div>
        <div id="ec-logo"><img src="assets/media/crew_logo.png" alt="CREW — Restore, Revamp, Rebuild" /></div>
        <div class="c" id="ec-line">Insurance claim? <em>Call CREW.</em></div>
        <div class="c" id="ec-phone"><span id="ec-pill"><svg viewBox="0 0 24 24" fill="#fff"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z" /></svg>605-965-2727<i id="shine" data-layout-allow-overflow></i></span></div>
        <div class="c" id="ec-tag">“We Are The Crew That Cares.”</div>
        <div class="c" id="ec-web">SIOUX FALLS, SD · CREW3R.COM</div>
      </div>
      <div id="grain"></div>
    </div>
    <audio id="music" src="assets/media/music.wav" data-start="0" data-duration="{{TOTAL}}" data-volume="1" data-track-index="10" data-automation='{{MUSIC_AUTO}}'></audio>
{{SFX}}
    <script>
      const tl = gsap.timeline({ paused: true });
      const EO = "power3.out";
      function enter(sel, t) {
        tl.fromTo(sel, { opacity: 0, scale: 1.06, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: EO }, t);
      }
      function cap(sel, a, b) {
        tl.fromTo(sel, { opacity: 0, y: 16, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.22, ease: "back.out(1.8)" }, Math.max(0, a - 0.06));
        tl.to(sel, { opacity: 0, duration: 0.08 }, b - 0.08);
      }
      function word(sel, t) {
        const el = document.querySelector(sel);
        tl.fromTo(sel, { color: "#707076" }, { color: el && el.classList.contains("hl") ? "#e8262b" : "#141416", duration: 0.06, immediateRender: false }, t);
        tl.fromTo(sel, { scale: 1 }, { scale: 1.06, duration: 0.08, yoyo: true, repeat: 1, ease: "power1.out", immediateRender: false }, t);
      }
      function tag(sel, a, b) {
        tl.fromTo(sel, { opacity: 0, y: 20, scale: 0.94 }, { opacity: 1, y: 0, scale: 1, duration: 0.3, ease: "back.out(1.8)" }, a);
        tl.to(sel, { opacity: 0, duration: 0.15 }, b - 0.15);
      }
      function flash(t, p = 0.6, d = 0.28) { tl.fromTo("#flash", { opacity: p }, { opacity: 0, duration: d, ease: "power2.out", immediateRender: false }, t); }
      function shake(t, dur, amp) {
        const n = Math.round(dur / 0.04);
        for (let i = 0; i < n; i++) { const k = 1 - i / n; tl.to("#world", { x: Math.sin(i * 2.7 + t * 13) * amp * k, y: Math.cos(i * 3.9 + t * 7) * amp * 0.8 * k, duration: 0.04, ease: "none" }, t + i * 0.04); }
        tl.to("#world", { x: 0, y: 0, duration: 0.05 }, t + n * 0.04);
      }
      function leak(t, d = 1.0) {
        tl.fromTo("#leak", { opacity: 0, x: -500 }, { opacity: 0.7, x: -100, duration: d * 0.45, ease: "power2.out", immediateRender: false }, t);
        tl.to("#leak", { opacity: 0, x: 400, duration: d * 0.55, ease: "power2.in" }, t + d * 0.45);
      }
      tl.set("#cam", { scale: 1 }, 0);
      tl.set("#world", { x: 0, y: 0 }, 0);
/*{{JS}}*/
      // cold open
      tl.fromTo("#k-denied", { opacity: 0, scale: 1.5, rotation: -6 }, { opacity: 1, scale: 1, rotation: -3, duration: 0.25, ease: "back.out(2)" }, 0.35);
      tl.to("#k-denied", { opacity: 0, duration: 0.12 }, 1.42);
      tl.fromTo("#tag", { opacity: 0, y: -20 }, { opacity: 1, y: 0, duration: 0.3, ease: EO }, 1.6);
      tl.to("#tag", { opacity: 0, duration: 0.2 }, 3.05);
      // behind-head words
      tl.set("#bt1", { opacity: 1 }, 7.4);
      tl.fromTo("#bt1 .b.red", { opacity: 0, scale: 1.8 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, 7.4);
      tl.fromTo("#bt1 .b:not(.red)", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.25, ease: EO }, 8.55);
      tl.set("#bt1", { opacity: 0 }, 9.5);
      tl.set("#bt2", { opacity: 1 }, 19.75);
      tl.fromTo("#bt2 .s", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.25, ease: EO }, 19.75);
      tl.fromTo("#bt2 .b", { opacity: 0, scale: 1.7 }, { opacity: 1, scale: 1, duration: 0.22, ease: "power4.out" }, 19.84);
      tl.set("#bt2", { opacity: 0 }, 22.5);
      // approved stamp
      tl.fromTo("#stamp", { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.in" }, 15.1);
      tl.to("#stamp", { opacity: 0, duration: 0.15 }, 15.85);
      // outro tags
      tag("#tg1", 22.65, 25.55); tag("#tg2", 27.75, 29.6);
      // hits
      flash(0, 0.8, 0.35); shake(0.02, 0.5, 18); shake(0.75, 0.4, 14);
      flash(1.5, 0.45, 0.25); leak(1.45, 1.0);
      flash(7.4, 0.55, 0.3); shake(7.42, 0.35, 16);
      flash(9.5, 0.4, 0.25);
      shake(15.3, 0.3, 14);
      flash(19.84, 0.5, 0.25); shake(19.86, 0.3, 14);
      flash(22.5, 0.45, 0.3); leak(22.45, 1.0);
      // CTA
      tl.fromTo("#cta", { opacity: 0 }, { opacity: 1, duration: 0.45, ease: "power1.inOut" }, {{CTA}});
      tl.fromTo("#ec-logo", { opacity: 0, y: 30, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: EO }, {{CTA}} + 0.2);
      tl.fromTo("#ec-line", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: EO }, {{CTA}} + 0.55);
      tl.fromTo("#ec-phone", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.5, ease: EO }, {{CTA}} + 0.8);
      tl.fromTo("#ec-tag", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, ease: EO }, {{CTA}} + 1.05);
      tl.fromTo("#ec-web", { opacity: 0 }, { opacity: 1, duration: 0.5 }, {{CTA}} + 1.3);
      tl.fromTo("#shine", { x: -200 }, { x: 760, duration: 0.9, ease: "power2.inOut" }, {{CTA}} + 1.6);
      for (let i = 0; i < {{TOTAL}} * 12; i++) tl.set("#grain", { x: ((i * 73) % 200) - 100, y: ((i * 131) % 200) - 100 }, i / 12);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
