# usage: asr.py MODEL_DIR in.wav(16k mono) out.json  -> {"text","words":[{text,start,end}]}
import sys, json, sherpa_onnx, soundfile as sf, numpy as np
md, wav, out = sys.argv[1:4]
r = sherpa_onnx.OfflineRecognizer.from_transducer(encoder=f"{md}/encoder.int8.onnx", decoder=f"{md}/decoder.int8.onnx",
    joiner=f"{md}/joiner.int8.onnx", tokens=f"{md}/tokens.txt", model_type="nemo_transducer", num_threads=4)
a, sr = sf.read(wav, dtype="float32")
if a.ndim > 1: a = a.mean(1)
words, texts = [], []
CH = 25 * sr
for off in range(0, len(a), CH):
    st = r.create_stream(); st.accept_waveform(sr, a[off:off + CH]); r.decode_stream(st)
    res = st.result; texts.append(res.text.strip()); toks, ts = res.tokens, res.timestamps
    cur = None
    for i, (tk, t) in enumerate(zip(toks, ts)):
        t += off / sr
        if tk.startswith(" ") or tk.startswith("▁") or cur is None:
            if cur: words.append(cur)
            cur = {"text": tk.strip(" ▁"), "start": t, "end": t + 0.16}
        else:
            cur["text"] += tk; cur["end"] = t + 0.16
        if i + 1 < len(ts): cur["end"] = max(cur["end"], ts[i + 1] + off / sr)
    if cur: words.append(cur)
words = [w for w in words if w["text"]]
json.dump({"text": " ".join(texts), "words": words}, open(out, "w"), indent=0)
print(" ".join(texts))
for w in words: print(f'{w["start"]:6.2f}-{w["end"]:6.2f} {w["text"]}')
