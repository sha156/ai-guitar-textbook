# 吉他教学大纲精排版（bcq）— 维护手册

本项目维护一份出版物级的吉他课程教学大纲 PDF（35 课 · 四阶段），XeLaTeX 排版。
交付物：`吉他课程教学大纲_第1-35课_精排版.pdf`（项目根目录，编译后从 build/tex/main.pdf 复制过来）。

## 内容红线（最高优先级，任何维护都不得违反）

1. **课文唯一真源是 `build/content_extracted.txt`**（从原始 PDF 提取的 35 课全文）。
   卡片内「教学目标 / 教学内容 / 课堂练习」三层文字必须逐字来自该文件，禁止改写、增删、润色。
2. **不发明数字**：学时、BPM、百分比、难度星级等原文没有的数字一律不加；
   建议性数字须明确标注为建议且有普适依据。
3. ⚠️ 历史调研中出现过一套**假课名**（入门筑基/和弦弹唱/进阶技巧/表演与风格）——那是调研残留，
   与本大纲无关，看到即忽略。真实阶段名：基础指法节奏与和弦 / 技巧进阶与伴奏应用 /
   指板音阶与即兴 / 曲目 Solo 专项。
4. **「图解笔记」的边界**：笔记只讲怎么读图、动作要领、练习方法，可延伸标准吉他教学常识，
   但不得与课文冲突、不得替课程新增教学内容（新增课程内容必须先进 content_extracted.txt）。
5. 第 31--35 课原文仅有标题（见整理说明），卡片照实呈现「暂保留课程标题」；
   将来细化时先更新 content_extracted.txt，再填 stage4.tex。

## 工程结构

```
build/tex/
  main.tex             入口：字体、geometry、hyperref、graphicspath、\input 顺序
  guitar-macros.sty    设计系统（全部组件与色板，唯一定义点）
  frontmatter.tex      整理说明 + 使用说明 + 全书路线图
  stage1.tex ~ stage4.tex   四个阶段：阶段扉页 + 课程卡片（含全部图与笔记）
  appendix.tex         附录·曲库总表
  backcover.tex        封底（纯 TikZ 设计）
build/images/ai/       AI 插画（gen_guitar_ai.py / gen_batch2.py 生成）
build/images/wiki/     旧版下载的 Wikimedia 照片（已弃用，仅留档）
build/content_extracted.txt   课文唯一真源（禁改，除非原大纲更新）
build/CHECKPOINT.md    进度与决策记录（每次大改后更新）
build/PLAN.md          初版制作计划（历史文档）
```

## 设计系统速查（都在 guitar-macros.sty）

- **色板**：主色 mainNavy #1B2A4A；阶段色 stageA #2E86AB（一）/ stageB #0F8B8D（二）/
  stageC #C89B3C（三）/ stageD #A63A50（四）；正文 inkGray #3C4048。
  正文只准引用色名；`stagecur` 是当前阶段别名。
- **`\SetStage{色名}{阶段名}{课程范围}`**：每个阶段文件开头调用一次，页眉、卡片、
  列表符号、笔记框全部自动换色。
- **`\stagepage{号}{色}{名}{范围}{导览}{左列}{右列}`**：整页阶段扉页。
- **`lessoncard` 环境**：`\begin{lessoncard}{课号}{课题}`，卡内用
  `\cardsec{\faBullseye}{教学目标}` 等三个子块；选曲行用 `\songrow{标签}{内容}`
  （标签只有四种：选曲/曲目练习/长期作业/结课曲目，与原文一致）。
- **`fignote` + `fignotes`**：图解笔记块。图放 center 里，笔记 `\begin{fignotes}\item ...`
  固定 3 条左右，footnotesize。
- **绘图组件**：`fretboard` 环境 + `\fbmark`/`\fbroot`（指板音位图，弦 1=高音e 在上）；
  `chordbox` + `\cbdot`/`\cbbarre`/`\cbopen`/`\cbmute`（竖版和弦窗格，品为窗口内相对品）；
  `\chordscheme[...]`（guitarchordschemes 包，横版和弦图，键语法 finger={品/弦:指}）；
  `rpattern` + `\rnhead`/`\rndot`/`\rnflag`/`\rnbeamA/B`（节奏块）；
  `\stepchip{}` + `\steparrow`（流程链）；`\photo[高]{文件}`（圆角细边图片）；
  `\figcaption{}`（无编号图注）；`\pagehead{}`（附录式页标题）。

