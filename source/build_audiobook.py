"""Render the narration script to a chaptered audiobook with Kokoro TTS."""
import re, sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

SCRIPT = "/root/.claude/uploads/878d03a8-1bf8-5670-b348-cf5e513251b7/ef71606d-Audiobook_Narration_Script.txt"
voice = sys.argv[1]; speed = float(sys.argv[2]); outdir = sys.argv[3]
import os; os.makedirs(outdir, exist_ok=True)

# Pronunciation respellings for words the English phonemizer mangles.
FIX = [
    ("étudiant·e·s", "ay-tood-YON, dot, E, dot, S"),
    ("dōnum", "DOH-num"),
    ("Gygax", "GHEE-gax"),
    ("Conseil d’État", "con-SAY day-TAH"),
    ("Loporcaro", "Lo-por-CAR-oh"),
    ("Accademia della Crusca", "Acca-DAY-mia della CRUS-ka"),
    ("the Crusca", "the CRUS-ka"),
    ("ministra, avvocata, and sindaca", "min-EES-tra, avvo-CAH-ta, and SEEN-da-ka"),
    ("written ə", "written as an upside-down e"),
    ("—", ", "),
]
ROMAN = {"I": "One", "II": "Two", "III": "Three", "IV": "Four", "V": "Five"}

lines = open(SCRIPT, encoding="utf-8").read().split("\n")
# Drop the narration-notes block (everything before the title line).
start = lines.index("The Sex Life of Furniture")
body = [l.strip() for l in lines[start:] if l.strip()]

# Build a list of (kind, text) segments.
segs = []
for l in body:
    m = re.match(r"^(I|II|III|IV|V)\.\s+(.*)$", l)
    if l == "The Sex Life of Furniture" and not segs:
        segs.append(("title", l))
    elif m:
        segs.append(("heading", f"Part {ROMAN[m.group(1)]}. {m.group(2)}."))
    else:
        segs.append(("para", l))
# Mark the beat before the final three paragraphs.
n = len(segs); segs[n-3] = ("para_beat", segs[n-3][1])

def fix(t):
    for a, b in FIX: t = t.replace(a, b)
    return t

k = Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
SR = 24000
def sil(sec): return np.zeros(int(sec*SR), dtype=np.float32)
PAUSE = {"title": 2.0, "heading": 1.6, "para": 0.8, "para_beat": 0.8}
PRE   = {"title": 0.8, "heading": 1.8, "para": 0.0, "para_beat": 1.4}

out, chapters, t = [], [], 0.0
for kind, text in segs:
    pre = sil(PRE[kind]); out.append(pre); t += len(pre)/SR
    if kind in ("title", "heading"):
        chapters.append((t, text.rstrip(".") if kind == "heading" else text))
    audio, sr = k.create(fix(text), voice=voice, speed=speed, lang="en-gb")
    assert sr == SR
    audio = audio.astype(np.float32)
    out.append(audio); t += len(audio)/SR
    post = sil(PAUSE[kind]); out.append(post); t += len(post)/SR
    print(f"{kind:9s} {len(audio)/SR:6.1f}s  {text[:60]}", flush=True)
out.append(sil(2.0)); t += 2.0

full = np.concatenate(out)
full = 0.95 * full / np.max(np.abs(full))
sf.write(f"{outdir}/raw.wav", full, SR)
json.dump({"duration": t, "chapters": chapters}, open(f"{outdir}/chapters.json", "w"), indent=1)
print(f"total {t/60:.1f} min")
