# AGENTS.md — SimpleSnake

给 AI 编码助手（Antigravity、Claude Code、Codex 等）的项目说明。动手前先读这份文件。

## 这是什么项目

单文件 **pygame** 贪吃蛇游戏：深色主题、渐变蛇身 + 动态眼睛、发光食物、计分面板、Game Over 重开界面。
用 **PyInstaller** 打包，GitHub Actions 构建 Windows `.exe` 与 macOS `.app`/`.dmg` 并发布 prerelease。

- 目标平台：**Windows / macOS**（Linux 构建已刻意移除，不要加回来）
- 运行环境：Python 3.6+、pygame 2.0+

## 目录结构

| 路径 | 说明 |
|---|---|
| `snake.py` | 全部游戏逻辑（约 180 行，单文件） |
| `requirements.txt` | `pygame>=2.0.0`、`pyinstaller>=5.0.0` |
| `SimpleSnake.spec` | PyInstaller 配置（pygame 隐藏导入等） |
| `build/icon.ico`、`build/icon.icns`、`build/icon.png`、`build/gen_icon.py` | 图标资源与生成脚本，**CI 依赖，别删** |
| `build/build-macos.sh` | macOS 本地打包脚本 |
| `demo.png` | README 截图（游戏运行时不会加载它；CI 打包时会被带进产物） |
| `dist/` | 本地构建产物 → 不提交 |
| `build/SimpleSnake/` | PyInstaller 中间产物 → 不提交 |
| `README.md`、`QUICKSTART.md`、`BUILD_GUIDE.md`、`BUGFIXES.md`、`BUILD_FIXES.md` | 文档，含历史构建问题记录 |

## 常用命令

```bash
pip install -r requirements.txt
python snake.py                                  # 运行游戏

# 本地打包（Windows）
pyinstaller --onefile --name SimpleSnake --add-data "demo.png;." snake.py

# 本地打包（macOS）
bash build/build-macos.sh
```

CI 使用 Python 3.11；也可以用 `pyinstaller SimpleSnake.spec` 构建。

## 硬性规则

1. **游戏保持单文件** `snake.py`：除非明确要求，不要拆模块、不要新增运行时资源文件。
2. **操作方式是对外契约**，改了必须同步 README：方向键／WASD 移动，Game Over 后 `R` 重开、`Q` 退出。
3. **不要提交构建产物**：`dist/`、`build/SimpleSnake/`、`__pycache__/`、`.DS_Store`（已写进 `.gitignore`）。
4. `build/` 下的图标文件是 CI 依赖，**不要整个目录清理**。
5. 不要加回 Linux 构建（历史上的 AppImage 方案问题多，已移除）。
6. 文档与实现保持一致：改了玩法、按键或构建方式，就顺手更新 README / BUILD_GUIDE。

## 发布流程（CI）

`.github/workflows/build.yml`：

- 手动触发：Actions → **Build and Release** → Run workflow（`version` 输入目前**没有被使用**）；或推送 `v*` tag。
- 产物：Windows `SimpleSnake-Windows-Alpha.exe`、macOS `SimpleSnake-macOS-Alpha.dmg`。
- ⚠ 发布步骤把 release tag **写死为 `vAlpha`**（prerelease）。所以推 `v1.0.0` 这类 tag 也只会更新 `vAlpha` 这个 release；要发正式版本，先改 workflow 里的 tag/release 命名。
- macOS 应用未签名：首次打开需要右键 → 打开。

## 验收标准

- `python snake.py` 能正常游玩；
- 改动了打包相关文件时，本地至少把对应的 PyInstaller 命令跑通一次；
- `git status` 没有构建产物混入。

## 维护

改了玩法或构建流程后，顺手更新这份文件（和 README），保持与实际一致。
