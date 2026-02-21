# 版本发布指南

## 核心规则

- ✅ 纯数字 `X.Y.Z` 或 `X.Y.Z-stable` = **正式版**
- ✅ 其他后缀（beta/rc/alpha 等）= **预发布版**
- ✅ **自动转正**：预发布版本自动转为正式版
  - 发布新版本预发布 → 转正上一版本预发布
  - 直接发布正式版 → 转正同版本预发布

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

### 场景 2：新版本预发布（自动转正上一版本）
```markdown
<!-- 发布 v1.3.0-beta 时，自动把 v1.2.0-beta 转为 v1.2.0 正式版 -->
<img src="https://img.shields.io/badge/version-1.3.0--beta-orange"/>
```

### 场景 3：直接发正式版（自动转正同版本）
```markdown
<!-- 发布 v1.2.0 正式版，自动删除并转正 v1.2.0-beta -->
<img src="https://img.shields.io/badge/version-1.2.0-blue"/>
```

## 自动转正机制

### 触发条件

| 当前发布         | 触发条件               | 自动转正操作                              |
| ---------------- | ---------------------- | ----------------------------------------- |
| 预发布版 (beta)  | 版本号前缀变大         | 上一版本预发布 → 正式版                   |
| 正式版           | 存在同版本预发布       | 同版本预发布 → 删除（已经是正式版了）     |

### 执行流程

**预发布触发转正**（版本号变大，如 `1.2` → `1.3`）
1. 下载上一版本预发布产物（如 `v1.2.0-beta`）
2. 删除上一版本预发布 tag/release
3. 创建新正式版（如 `v1.2.0`），复用产物
4. 发布当前新预发布版（如 `v1.3.0-beta`）

**正式版触发清理**（直接发布正式版）
1. 查找同版本所有预发布（如 `v1.2.0-beta`, `v1.2.0-alpha`）
2. 删除这些预发布 tag/release（正式版已存在，无需转正）
3. 发布当前正式版（如 `v1.2.0`）

### 示例

```
时间线：
1. 发布 v1.0.0-beta → 无操作
2. 发布 v1.1.0-beta → 自动转正 v1.0.0-beta 为 v1.0.0
3. 发布 v1.1.0     → 删除 v1.1.0-beta
```

**失败保护：** 产物下载失败 → 跳过转正，不影响当前版本发布

## Changelog 生成

✅ **使用 GitHub 自动生成**：所有 Release 的 What's Changed 由 GitHub 自动生成，基于：
- Pull Requests
- Commit messages
- Contributors

✅ **优势**：
- 自动关联 PR 和 Issue
- 自动识别贡献者
- 格式统一，内容清晰
- 无重复内容

## 注意事项

1. ✅ **版本号只改一处**：README.md 的 badge
2. ✅ **自动去除 `-stable`**：正式版 tag 为 `vX.Y.Z`
3. ✅ **同版本覆盖**：相同版本号会重建 release
4. ✅ **完全自动**：无需手动操作，push 即可
5. ✅ **智能转正**：预发布自动转正式版，无残留
6. ✅ **GitHub Changelog**：统一使用 GitHub 自动生成
7. ✅ **Build & Release badge**：自动显示构建状态
8. ✅ **支持任意后缀**：未来添加新版本类型无需修改 workflow

## Release 规则

| README 版本号   | 提取后版本    | Release Tag    | Pre-release | 自动转正操作                                |
| --------------- | ------------- | -------------- | ----------- | ------------------------------------------- |
| `2.0.4`         | `2.0.4`       | `v2.0.4`       | ❌ false     | 删除 `v2.0.4-*` 所有预发布版本              |
| `2.0.4--stable` | `2.0.4`       | `v2.0.4`       | ❌ false     | 删除 `v2.0.4-*` 所有预发布版本              |
| `2.0.5--beta`   | `2.0.5-beta`  | `v2.0.5-beta`  | ✅ true      | 如果 `2.0.5 > 2.0.4`，转正 `v2.0.4-beta`   |
| `2.0.5--alpha`  | `2.0.5-alpha` | `v2.0.5-alpha` | ✅ true      | 如果 `2.0.5 > 2.0.4`，转正上一预发布版本    |

**规则说明**：

- `-stable` 后缀会被自动移除（正式版不需要显式标注）
- `-beta`/`-alpha` 会保留并标记为 Pre-release
- **自动转正**：预发布版本在适当时机自动转为正式版
  - 正式版发布 → 删除同版本预发布
  - 新预发布发布 → 转正上一预发布