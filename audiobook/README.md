# The Sex Life of Furniture — audiobook

Narrated with Kokoro (open-source neural TTS, `kokoro-onnx`), British English.
No real performer's voice is cloned or imitated; the voice is a synthetic
deep-register British male narrator in a measured, theatrical style.

| File | Voice | Notes |
|------|-------|-------|
| `The_Sex_Life_of_Furniture.m4b` / `.mp3` | `bm_george`, speed 0.88, pitch lowered ~1.5 semitones | Primary take |
| `The_Sex_Life_of_Furniture_alt_take_Lewis.m4b` / `.mp3` | `bm_lewis`, speed 0.90, no pitch shift | Deeper alternate take |

Both files run about 16 minutes and carry chapter markers (title + Parts One to Five).
Loudness normalised to -18 LUFS, 44.1 kHz mono.

Source text: `../source/Audiobook_Narration_Script.txt` (narration notes stripped,
headings read as "Part One" etc., pauses after headings and a beat before the
final three paragraphs, citations omitted). Rebuild with `../source/build_audiobook.py`
and `../source/package.py`; model files are downloaded from the kokoro-onnx GitHub releases.
