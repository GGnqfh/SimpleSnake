# 快速开始指南

## 🔧 立即执行（网络恢复后）

### 1. 推送代码到 GitHub

```bash
cd /Users/huang/Github-repos/SimpleSnake
git add .
git commit -m "Fix cross-platform build: Linux and macOS"
git push origin main
```

### 2. 触发构建

1. 打开 GitHub 仓库: https://github.com/GGnqfh/SimpleSnake
2. 点击 **Actions** 选项卡
3. 点击 **Build and Release** 工作流
4. 点击 **Run workflow** 按钮
5. 保持默认版本 "Alpha"
6. 点击 **Run workflow**

### 3. 等待构建完成

- ⏱️ 预计时间: 5-10 分钟
- 📍 位置: Actions 选项卡可以看到进度
- ✅ 成功标志: 所有任务显示 ✓

### 4. 检查结果

1. 进入 **Releases** 页面
2. 找到 **SimpleSnake Alpha Release**
3. 下载三个平台的安装包:
   - `SimpleSnake-Windows-Alpha.exe`
   - `SimpleSnake-macOS-Alpha.dmg`
   - `SimpleSnake-Linux-Alpha.AppImage`

## 📁 已修复的文件

### 核心修复
- ✅ `.github/workflows/build.yml` - 重写构建流程
- ✅ `requirements.txt` - 添加依赖管理
- ✅ `SimpleSnake.spec` - 优化 PyInstaller 配置

### 图标文件
- ✅ `build/icon.ico` - Windows 图标 (26KB)
- ✅ `build/icon.png` - Linux 图标 (6.2KB)
- ✅ `build/icon.icns` - macOS 图标 (94KB)
- ✅ `build/gen_icon.py` - 图标生成器

### 文档
- ✅ `BUILD_GUIDE.md` - 详细构建指南
- ✅ `BUILD_FIXES.md` - 修复总结文档

## 🎯 主要修复内容

### Linux
- 添加完整的 SDL2 系统依赖
- 改进 AppImage 创建流程
- 添加 AppRun 启动脚本
- 添加构建验证步骤

### macOS
- 修复 PyInstaller 图标问题
- 改进 .app bundle 结构
- 添加完整的 Info.plist
- 添加 DMG 验证

## 🧪 本地测试

如果想先在本地测试构建：

### macOS
```bash
cd /Users/huang/Github-repos/SimpleSnake
python3 -m pip install pygame pyinstaller
pyinstaller --onefile --windowed --name SimpleSnake --distpath dist snake.py
```

### Linux (需要 Ubuntu/Debian)
```bash
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
pip install pygame pyinstaller
pyinstaller --onefile --name SimpleSnake snake.py
```

### Windows (PowerShell)
```powershell
pip install pygame pyinstaller
pyinstaller --onefile --name SimpleSnake snake.py
```

## 📊 构建状态

| 平台 | 状态 | 预期输出 |
|------|------|----------|
| Windows | ✅ 就绪 | SimpleSnake-Windows-Alpha.exe |
| macOS | ✅ 就绪 | SimpleSnake-macOS-Alpha.dmg |
| Linux | ✅ 就绪 | SimpleSnake-Linux-Alpha.AppImage |
| Release | ✅ 就绪 | GitHub Releases 页面 |

## ❓ 常见问题

**Q: 构建失败了怎么办？**
A: 检查 Actions 日志，通常会有详细的错误信息。

**Q: 三个平台都需要构建吗？**
A: GitHub Actions 会自动在各自的 runner 上构建（Windows、macOS、Linux）。

**Q: 如何测试构建的文件？**
A: 
- Windows: 双击 .exe
- macOS: 打开 .dmg，拖动到 Applications
- Linux: `chmod +x *.AppImage && ./SimpleSnake-Linux-Alpha.AppImage`

**Q: 版本号在哪里设置？**
A: 工作流中 `default: 'Alpha'`，可以手动运行时修改。

---

**注意**: 由于网络问题，代码需要手动推送到 GitHub。修复文件已准备好，一旦网络恢复即可推送。
