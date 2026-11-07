import json, subprocess, sys, os
src, name, pitch, outdir = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
os.makedirs(outdir, exist_ok=True)
meta = json.load(open(f"{src}/chapters.json"))
chs = meta["chapters"]; dur = meta["duration"]
with open(f"{src}/ffmeta.txt", "w") as f:
    f.write(";FFMETADATA1\ntitle=The Sex Life of Furniture\nartist=Narrated with Kokoro TTS\nalbum=The Sex Life of Furniture\ngenre=Audiobook\n")
    for i, (t0, title) in enumerate(chs):
        t1 = chs[i+1][0] if i+1 < len(chs) else dur
        f.write(f"\n[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(t0*1000)}\nEND={int(t1*1000)}\ntitle={title}\n")
af = (f"rubberband=pitch={pitch}:formant=preserved," if pitch != 1.0 else "") + "loudnorm=I=-18:TP=-2:LRA=9"
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{src}/raw.wav","-af",af,"-ar","44100","-ac","1",f"{src}/master.wav"], check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{src}/master.wav","-i",f"{src}/ffmeta.txt","-map_metadata","1","-c:a","aac","-b:a","96k",f"{outdir}/{name}.m4b"], check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",f"{src}/master.wav","-i",f"{src}/ffmeta.txt","-map_metadata","1","-c:a","libmp3lame","-b:a","96k","-id3v2_version","3",f"{outdir}/{name}.mp3"], check=True)
print("done", name)
