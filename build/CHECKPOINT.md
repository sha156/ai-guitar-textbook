# 吉他教学大纲 LaTeX 重排版 — 进度检查点

> 更新时间：2026-07-20（第 2 版：全矢量 + 图解笔记）。**任务已完成交付。**
> 产物：`D:\Project\py\bcq\吉他课程教学大纲_第1-35课_精排版.pdf`（38 页，468 KB，纯矢量无位图）

## 完成状态（v2）

- 应用户要求撤掉全部实拍照片（风格不统一），改为 **17 套统一风格 TikZ 矢量图 + 图解笔记**：
  每套 = 图 + 「图解笔记」讲解块（fignote/fignotes 组件，随阶段换色）。
- 图清单：L1 指板构造标注图、L2 节奏型条、L3 附点节奏、L4 C+Am 和弦图读法、L6 扫弦方向、
  L7 大小三和弦构成堆叠、L10 Bm 大横按、L11 击/勾/滑三联、L13 节拍器、L14 调内和弦级数
  （C 大调示范）、L16 强力和弦 E5/A5、L19 推弦+揉弦、L21 CAGED 五指型、L24 人工泛音驻波、
  L26 琶音构成、L28 A 小调五声指板、L29 直八 vs Swing 三连音对比。
- 封底改纯设计（音孔同心圆 + 金色吉他图标）；附录 B 图片授权已删（无外部图片）；
  使用说明加了「图解笔记」组件说明。
- 35 课课文仍逐字来自 content_extracted.txt；笔记只讲"怎么读图/动作要点"，与课文一致不冲突。
- QA：38 页 PNG 逐页目检通过；对账 35 课卡 / 11 曲目徽章 / 17 图解笔记 / 0 照片。

## 工程位置

- LaTeX 工程：`build\tex\`（main.tex + guitar-macros.sty + frontmatter/stage1-4/appendix/backcover.tex）
- 编译：`xelatex -interaction=nonstopmode main.tex` 两遍；QA：`pdftoppm -png -r 100 main.pdf qa/p`
- `build\images\` 里的 wiki 照片已不再引用，仅留档

## v3 更新（2026-07-20 晚）：right.codes 通道打通，AI 插画已加入

- 用户提供 right.codes key（rc_draw 异步接口，配置在 `~\.claude\secrets\imagegen-right.env`，
  **key 曾在对话贴出，建议轮换**）。通道事实已沉淀进 gpt-image2 skill 并 push harness 仓库。
- 3 张 AI 插画（全书同配色扁平矢量风）已嵌入：L1 持琴坐姿 + 拨片握法（nano-banana-2），
  L10 大横按手型（gpt-image-2——nano-banana-2 画横按解剖连错两次，结构性手型图用 gpt-image-2）。
- 生成脚本 `build\gen_guitar_ai.py`（right 优先→tokeness 兜底，样张/批量/指定序号三种模式）。
- 重编译 38 页逐项目检通过，交付 PDF 已更新（2.6 MB）。

## v4 完成（2026-07-20 深夜）：满配图 + 全课笔记 + 项目 CLAUDE.md
> 终态：43 页 PDF 已交付；对账 35 课卡 / 11 曲目徽章 / **31 个图解笔记块（1--30 课全覆盖）** /
> 8 张 AI 插画全部在用；逐页目检通过。gpt-image-2 上游 "excessive system load" 为临时错误，
> 隔 20 秒重试即过（已写进 CLAUDE.md）。流程链组件 \stepchip 过长会折行悬空箭头，
> 一律包 adjustbox{max width=\textwidth} 缩放到一行。

- 目标：1--30 课每课至少一个「图 + 图解笔记」块。新补 13 课：
  L5/L17/L18/L25/L27/L30 流程链（stepchip 组件）、L12 双滑与断音示意、L15 小指击弦示意、
  L22 八度指型指板图、L23 相邻把位串联指板图（重叠音金圈 + 滑音箭头）、
  L8 爬格子手型（AI）、L9 右手分解拨弦（AI）、L20 结课舞台（AI）；
  L16 加掌根闷音特写（AI）；第四阶段页加双吉他 Solo 插画（AI）。
- 新组件：\stepchip + \steparrow 流程链（guitar-macros.sty）。
- AI 第二批 5 张：stage_solo / duo_solo（nano-banana-2，一次过）；
  crawl / pick_strings / palm_mute（gpt-image-2，上游 "excessive system load" 重试中）。
- 新增项目根 `CLAUDE.md`：内容红线、组件速查、编译与对账流程、AI 插画规范、踩坑清单。

## 遗留事项（可选后续）

1. tokeness 通道额度仍为负（¥-0.017），充值后可作兜底。
2. 第 31-35 课原文只有标题；细化后填 stage4.tex，可复用 fignote 组件。
3. 踩坑：附录超页 1-2mm 会溢出空页且页眉 overlay 坐标漂移成整页色块（收紧 \vspace 解决）；
   Palatino 缺 ■ ○ ◌ 等几何字符（用 \rule / TikZ / 文字表述替代）；\rhead 与 fancyhdr 冲突（改名 \rnhead）。

## v5（2026-07-20）：发布 GitHub 公开仓库

- https://github.com/sha156/ai-guitar-textbook （public，34 个文件，含成品 PDF + 全部 tex 源 + README）
- 弃用素材（wiki 照片、早期自备 jpg）与编译中间产物已 gitignore，未入库；push 前密钥扫描干净。
- 本地 D:\Project\py\bcq 已初始化为 git 仓库（main 分支跟踪 origin/main），后续改动直接 commit+push。

## v6（2026-07-21）：协作化改造完成

- 跨平台字体回退（IfFontExistsTF → TeX Gyre）；CI（TeX Live 容器编两遍+错误/缺字检查）
  **首跑即绿**（run 29753115781，3m20s），证明 Linux 环境可完整复现编译。
- 双许可落地：工程 MIT + 课文 CC BY-NC 4.0；CONTRIBUTING.md 面向人类协作者；
  docs/ai-prompts.md 收录 8 张插画全套提示词与风格合同。
