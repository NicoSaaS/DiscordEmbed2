# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# For Windows version info
def get_version_info():
    import PyInstaller.utils.win32.versioninfo as vi
    return vi.VSVersionInfo(
        ffi=vi.FixedFileInfo(
            filevers=(2, 0, 2, 0),
            prodvers=(2, 0, 2, 0),
            mask=0x3F,
            flags=0x0,
            OS=0x40004,
            fileType=0x1,
            subtype=0x0,
            date=(0, 0)
        ),
        kids=[
            vi.StringFileInfo(
                [
                    vi.StringTable(
                        '040904B0',
                        [
                            vi.StringStruct('CompanyName', 'Nico Inc.'),
                            vi.StringStruct('FileDescription', 'DiscordEmbed2 - Webhook Message Tool'),
                            vi.StringStruct('FileVersion', '2.0.2.0'),
                            vi.StringStruct('InternalName', 'DiscordEmbed2'),
                            vi.StringStruct('LegalCopyright', 'Copyright © 2025 Nico Prang'),
                            vi.StringStruct('OriginalFilename', 'DiscordEmbed2.exe'),
                            vi.StringStruct('ProductName', 'DiscordEmbed2'),
                            vi.StringStruct('ProductVersion', '2.0.2.0')
                        ]
                    )
                ]
            ),
            vi.VarFileInfo([vi.VarStruct('Translation', [1033, 1200])])
    ])

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('imgs', 'imgs')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DiscordEmbed2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=None,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version_info=get_version_info(),
    onefile=True
)