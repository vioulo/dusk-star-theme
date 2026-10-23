# Dusk Star Theme 修补计划（临时）

> 临时文档，用于跟踪主题审查后的修复项。全部完成或合并后可删除。

## 1. 发布阻断项（已完成）

- [x] 删除两个无效颜色键：`editorGuide.background`、`gitDecoration.stageAddedResourceForeground`
- [x] 为暗色、亮色主题和图标主题补充 `$schema`
- [x] 修复 `package.json` 中失效的 `homepage` 链接
- [x] 统一 `engines.vscode` 为 `^1.81.0`，与 `package-lock.json` 保持一致
- [x] 将 `UPLOG.md` 迁移为标准的 `CHANGELOG.md`，并补充本次修复记录

## 废弃颜色 ID（已完成，方案 A）

- [x] `editorIndentGuide.background` → `editorIndentGuide.background1`
- [x] `editorIndentGuide.activeBackground` → `editorIndentGuide.activeBackground1`
- [x] `engines.vscode` 提升到 `^1.81.0`，同步 `package-lock.json`

## 2. 图标主题（配置与图标已完成，截图待补）

- [x] 处理 `themes/file-icon.json` 中 `iconPath` 为空的问题：移除空文件图标定义，保留纯文件夹图标主题
- [x] 确认不提供文件图标，移除 `fileNames`、`fileExtensions`、`languageIds` 需求
- [x] 为亮色主题制作独立的高对比度文件夹图标
- [x] 设置 `hidesExplorerArrows: false`，恢复展开箭头
- [x] 在 README 中补充图标主题说明（文字说明，截图待补）
- [x] 修复文件夹 SVG 根节点 `transform` 导致图标完全透明的问题


## 3. 可读性

- [ ] 调整亮色行号、注释、类名、字符串、常量的对比度
- [ ] 修复亮色活动栏徽章白字对比度不足
- [ ] 修复暗色 ignored Git 状态几乎不可见的问题
- [ ] 修复暗色当前行号比普通行号更难读的问题
- [ ] 复核按钮、调试状态栏、关键字等低对比度文字

## 4. 语义高亮与 UI 覆盖

- [ ] 开启 `semanticHighlighting`，补充 `semanticTokenColors`
- [ ] 补充接口、枚举、属性、对象键、Markdown、diff 等 token scope
- [ ] 收窄 `meta.function-call` 的染色范围
- [ ] 补充高频 UI 颜色：panel、terminal、diffEditor、suggest/hover、notification、quickInput、dropdown、bracket 等

## 5. 状态色与高亮语义

- [ ] 区分 Git added / modified / deleted 的颜色
- [ ] 让亮色选区比“其他匹配项”更明显
- [ ] 给 find match 使用区别于普通选区的颜色
- [ ] 将 `editor.wordHighlightTextBackground` 改为半透明色
- [ ] 梳理绿色语义，避免字符串、类名、常量、徽章、高亮同时使用绿色

## 6. 工程化与文档

- [ ] 增加 `@vscode/vsce` 依赖和 `package` / `publish` 脚本
- [ ] 增加 `.vscodeignore`、`.gitignore`
- [ ] 增加 JSON、颜色 ID、对比度校验脚本和 CI
- [ ] 更新 README：安装、主题列表、图标主题、配色表、许可证
- [ ] 重拍过期的亮色/暗色截图，并补充 `alt` 文本
- [ ] 清理未使用的 `imgs/PixPin_2024-05-24_09-45-54.png`
- [x] 补充 SVG 图标来源与许可说明
- [ ] 整理 package 元数据：keywords、description、publisher、bugs 等
