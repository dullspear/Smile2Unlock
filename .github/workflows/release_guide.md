# 版本发布指南

## 核心规则

- ✅ 纯数字 `X.Y.Z` 或 `X.Y.Z-stable` = **正式版**
- ✅ 其他后缀（beta/rc/alpha 等）= **预发布版**
- ✅ **自动转正**：发布新版本 beta 时，上一版本 beta 自动变正式版

## 快速开始

### 修改 README.md 版本号

```markdown
<!-- 正式版 -->
<img src="https://img.shields.io/badge/version-1.2.0-blue"/>

<!-- Beta 版 -->
<img src="https://img.shields.io/badge/version-1.2.0--beta-orange"/>

<!-- RC 版 -->
<img src="https://img.shields.io/badge/version-1.2.0--rc-purple"/>
```

**注意**：Shields.io 中 `-` 用 `--` 转义，如 `1.2.0-beta` 写成 `1.2.0--beta`

### 提交并推送

```bash
git add README.md
git commit -m "chore: bump version to 1.2.0-beta"
git push origin main
```

## 发布流程

### 场景 1：同版本多次调试（覆盖）
```markdown
<!-- 多次 push 都用这个，每次覆盖 v1.2.0-beta -->
<img src="https://img.shields.io/badge/version-1.2.0--beta-orange"/>
```

### 场景 2：新版本 beta（自动转正上一版本）
```markdown
<!-- 发布 v1.3.0-beta 时，自动把 v1.2.0-beta 转为 v1.2.0 正式版 -->
<img src="https://img.shields.io/badge/version-1.3.0--beta-orange"/>
```

### 场景 3：直接发正式版（手动）
```markdown
<!-- 不经过 beta，直接发正式版 -->
<img src="https://img.shields.io/badge/version-1.2.0-blue"/>
```

## 自动转正详解

**触发条件：**  
当前版本是预发布 + 版本号前缀变大（如 `1.2` → `1.3`）

**执行操作：**
1. 下载上一版本产物
2. 删除旧 tag/release（如 `v1.2.0-beta`）
3. 创建新正式版（如 `v1.2.0`）
4. 复用产物，继承 changelog

**失败保护：**  
产物下载失败 → 跳过转正，不影响当前版本发布

## 注意事项

1. ✅ **版本号只改一处**：README.md 的 badge
2. ✅ **自动去除 `-stable`**：正式版 tag 为 `vX.Y.Z`
3. ✅ **同版本覆盖**：相同版本号会重建 release
4. ✅ **完全自动**：无需手动操作，push 即可
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