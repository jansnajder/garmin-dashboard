# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

datas, binaries, hiddenimports = [], [], []

# uvicorn imports loops/protocols/lifespan by string -> collect them all
hiddenimports += collect_submodules("uvicorn")

# garminconnect -> curl_cffi native _wrapper.pyd + libcurl DLL
cc_datas, cc_binaries, cc_hidden = collect_all("curl_cffi")
datas += cc_datas
binaries += cc_binaries
hiddenimports += cc_hidden

# curl_cffi resolves its CA bundle via certifi.where()
datas += collect_data_files("certifi")

# frontend is served BY FastAPI -> bundle it into the backend build
datas += [("../frontend", "frontend")]

a = Analysis(
    ["run_server.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="backend",
    console=True,  # keep console during bring-up; flip to False for final installer
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,  # UPX corrupts DLLs
    name="backend",
)
