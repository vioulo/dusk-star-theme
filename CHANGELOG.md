# Changelog

本文件记录 Dusk Star Theme 的重要变更。

## [Unreleased]

### Added

- 为暗色、亮色主题和图标主题补充 `$schema`，便于编辑器校验配置。

### Fixed

- 删除无效颜色键 `editorGuide.background`。
- 删除无效颜色键 `gitDecoration.stageAddedResourceForeground`。
- 移除三处会触发 VS Code 颜色校验警告的不透明高亮背景色：暗色/亮色的 `editor.wordHighlightTextBackground`，以及亮色的 `editor.selectionHighlightBackground`。
- 提升亮色主题中注释、字符串、类名、常量和行号的对比度。
- 提升亮色主题活动栏徽章、按钮、调试状态栏和 Git added/modified/renamed 状态色的对比度。
- 将亮色主题中 Git 忽略文件的状态色调淡为中性灰，避免与普通文件混淆。
- 将亮色主题的代码单词高亮改为蓝色系，并增加蓝色描边以突出显示。
- 调整亮色主题函数名、参数/类常量和 CodeLens 的颜色。
- 将亮色主题的输入框焦点边框调整为更暗的蓝色（`focusBorder`）。
- 将废弃的 `editorIndentGuide.background` / `editorIndentGuide.activeBackground` 迁移为 `editorIndentGuide.background1` / `editorIndentGuide.activeBackground1`。
- 修正 `package.json` 中失效的 `homepage` 链接。
- 将 `engines.vscode` 提升到 `^1.81.0`，与 `package-lock.json` 保持一致。
- 移除图标主题中的空文件图标定义和 `file` 关联，图标主题只保留文件夹图标。
- 为亮色主题新增独立的箭头样式文件夹图标。
- 移除亮色选中文件的高亮焦点描边。

### Changed

- 将 `UPLOG.md` 迁移为标准 `CHANGELOG.md`。
- 保留原有箭头样式文件夹图标，恢复隐藏资源管理器展开箭头。
- 统一明暗主题的箭头色系：关闭为青绿色，展开为蓝色；暗色箭头加深，亮色箭头按反馈再次提亮。
- README 补充文件夹图标主题说明。

## [0.1.2] - 2026-04-17

### Changed

- 调整选中字符高亮。
- 添加菜单边框。

## [0.1.1] - 2026-03-25

### Light

- 加深字符串绿色。
- 修改 editor words focus 颜色。
- 修改选中颜色。

### Dark

- 调整 active tab 的样式，保持和 Light 一致。

### Both

- 调整搜索高亮。
