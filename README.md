## AutoAtenConsoleUpgrade ![VERSION](https://img.shields.io/badge/Version-v1-green.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)

## 此程式可實現
  - 檢測韌體版本
  - 自動上傳韌體並更新
  - 配合 IP List 做動，並檢測是否更新成功

## Logs
   * ver 1.0
     - 開發中

## Useage
    #Init for Virtual Env 建立虛擬環境。
    virtualenv venv
    
    #Active Virtual Env 進入虛擬環境。
    source ./venv/bin/activate
    
    #Install Requirements 安裝所需要之套件。
    pip install -r requirements.txt
    
    #Use it 準備就緒，可以直接執行，看看結果再行調整。
    python ./main.py
    
    or （如果想要打包為單一執行檔，下面就是打包的指令。）
    pyinstaller -F ./main.py -n ./AutoAtenConsoleUpgrade -i ico.ico

    #運作結束後，離開虛擬環境。
    deactivate
