import ffmpeg
import os


def change_tempo(filename, tempo: float):
    tmp_file = f"{filename}.tmp"
    os.rename(filename, tmp_file)
    ffmpeg.input(tmp_file).filter("atempo", tempo).output(
        filename).overwrite_output().run(quiet=True)
    os.unlink(tmp_file)


def get_duration(filename):
    f = ffmpeg.probe(filename)
    return float(f.get("format", {}).get("duration", "1.0"))
