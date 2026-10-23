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
- [x] 为亮色主题制作独立的高对比度箭头图标，并加大开合颜色差异
- [x] 统一明暗主题的箭头色系：关闭青绿、展开蓝色，暗色加深、亮色再次提亮
- [x] 移除亮色选中文件的高亮焦点描边
- [x] 保留 `hidesExplorerArrows: true`，由箭头样式文件夹图标承担开合指示
- [x] 在 README 中补充图标主题说明（文字说明，截图待补）
- [x] 保留原有三角形箭头样式，仅调整亮色版本配色
- [x] 确认原 SVG 的根节点 `transform` 在 Chromium/VS Code 中可正常渲染


## 3. 可读性

- [x] 调整亮色行号、注释、类名、字符串、常量的对比度
- [x] 修复亮色活动栏徽章白字对比度不足
- [x] 调整亮色侧栏输入框焦点高亮颜色
- [x] 将亮色 Git ignored 文件状态调淡为中性灰
- [x] 修复暗色 ignored Git 状态几乎不可见的问题
- [x] 修复暗色当前行号比普通行号更难读的问题
- [x] 复核按钮、调试状态栏、关键字等低对比度文字
- [x] 提升暗色注释、关键字、按钮和调试状态栏的对比度

## 4. 语义高亮与 UI 覆盖

- [x] 开启 `semanticHighlighting`，补充 `semanticTokenColors`（亮色、暗色已完成）
- [x] 补充接口、枚举、属性、对象键、Markdown、diff 等 token scope（亮色、暗色已完成）
- [x] 收窄 `meta.function-call` 的染色范围（亮色、暗色已完成）
- [x] 补充高频 UI 颜色：panel、terminal、diffEditor、suggest/hover、notification、quickInput、dropdown、bracket 等（亮色已完成；暗色待处理）

## 5. 状态色与高亮语义

- [x] 区分 Git added / modified / deleted 的颜色（亮色已完成；暗色待处理）
- [x] 让亮色选区比“其他匹配项”更明显
- [x] 给 find match 使用区别于普通选区的颜色（亮色已完成；暗色待处理）
- [x] 移除会触发 VS Code 颜色校验警告的不透明高亮背景色，回退到默认值
- [x] 将亮色代码单词高亮改为蓝色系并增加描边
- [x] 移除亮色文件标签选中边框、焦点虚线和代码高亮选择的边框
- [x] 梳理绿色语义，避免字符串、类名、常量、徽章、高亮同时使用绿色（亮色保留类名绿色，常量与徽章已改色；暗色待处理）

## 6. 工程化与文档

- [ ] 增加 `@vscode/vsce` 依赖和 `package` / `publish` 脚本
- [ ] 增加 `.vscodeignore`、`.gitignore`
- [ ] 增加 JSON、颜色 ID、对比度校验脚本和 CI
- [ ] 更新 README：安装、主题列表、图标主题、配色表、许可证
- [ ] 重拍过期的亮色/暗色截图，并补充 `alt` 文本
- [ ] 清理未使用的 `imgs/PixPin_2024-05-24_09-45-54.png`
- [ ] 补充 SVG 图标来源与许可说明（原始 SVG 来源/许可待确认）
- [ ] 整理 package 元数据：keywords、description、publisher、bugs 等
