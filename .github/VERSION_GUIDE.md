# 版本发布指南（SPlayer 风格 - 简化版）

## 核心规则

**简单明了：**

- ✅ 只有 `X.Y.Z`（纯数字）和 `X.Y.Z-stable` 是**正式版**
- ✅ 其他一律是**预发布版**（beta/alpha/canary/rc/nightly 等）
- ✅ Tag 和 Release 标题自动去除 `-stable` 和颜色，其他保持一致

## 快速开始

### 发布新版本只需修改 README.md 一处

```markdown
<!-- 正式版（推荐，纯数字） -->
<img src="https://img.shields.io/badge/version-2.0.4-blue"/>

<!-- 正式版（显式 stable，会自动去除） -->
<img src="https://img.shields.io/badge/version-2.0.4--stable-green"/>

<!-- Beta 版 -->
<img src="https://img.shields.io/badge/version-2.0.5--beta-orange"/>

<!-- Alpha 版 -->
<img src="https://img.shields.io/badge/version-2.0.5--alpha-red"/>

<!-- 金丝雀版 -->
<img src="https://img.shields.io/badge/version-2.0.6--canary-yellow"/>

<!-- RC 版 -->
<img src="https://img.shields.io/badge/version-2.0.6--rc1-purple"/>

<!-- 每日构建版 -->
<img src="https://img.shields.io/badge/version-2.0.6--nightly-gray"/>
```

**注意**：Shields.io 中 `-` 需要用 `--` 转义，所以 `2.0.4-beta` 写成 `2.0.4--beta`

## Badge 说明

### 版本 Badge（任意后缀支持）

- **格式**：`version-X.Y.Z-颜色` 或 `version-X.Y.Z--后缀-颜色`
- **颜色自选**（workflow 会自动去除）：
  - 正式版建议：`blue` / `green`
  - Beta 建议：`orange` / `yellow`
  - Alpha 建议：`red`
  - 其他自定义：`purple` / `gray` / `pink` 等

### 构建状态 Badge

使用 GitHub Actions 官方 badge（现在显示 "Build & Release"）：

```markdown
<img src="https://github.com/dullspear/CQUPT_Link/actions/workflows/release.yml/badge.svg"/>
```

## 发布流程

### 1. 修改版本号（README.md）

**正式版 2.0.4：**

```markdown
<img src="https://img.shields.io/badge/version-2.0.4-blue"/>
```

**金丝雀版 2.0.5：**

```markdown
<img src="https://img.shields.io/badge/version-2.0.5--canary-yellow"/>
```

### 2. 提交并推送

```bash
git add README.md
git commit -m "chore: bump version to 2.0.4"
git push origin main
```

## Changelog 格式（自动生成）

```
## What's Changed
--------------
- feat: add auto-login by @author (Dec 20, 08:30 AM GMT+0000)
- fix: network issue by @author (Dec 19, 03:20 PM GMT+0000)
- docs: update README by @author (Dec 18, 10:15 AM GMT+0000)
```

## 注意事项

1. ✅ **版本号只改一处**：README.md 的 badge URL
2. ✅ **自动去除 stable**：`2.0.4-stable` → `2.0.4`（Release 中）
3. ✅ **保留其他后缀**：`2.0.4-beta` / `2.0.4-canary` 等保持不变
4. ✅ **极简判断逻辑**：纯数字 = 正式版，其他 = 预发布版
5. ✅ **删除旧 Release**：同版本号会先删除旧的再创建新的
6. ✅ **时间格式标准**：`Dec 20, 08:30 AM GMT+0000`（Actions 运行在 UTC）
7. ✅ **Build & Release badge**：自动显示构建状态
8. ✅ **支持任意后缀**：未来添加新版本类型无需修改 workflow

## Release 规则

| README 版本号   | 提取后版本    | Release Tag    | Pre-release |
| --------------- | ------------- | -------------- | ----------- |
| `2.0.4`         | `2.0.4`       | `v2.0.4`       | ❌ false     |
| `2.0.4--stable` | `2.0.4`       | `v2.0.4`       | ❌ false     |
| `2.0.5--beta`   | `2.0.5-beta`  | `v2.0.5-beta`  | ✅ true      |
| `2.0.5--alpha`  | `2.0.5-alpha` | `v2.0.5-alpha` | ✅ true      |

**规则说明**：

- `-stable` 后缀会被自动移除（正式版不需要显式标注）
- `-beta`/`-alpha` 会保留并标记为 Pre-release