## 编译与验收（假修复防线，必须走完）

```bash
cd D:/Project/py/bcq/build/tex
xelatex -interaction=nonstopmode main.tex   # 第 1 遍
xelatex -interaction=nonstopmode main.tex   # 第 2 遍（remember picture 对位必须两遍）
grep -E "^!|Missing character" main.log     # 必须为空
pdftoppm -png -r 100 main.pdf qa/p          # 渲染 PNG
```

- latexmk 不可用（缺 perl），别尝试。
- 西文字体带跨平台回退（Windows: Palatino/Segoe UI；其他平台自动落到 TeX Gyre），
  中文由 ctex 按平台自选——改字体只动 main.tex 的 \IfFontExistsTF 分支。
- **CI**：push/PR 会触发 `.github/workflows/build.yml`（TeX Live 容器编两遍 + 错误/缺字检查）。
  本地过了 CI 红了，优先怀疑 Fandol 字库缺字或包版本差异。
- **许可**：双许可（工程 MIT + 课文 CC BY-NC 4.0，见 LICENSE / LICENSE-CONTENT.md）；
  给课程正文添加内容前注意贡献即视为接受该许可（CONTRIBUTING.md 有声明）。
- **改动涉及的页必须逐页目检 PNG**（Read 工具看图）：查溢出、错位、缺字、图文重叠、页眉换色。
- **对账清单**：lessoncard=35、\songrow=11、\pdfbookmark[2]=35、页数与上版对比可解释。
- 验收通过后：`cp main.pdf ../../吉他课程教学大纲_第1-35课_精排版.pdf`，并更新 CHECKPOINT.md。

## AI 插画（生成新图时看这里）

- 双通道脚本：`build/gen_guitar_ai.py`（right.codes 优先 → tokeness 兜底；
  sample/all/序号三种模式）；第二批任务在 `build/gen_batch2.py`。
- 通道配置在 `~\.claude\secrets\imagegen*.env`，接口细节与坑见全局 gpt-image2 skill
  （right.codes 是异步接口：提交拿 task_id 再轮询；文档示例模型 nano-banana-fast 不存在）。
- **模型选型**：场景/整身人物用 nano-banana-2（便宜、风格稳）；
  手部结构图（横按、按弦特写）必须用 gpt-image-2（nano-banana 手部解剖不可靠）。
  上游偶发 "excessive system load"，隔 20 秒重试即可。
- **风格合同**（prompt 里必须带）：flat vector、白底、无渐变无阴影、
  配色锁 #1B2A4A/#0F8B8D/#C89B3C、**图内绝对无文字**（中文必乱码，英文也不要）、no border。
- **纪律**：先出样张目检再批量；每张生成后必须目检（手部解剖、左右手、有无边框、有无彩甲
  之类怪东西）；**动作错误的教学图宁可弃用**，错误示范比没图更糟。

## 已踩坑（勿再犯）

1. 附录内容超出一页 1--2mm 会溢出一张"空页"，且该页页眉 overlay 坐标漂移成整页色块
   →内容临界时收紧 \vspace，页数异常先怀疑这个。
2. Palatino 缺 ■ ○ ◌ → 等几何字符 → 用 \rule 色块 / 内联 TikZ / 文字表述替代。
3. `\rhead` 与 fancyhdr 冲突 → 节奏宏全部用 rn 前缀（\rnhead 等）。
4. fontawesome5 部分图标无专名宏（如 sync-alt）→ 用 \faIcon{kebab-name}。
5. chordscheme 换把位：position={n} 只印把位数字，finger/barre 品号写窗口内相对品。
6. 裸 python 是 3.9，跑脚本一律用
   `C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe`。
7. bash 的 /tmp 与 Windows Python 路径不互通，中转文件放 scratchpad 或项目 build 目录。

## 常见维护任务

- **改某课文字**：先改 content_extracted.txt（若是原大纲更新），再同步 stageN.tex 对应卡片。
- **给某课加图**：图 + 笔记包进 `fignote`，TikZ 风格对齐现有组件（inkGray 主线、stagecur 强调、
  Stealth 箭头、footnotesize sffamily 标签）。
- **细化第 31--35 课**：更新真源 → stage4.tex 按 stage1-3 的卡片模板填三层内容。
- **换配色**：只动 guitar-macros.sty 色板区，正文零改动。
