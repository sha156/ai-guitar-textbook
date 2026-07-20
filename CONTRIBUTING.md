# 贡献指南

欢迎一起维护这份教材。规则不多，但下面几条是硬约束，PR 不满足会被打回。

## 内容红线（先读这个）

1. **课文的唯一真源是 `build/content_extracted.txt`**。要改 35 课的教学文字
   （教学目标/教学内容/课堂练习/选曲），必须**先改真源，再同步到对应的 `stageN.tex`**，
   两处保持逐字一致。只改 tex 不改真源的 PR 不收。
2. **不发明数字**：学时、BPM、百分比、难度等级等原文没有的量化信息一律不加。
3. **「图解笔记」只讲怎么读图、动作要领、练习方法**，可以是标准吉他教学常识，
   但不得与课文冲突、不得夹带新的课程内容。
4. 第 31–35 课原文只有标题，在真源细化之前，卡片保持「暂保留课程标题」现状。

更完整的设计系统说明（组件用法、色板、踩坑清单）见 [`CLAUDE.md`](./CLAUDE.md)。

## 本地环境

- 任意平台的 TeX 发行版均可：Windows 用 MiKTeX，Linux/macOS 用 TeX Live（需含
  ctex、tcolorbox、fontawesome5、guitarchordschemes、pgfornament）。
- 西文字体自动回退：Windows 用 Palatino/Segoe UI，其他平台用发行版自带的 TeX Gyre 系；
  中文由 ctex 按平台自动选择，无需手动装字体。

## 提交一个改动的完整流程

```bash
cd build/tex
xelatex -interaction=nonstopmode main.tex   # 必须编两遍
xelatex -interaction=nonstopmode main.tex
grep -E "^!|Missing character" main.log     # 必须为空
```

1. 从 `main` 拉分支，命名 `fix/...` 或 `content/...` 或 `design/...`
2. 改动后本地编两遍，确认无错误、无缺字
3. **目检受影响的页面**（`pdftoppm -png -r 100 main.pdf qa/p` 渲染后逐页看）：
   无溢出、无图文重叠、页眉颜色正确
4. 若改了课程结构，核对三项对账数：课程卡片 35、曲目徽章 11、书签 35
5. 提交 PR，说明改了什么、为什么；CI 会自动编译检查，红了先修再请求 review

## 图片贡献

- **矢量图优先**：新图请用 TikZ 按现有组件风格绘制（墨灰主线 + 当前阶段色强调 +
  Stealth 箭头 + footnotesize 无衬线标签），包进 `fignote` 环境
- **AI 插画**：生成通道的密钥在维护者本地，贡献者无法直接跑 `gen_guitar_ai.py`。
  两个选择：① 提 Issue 描述需求，由维护者生成；② 用自己的生图通道，
  严格遵守 [`docs/ai-prompts.md`](./docs/ai-prompts.md) 里的风格合同（配色锁定、图内无文字、无边框）
- 不接受来源不明的照片；外部图片必须自带可商用授权且在 PR 里注明来源

## 许可

提交贡献即表示你同意：对排版工程的贡献按 MIT 发布，对课程内容的贡献按 CC BY-NC 4.0 发布
（见 [LICENSE](./LICENSE) 与 [LICENSE-CONTENT.md](./LICENSE-CONTENT.md)）。
