# -*- coding: utf-8 -*-
"""吉他大纲 AI 插画第二批（5 张）。手部结构图用 gpt-image-2，整身/场景用 nano-banana-2。"""
import sys

sys.path.insert(0, r"D:\Project\py\bcq\build")
import gen_guitar_ai as g

STYLE = g.STYLE

BATCH = [
    # (文件名, 模型, 比例, prompt)
    (
        "crawl.png", "gpt-image-2", "4:3",
        "Instructional close-up of a left hand doing the one-finger-per-fret "
        "spider exercise on a guitar fretboard, viewed from the front: four "
        "fingers lined up over four consecutive frets on the SAME string, "
        "the index finger pressing the string down just behind a fret wire, "
        "the other three fingertips hovering very low and close above the "
        "same string ready to press, thumb hidden behind the neck. Six "
        "strings and fret wires clearly visible. " + STYLE,
    ),
    (
        "pick_strings.png", "gpt-image-2", "4:3",
        "Instructional close-up of a right hand playing fingerstyle-like "
        "arpeggios with a pick on an electric guitar: the hand holds a small "
        "brass gold triangular pick between thumb and index finger, picking "
        "one single middle string above the pickups, wrist relaxed and "
        "gently arched, remaining fingers loosely curled. All six strings "
        "and two pickups visible. No colored fingernails. " + STYLE,
    ),
    (
        "palm_mute.png", "gpt-image-2", "4:3",
        "Instructional close-up of palm muting on an electric guitar: the "
        "fleshy outer edge of the right palm rests lightly on the strings "
        "exactly at the bridge, while the hand holds a brass gold triangular "
        "pick striking a low string. Bridge, pickups and all six strings "
        "clearly visible, side three-quarter view. No colored fingernails. "
        + STYLE,
    ),
    (
        "stage_solo.png", "nano-banana-2", "1:1",
        "A guitarist standing on a small stage playing an electric guitar "
        "solo, leaning slightly back, left hand high on the neck, right "
        "hand striking the strings; two simple spotlight beams from above "
        "and a few small monitor wedges at the stage edge. Full figure, "
        "energetic but clean composition, generous white margin, no border, "
        "no frame. " + STYLE,
    ),
    (
        "duo_solo.png", "nano-banana-2", "16:9",
        "Two guitarists standing side by side playing a twin guitar solo "
        "together on stage, both with electric guitars, mirrored relaxed "
        "poses, one guitar body teal and the other brass gold; two simple "
        "spotlight beams behind them. Full figures, wide composition, "
        "generous white margin, no border, no frame. " + STYLE,
    ),
]


def main():
    cfg = g.load_env(g.RIGHT_ENV)
    ok = 0
    for fname, model, size, prompt in BATCH:
        c = dict(cfg)
        c["RC_MODEL"] = model
        print(f"=== {fname} ({model})")
        try:
            g.via_right(c, fname, size, prompt)
            ok += 1
        except Exception as e:
            msg = str(e)
            if hasattr(e, "response") and getattr(e, "response") is not None:
                msg += " | " + e.response.text[:200]
            print(f"    失败: {msg}")
    print(f"=== 完成 {ok}/{len(BATCH)} 张")


if __name__ == "__main__":
    main()
