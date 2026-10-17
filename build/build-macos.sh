#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP_NAME="SimpleSnake"
VERSION="Alpha"
DIST_DIR="$ROOT/dist"

echo "==> Building macOS .app with PyInstaller..."
cd "$ROOT"

pyinstaller --onefile --windowed \
  --name "$APP_NAME" \
  --osx-bundle-identifier com.simplesnake.app \
  --icon "$ROOT/build/icon.icns" \
  --add-data "$ROOT/demo.png:." \
  --distpath "$DIST_DIR" \
  "$ROOT/snake.py" 2>&1 || true

echo "==> Creating .app bundle manually..."
# PyInstaller --onefile --windowed produces a Unix executable for macOS.
# We need to wrap it in a proper .app bundle manually.

APP_BUNDLE="$DIST_DIR/$APP_NAME.app"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Copy the executable
cp "$DIST_DIR/$APP_NAME" "$APP_BUNDLE/Contents/MacOS/$APP_NAME"

# Create Info.plist
cat > "$APP_BUNDLE/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>$APP_NAME</string>
    <key>CFBundleIdentifier</key>
    <string>com.simplesnake.app</string>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundleVersion</key>
    <string>$VERSION</string>
    <key>CFBundleShortVersionString</key>
    <string>$VERSION</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

# Copy icon if exists
if [ -f "$ROOT/build/icon.icns" ]; then
  cp "$ROOT/build/icon.icns" "$APP_BUNDLE/Contents/Resources/icon.icns"
fi

chmod +x "$APP_BUNDLE/Contents/MacOS/$APP_NAME"
echo "  -> Created: $APP_BUNDLE"

echo "==> Creating .dmg..."
DMG_PATH="$DIST_DIR/${APP_NAME}-macOS-${VERSION}.dmg"
rm -f "$DMG_PATH"

hdiutil create -srcfolder "$APP_BUNDLE" \
  -volname "$APP_NAME" \
  -format UDZO \
  -ov \
  "$DMG_PATH" 2>&1

echo "  -> Created: $DMG_PATH"
echo "==> macOS build complete!"
