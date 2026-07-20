# -*- coding: utf-8 -*-
"""吉他大纲 AI 插画生成。

通道 1（优先）：right.codes rc_draw 异步接口（提交→轮询 task）
通道 2（兜底）：tokeness OpenAI 同步接口

用法（Python 3.11）：
    python gen_guitar_ai.py sample   # 只生成第 1 张样张（默认）
    python gen_guitar_ai.py all      # 样张确认后生成全部 3 张
    python gen_guitar_ai.py 2 3      # 只生成指定序号
"""
import base64
import io
import os
import sys
import time

import requests

RIGHT_ENV = r"C:\Users\Administrator\.claude\secrets\imagegen-right.env"
TOKENESS_ENV = r"C:\Users\Administrator\.claude\secrets\imagegen.env"
OUT_DIR = r"D:\Project\py\bcq\build\images\ai"

STYLE = (
    "Flat vector illustration for a printed guitar method book. Clean minimal "
    "line-art, crisp outlines, no gradients, no drop shadows, plain white "
    "background. Color palette strictly limited to: deep navy #1B2A4A "
    "outlines, teal #0F8B8D and brass gold #C89B3C accents, light warm gray "
    "fills. Absolutely no text, no letters, no numbers, no labels, no "
    "watermark anywhere."
)

JOBS = [
    (
        "posture.png",
        "1:1",
        "A person sitting upright on a stool playing an electric guitar, "
        "correct playing position: the guitar waist rests on the right "
        "thigh, the right forearm drapes over the guitar body with the hand "
        "near the strings above the pickups, and the LEFT hand wraps around "
        "the guitar neck with fingers curled onto the fretboard. Six strings "
        "visible along the neck. Relaxed straight back and shoulders. "
        "Three-quarter front view, full figure, generous white margin "
        "around the subject, no border, no frame, no outline box around the "
        "image edge. " + STYLE,
    ),
    (
        "pick_grip.png",
        "1:1",
        "Instructional close-up of how to hold a guitar plectrum: a large "
        "flat triangular guitar pick in brass gold color, clearly visible, "
        "held between the thumb pad and the side of the index finger, with "
        "the pointed tip of the pick sticking out; the other three fingers "
        "gently curled away. The gold pick is the focal point and the ONLY "
        "gold element. Plain light-gray skin, absolutely no colored "
        "fingernails, no nail polish. Side view, large and clear. " + STYLE,
    ),
    (
        "barre_hand.png",
        "4:3",
        "Instructional close-up of a barre chord on a guitar neck, viewed "
        "from the front of the fretboard: the LEFT index finger lies "
        "perfectly flat and straight like a bar, pressing down ALL six "
        "strings at once directly behind one fret wire, spanning the full "
        "width of the fretboard from the lowest string to the highest "
        "string; the middle, ring and little fingers arch over and press "
        "separate strings on higher frets; the thumb is hidden behind the "
        "neck. Six strings and fret wires clearly visible. " + STYLE,
    ),
]


def load_env(path):
    cfg = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    cfg[k.strip()] = v.strip()
    return cfg


def fetch(url):
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return r.content


def save(blob, fname):
    out_path = os.path.join(OUT_DIR, fname)
    with open(out_path, "wb") as f:
        f.write(blob)
    try:
        from PIL import Image
        im = Image.open(io.BytesIO(blob))
        print(f"OK {out_path}  实际尺寸 {im.size[0]}x{im.size[1]}")
    except ImportError:
        print(f"OK {out_path}  ({len(blob)} bytes)")


def via_right(cfg, fname, size, prompt):
    r = requests.post(
        f"{cfg['RC_DRAW_BASE']}/v1/images/generations",
        headers={"Authorization": f"Bearer {cfg['RC_API_KEY']}",
                 "Content-Type": "application/json"},
        json={"model": cfg["RC_MODEL"], "prompt": prompt, "n": 1,
              "size": size, "async": True},
        timeout=60,
    )
    r.raise_for_status()
    task_id = r.json()["task_id"]
    print(f"    task_id={task_id}, 轮询中...")
    for i in range(60):
        time.sleep(5)
        q = requests.get(
            f"{cfg['RC_TASKS_BASE']}/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {cfg['RC_API_KEY']}"},
            timeout=60,
        )
        q.raise_for_status()
        j = q.json()
        status = j.get("status")
        if status == "failed":
            raise RuntimeError(f"任务失败: {j.get('error')}")
        if status == "completed" or "data" in j:
            item = j["data"][0]
            if item.get("b64_json"):
                blob = base64.b64decode(item["b64_json"])
            else:
                blob = fetch(item["url"])
            save(blob, fname)
            return
        print(f"    ...{status} {j.get('progress', '?')}%")
    raise TimeoutError("轮询 5 分钟未完成")


def via_tokeness(cfg, fname, size, prompt):
    r = requests.post(
        f"{cfg['IMAGEGEN_BASE_URL']}/images/generations",
        headers={"Authorization": f"Bearer {cfg['IMAGEGEN_API_KEY']}"},
        json={"model": cfg["IMAGEGEN_MODEL"], "prompt": prompt,
              "size": "1024x1024"},
        timeout=300,
    )
    r.raise_for_status()
    item = r.json()["data"][0]
    blob = (base64.b64decode(item["b64_json"]) if item.get("b64_json")
            else fetch(item["url"]))
    save(blob, fname)


def main():
    args = sys.argv[1:] or ["sample"]
    if args == ["sample"]:
        picked = [0]
    elif args == ["all"]:
        picked = list(range(len(JOBS)))
    else:
        picked = [int(a) - 1 for a in args]
    right = load_env(RIGHT_ENV)
    tokeness = load_env(TOKENESS_ENV)
    os.makedirs(OUT_DIR, exist_ok=True)
    ok = 0
    for i in picked:
        fname, size, prompt = JOBS[i]
        print(f"=== [{i + 1}/{len(JOBS)}] {fname}")
        try:
            via_right(right, fname, size, prompt)
            ok += 1
            continue
        except Exception as e:
            msg = str(e)
            if hasattr(e, "response") and getattr(e, "response") is not None:
                msg += " | " + e.response.text[:200]
            print(f"    right.codes 失败: {msg}")
        try:
            via_tokeness(tokeness, fname, size, prompt)
            ok += 1
        except Exception as e:
            print(f"    tokeness 兜底也失败: {e}")
    print(f"=== 完成 {ok}/{len(picked)} 张")


if __name__ == "__main__":
    main()
