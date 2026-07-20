# AI 插画提示词手册

本教材的 8 张 AI 插画全部按同一套「风格合同」生成，保证与 TikZ 矢量图视觉统一。
想重新生成或补新图，照抄本文的合同和模板即可。脚本在 `build/gen_guitar_ai.py` /
`build/gen_batch2.py`（密钥从本地 env 文件读取，不入库）。

## 风格合同（每条 prompt 必须带）

```text
Flat vector illustration for a printed guitar method book. Clean minimal
line-art, crisp outlines, no gradients, no drop shadows, plain white
background. Color palette strictly limited to: deep navy #1B2A4A outlines,
teal #0F8B8D and brass gold #C89B3C accents, light warm gray fills.
Absolutely no text, no letters, no numbers, no labels, no watermark anywhere.
```

要点：
- **配色锁死**三个主题色（藏青描边 / 青、金点缀），与全书 `guitar-macros.sty` 色板一致
- **图内绝对无文字**：中文必乱码，英文数字也一律禁止，标注全部留给 LaTeX 层
- 整身/场景图额外加 `generous white margin, no border, no frame`（防止模型自作主张画外框）

## 模型选型（实测结论）

| 场景 | 模型 | 原因 |
|---|---|---|
| 整身人物、舞台场景 | nano-banana-2 | 便宜、风格稳定，一次过 |
| 手部结构特写（横按、按弦、握拨片） | gpt-image-2 | nano-banana 手部解剖不可靠（横按连错两次：弯指扣弦画不成直条横压） |

其他实测：上游偶发 `excessive system load` 是临时错误，隔 20 秒重试即过；
生成后必须逐张目检——重点看左右手是否搞反、手指数量与姿态、有没有多余边框和
彩色指甲之类的怪东西。**动作错误的教学图宁可弃用**。

## 8 张成图的完整提示词

以下每条 prompt 结尾都要拼接上面的风格合同（表中省略）。

### 1. posture.png — 持琴坐姿（第 1 课）｜nano-banana-2｜1:1

```text
A person sitting upright on a stool playing an electric guitar, correct
playing position: the guitar waist rests on the right thigh, the right
forearm drapes over the guitar body with the hand near the strings above the
pickups, and the LEFT hand wraps around the guitar neck with fingers curled
onto the fretboard. Six strings visible along the neck. Relaxed straight
back and shoulders. Three-quarter front view, full figure, generous white
margin around the subject, no border, no frame, no outline box around the
image edge.
```

> 第一版失败教训：不强调 "LEFT hand wraps around the neck" 时，模型把左手画在膝盖上。

### 2. pick_grip.png — 拨片握法（第 1 课）｜nano-banana-2｜1:1

```text
Instructional close-up of how to hold a guitar plectrum: a large flat
triangular guitar pick in brass gold color, clearly visible, held between
the thumb pad and the side of the index finger, with the pointed tip of the
pick sticking out; the other three fingers gently curled away. The gold
pick is the focal point and the ONLY gold element. Plain light-gray skin,
absolutely no colored fingernails, no nail polish. Side view, large and clear.
```

> 第一版失败教训：不写 "no colored fingernails" 时，模型把青色点缀用在指甲上，像美甲图。

### 3. barre_hand.png — 大横按手型（第 10 课）｜gpt-image-2｜4:3

```text
Instructional close-up of a barre chord on a guitar neck, viewed from the
front of the fretboard: the LEFT index finger lies perfectly flat and
straight like a bar, pressing down ALL six strings at once directly behind
one fret wire, spanning the full width of the fretboard from the lowest
string to the highest string; the middle, ring and little fingers arch over
and press separate strings on higher frets; the thumb is hidden behind the
neck. Six strings and fret wires clearly visible.
```

### 4. crawl.png — 爬格子一指一品（第 8 课）｜gpt-image-2｜4:3

```text
Instructional close-up of a left hand doing the one-finger-per-fret spider
exercise on a guitar fretboard, viewed from the front: four fingers lined up
over four consecutive frets on the SAME string, the index finger pressing
the string down just behind a fret wire, the other three fingertips hovering
very low and close above the same string ready to press, thumb hidden behind
the neck. Six strings and fret wires clearly visible.
```

### 5. pick_strings.png — 右手分解拨弦（第 9 课）｜gpt-image-2｜4:3

```text
Instructional close-up of a right hand playing fingerstyle-like arpeggios
with a pick on an electric guitar: the hand holds a small brass gold
triangular pick between thumb and index finger, picking one single middle
string above the pickups, wrist relaxed and gently arched, remaining fingers
loosely curled. All six strings and two pickups visible. No colored
fingernails.
```

### 6. palm_mute.png — 掌根闷音（第 16 课）｜gpt-image-2｜4:3

```text
Instructional close-up of palm muting on an electric guitar: the fleshy
outer edge of the right palm rests lightly on the strings exactly at the
bridge, while the hand holds a brass gold triangular pick striking a low
string. Bridge, pickups and all six strings clearly visible, side
three-quarter view. No colored fingernails.
```

### 7. stage_solo.png — 结课舞台独奏（第 20 课）｜nano-banana-2｜1:1

```text
A guitarist standing on a small stage playing an electric guitar solo,
leaning slightly back, left hand high on the neck, right hand striking the
strings; two simple spotlight beams from above and a few small monitor
wedges at the stage edge. Full figure, energetic but clean composition,
generous white margin, no border, no frame.
```

### 8. duo_solo.png — 双吉他 Solo（第四阶段页）｜nano-banana-2｜16:9

```text
Two guitarists standing side by side playing a twin guitar solo together on
stage, both with electric guitars, mirrored relaxed poses, one guitar body
teal and the other brass gold; two simple spotlight beams behind them. Full
figures, wide composition, generous white margin, no border, no frame.
```

## 通道配置（不含密钥）

脚本按顺序尝试两个通道，配置文件放在本地 `~/.claude/secrets/`（永不入库）：

```env
# imagegen-right.env —— right.codes rc_draw 异步接口
RC_DRAW_BASE=https://www.right.codes/draw
RC_TASKS_BASE=https://www.right.codes
RC_API_KEY=<你的 key>
RC_MODEL=nano-banana-2

# imagegen.env —— OpenAI 兼容同步接口（兜底）
IMAGEGEN_BASE_URL=<兼容端点>/v1
IMAGEGEN_API_KEY=<你的 key>
IMAGEGEN_MODEL=gpt-image-2
```

rc_draw 是异步接口：`POST {RC_DRAW_BASE}/v1/images/generations`（body 带
`"async": true`）返回 task_id，再轮询 `GET {RC_TASKS_BASE}/v1/tasks/{task_id}`
直到 `completed`。可用模型查 `GET {RC_DRAW_BASE}/v1/models`。
