# Changelog

本文件记录 Dusk Star Theme 的重要变更。

## [Unreleased]

### Added

- 为暗色、亮色主题和图标主题补充 `$schema`，便于编辑器校验配置。

### Fixed

- 删除无效颜色键 `editorGuide.background`。
- 删除无效颜色键 `gitDecoration.stageAddedResourceForeground`。
- 将废弃的 `editorIndentGuide.background` / `editorIndentGuide.activeBackground` 迁移为 `editorIndentGuide.background1` / `editorIndentGuide.activeBackground1`。
- 修正 `package.json` 中失效的 `homepage` 链接。
- 将 `engines.vscode` 提升到 `^1.81.0`，与 `package-lock.json` 保持一致。
- 修复文件夹图标 SVG 因根节点变换而完全透明的问题。
- 移除图标主题中的空文件图标定义和 `file` 关联，图标主题只保留文件夹图标。
- 为亮色主题新增独立的高对比度文件夹图标。

### Changed

- 将 `UPLOG.md` 迁移为标准 `CHANGELOG.md`。
- 图标主题不再隐藏资源管理器展开箭头。
- README 补充文件夹图标主题说明和图标来源。

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
