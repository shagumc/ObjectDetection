@echo off
echo ===============================
echo   Python 仮想環境セットアップ
echo ===============================
echo.

REM ---- Python 実行ファイルを確認 ----
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python が見つかりません。
    echo Python をインストールしてから再実行してください。
    pause
    exit /b
)

REM ---- .venv フォルダ作成 ----
echo [+] 仮想環境 .venv を作成します...
py -3.11 -m venv .venv

if not exist ".venv" (
    echo [ERROR] .venv の作成に失敗しました
    pause
    exit /b
)

echo [+] 仮想環境をアクティベートします...

REM ---- 仮想環境を有効化 ----
call .venv\Scripts\activate

echo [+] requirements.txt をインストールします...

REM ---- パッケージをインストール ----
python -m pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] パッケージのインストール中にエラーが発生しました。
    echo 仮想環境は作成されています。
    echo 手動で以下を実行してください:
    echo   call .venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b
)

pip install LabelImg

REM LabelImgはそのままではエラーが出てしまうので、上書きする
COPY Overwrite\labelImg.py .venv\Lib\site-packages\labelImg\
COPY Overwrite\canvas.py .venv\Lib\site-packages\libs\

REM GPU使う場合はインストール
REM pip install torch==2.9.0 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

echo.
echo ==========================================
echo   セットアップ完了
echo ------------------------------------------
echo   仮想環境が作成され、有効化されました。
echo   requirements.txt も正常にインストールされました。
echo ------------------------------------------
echo   次回以降の起動方法:
echo     call .venv\Scripts\activate
echo ==========================================

pause
