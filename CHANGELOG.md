# Changelog

本文件记录 Dusk Star Theme 的重要变更。

## [0.2.1] - 2026-10-24

### Added

- 为亮色主题增加 Git blame 行内注解颜色，降低其与正文的视觉竞争。
- 对亮色主题的 token 和 semantic token 增加对比度校验。

### Fixed

- 修正亮色查找高亮前景色的透明度配置。
- 提升亮色主题 Tag attribute 的对比度。

## [0.2.0] - 2026-10-23

### Added

- 增加主题 JSON、颜色 ID、透明度、对比度和包元数据校验脚本，并在 GitHub Actions 中运行。
- 增加 `@vscode/vsce` 开发依赖和 `validate` / `package` / `publish` npm 脚本。
- 增加 `.vscodeignore`、`.gitignore` 和 VSIX 打包 CI。
- 增加 `scripts/vscode-color-registry.json` 颜色 ID 注册表快照及生成脚本。
- 为暗色、亮色主题和图标主题补充 `$schema`，便于编辑器校验配置。
- 亮色主题开启语义高亮，补充接口、枚举、属性、对象键、类型参数和 Markdown 等 token scope。
- 暗色主题开启语义高亮，补充接口、枚举、属性、对象键、类型参数和 Markdown 等 token scope。
- 补充亮色主题的面板、终端、差异编辑器、建议/悬停、通知、快速输入、下拉框和括号等 UI 配色。
- 补充暗色主题的面板、终端、差异编辑器、建议/悬停、通知、快速输入、下拉框和括号等 UI 配色。
- 补充暗色主题的滚动条、面包屑、状态栏项、输入校验、调试控制台和快捷键标签等控件配色。
- 补充暗色主题的选区、查找匹配、Git 状态、minimap 和 overview ruler 配色。

### Fixed

- 删除无效颜色键 `editorGuide.background`。
- 删除无效颜色键 `gitDecoration.stageAddedResourceForeground`。
- 移除三处会触发 VS Code 颜色校验警告的不透明高亮背景色：暗色/亮色的 `editor.wordHighlightTextBackground`，以及亮色的 `editor.selectionHighlightBackground`。
- 移除暗色主题的文件标签选中边框、列表焦点虚线和选区/单词/范围高亮边框，并为 overview ruler 高亮使用透明色。
- 将暗色 `editor.findMatchHighlightForeground` 设为 90% 透明度，满足 VS Code 颜色 schema。
- 将暗色 Git blame 行内注解颜色调暗为 `#969BA3`，避免与正文混淆。
- 提升亮色主题中注释、字符串、类名、常量和行号的对比度。
- 提升暗色主题中注释、关键字、当前行号、Git 忽略文件、按钮和调试状态栏的对比度。
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

- 更新暗色/亮色主题截图，旧截图归档到 `imgs/archive/`，并从 VSIX 中排除。
- 重写 README，补充安装、主题、图标主题、配色表、定制、开发和许可证说明。
- 整理 package 元数据：description、keywords、galleryBanner、bugs、homepage。
- 将文件夹箭头 SVG 替换为项目原创、MIT 许可的图标，移除 SVG Repo 来源注释。
- 删除未使用的 `imgs/PixPin_2024-05-24_09-45-54.png`。
- 将 `UPLOG.md` 迁移为标准 `CHANGELOG.md`。
- 保留原有箭头样式文件夹图标，恢复隐藏资源管理器展开箭头。
- 统一明暗主题的箭头色系：关闭为青绿色，展开为蓝色；暗色箭头加深，亮色箭头按反馈再次提亮。
- README 补充文件夹图标主题说明。
- 亮色选区改为更明显的蓝色并设置选中文字前景色；查找匹配改用琥珀色，与其他高亮区分。
- 区分亮色 Git added/modified/deleted/renamed/conflicting 状态色。
- 梳理亮色绿色语义：类名保留绿色，常量改为紫色，活动栏徽章改为蓝色。
- 将暗色主题活动栏徽章由淡紫色调整为蓝色。
- 收窄亮色主题的函数调用染色范围，避免整个调用表达式被统一染色。
- 收窄暗色主题的函数调用染色范围，避免整个调用表达式被统一染色。
- 移除亮色主题的文件标签选中边框、焦点虚线和代码高亮选择的边框。
- 将暗色选区改为不透明蓝色并设置选中文字前景色；查找匹配改用琥珀色，与其他高亮区分。
- 区分暗色 Git added/modified/deleted/renamed/conflicting 状态色。
- 梳理暗色绿色语义：用户常量、枚举成员改为紫色，侧栏标题改为中性前景色，链接编辑高亮改用青色。
- 将暗色文件标签的 modified 状态改为橙色，并补充 minimap、overview ruler 的选区/查找/Git 标记。

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
