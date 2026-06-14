# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect all pygame data files and submodules
datas = []
hiddenimports = [
    'pygame',
    'pygame.constants',
    'pygame.display',
    'pygame.draw',
    'pygame.event',
    'pygame.font',
    'pygame.image',
    'pygame.key',
    'pygame.mouse',
    'pygame.mixer',
    'pygame.mixer.music',
    'pygame.time',
    'pygame.transform',
    'pygame.version',
    'pygame.surface',
    'pygame.rect',
    'pygame.color',
    'pygame.bufferproxy',
    'pygame.math',
]

# Collect all pygame modules
try:
    pygame_submodules = collect_submodules('pygame')
    hiddenimports.extend(pygame_submodules)
except:
    pass

a = Analysis(
    ['snake.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SimpleSnake',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SimpleSnake',
)

app = BUNDLE(
    coll,
    name='SimpleSnake.app',
    icon='build/icon.icns',
    bundle_identifier='com.simplesnake.app',
)
