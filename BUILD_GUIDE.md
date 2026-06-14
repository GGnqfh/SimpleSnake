# SimpleSnake Build Guide

## 项目概述

这是一个使用 Pygame 编写的经典贪吃蛇游戏，支持跨平台构建。

## 支持的平台

| 平台 | 格式 | 文件命名 |
|------|------|----------|
| Windows | 64位可执行文件 | `SimpleSnake-Windows-Alpha.exe` |
| macOS | 磁盘镜像 | `SimpleSnake-macOS-Alpha.dmg` |
| Linux | AppImage | `SimpleSnake-Linux-Alpha.AppImage` |

## 版本信息

所有平台的版本号统一设置为 **Alpha**

## 本地构建指南

### macOS 构建

**要求:**
- macOS 10.15+
- Python 3.9+
- pygame
- pyinstaller

```bash
# 安装依赖
pip install pygame pyinstaller

# 使用 PyInstaller 构建
pyinstaller --onefile --windowed \
  --name SimpleSnake \
  --osx-bundle-identifier com.simplesnake.app \
  --icon build/icon.icns \
  --distpath dist \
  snake.py

# 验证构建
file dist/SimpleSnake.app/Contents/MacOS/SimpleSnake

# 创建 DMG
hdiutil create -srcfolder "dist/SimpleSnake.app" \
  -volname "SimpleSnake" \
  -format UDZO \
  -ov "dist/SimpleSnake-macOS-Alpha.dmg"
```

### Windows 构建

**要求:**
- Windows 10+
- Python 3.9+
- pygame
- pyinstaller

```powershell
# 安装依赖
pip install pygame pyinstaller

# 构建可执行文件
pyinstaller --onefile \
  --name SimpleSnake \
  --icon build/icon.ico \
  --distpath dist \
  snake.py
```

### Linux 构建

**要求:**
- Ubuntu/Debian 或其他 Linux 发行版
- Python 3.9+
- pygame
- pyinstaller
- AppImageTool

```bash
# 安装系统依赖
sudo apt-get update
sudo apt-get install -y libsdl2-dev libsdl2-image-dev \
  libsdl2-mixer-dev libsdl2-ttf-dev python3-dev

# 安装 Python 依赖
pip install pygame pyinstaller

# 构建可执行文件
pyinstaller --onefile \
  --name SimpleSnake \
  --distpath dist \
  snake.py

# 创建 AppImage 目录结构
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

cp dist/SimpleSnake AppDir/usr/bin/

cat > AppDir/usr/share/applications/simplesnake.desktop << EOF
[Desktop Entry]
Name=SimpleSnake
Comment=Snake game built with Pygame
Exec=SimpleSnake
Icon=simplesnake
Terminal=false
Type=Application
Categories=Game;
EOF

# 下载 AppImageTool 并构建
wget -q -O appimagetool \
  https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool
./appimagetool AppDir dist/SimpleSnake-Linux-Alpha.AppImage
```

## GitHub Actions 自动构建

项目已配置 GitHub Actions 工作流，支持自动构建和发布。

### 触发方式

1. **手动触发**: 在 GitHub 仓库的 Actions 页面选择 "Build and Release" 工作流，点击 "Run workflow"

2. **标签触发**: 推送 `v*` 格式的标签自动触发构建

### 工作流流程

```
┌─────────────────────────────────────────────────────────────┐
│                    Build and Release                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ build-windows│  │ build-linux │  │ build-macos │        │
│  │ (Windows)   │  │ (Ubuntu)    │  │ (macOS)     │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          ▼                                  │
│                   ┌───────────┐                             │
│                   │  release  │                             │
│                   │ (上传到   │                             │
│                   │  GitHub   │                             │
│                   │  Releases)│                             │
│                   └───────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

### 输出文件

- **Windows**: `SimpleSnake.exe` → 重命名为 `SimpleSnake-Windows-Alpha.exe`
- **macOS**: `SimpleSnake-macOS-Alpha.dmg`
- **Linux**: `SimpleSnake-Linux-Alpha.AppImage`

## 文件完整性验证

每个发布版本建议验证文件完整性：

```bash
# macOS
md5 dist/SimpleSnake-macOS-Alpha.dmg

# Linux (使用 sha256)
sha256sum dist/SimpleSnake-Linux-Alpha.AppImage

# Windows (PowerShell)
Get-FileHash dist/SimpleSnake-Windows-Alpha.exe -Algorithm MD5
```

## 运行说明

### macOS
1. 打开 `.dmg` 文件
2. 将 `SimpleSnake.app` 拖拽到 Applications 文件夹
3. 右键点击应用选择 "Open"（首次运行需要）

### Windows
1. 下载 `.exe` 文件
2. 双击运行即可

### Linux
1. 下载 `.AppImage` 文件
2. 赋予执行权限: `chmod +x SimpleSnake-Linux-Alpha.AppImage`
3. 双击或命令行运行

## 项目结构

```
SimpleSnake/
├── .github/workflows/
│   └── build.yml          # GitHub Actions 配置
├── build/
│   ├── icon.icns          # macOS 图标
│   ├── icon.ico           # Windows 图标
│   └── build-macos.sh     # macOS 构建脚本
├── dist/                  # 构建输出目录
├── snake.py               # 游戏主代码
├── SimpleSnake.spec       # PyInstaller 配置
└── README.md              # 项目说明
```

## 故障排除

### macOS 权限问题

如果遇到 "无法打开，因为无法验证开发者" 的错误：

1. 打开 "系统设置" → "隐私与安全性"
2. 在 "安全性" 部分找到被阻止的应用
3. 点击 "仍要打开"

### Linux SDL 错误

如果运行时遇到 SDL 相关错误：

```bash
# 安装缺失的库
sudo apt-get install libsdl2-2.0-0 libsdl2-image-2.0-0 \
  libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0
```

### Windows 图标问题

确保安装了 pywin32：

```powershell
pip install pywin32
```

## 许可证

MIT License - 详见 LICENSE 文件