# Version. 0.2.0
# 在linux下，背景執行指令
- 在指令的後面加上&的符號，就可以背景執行
```
$ your-command &
```
- 使用jobs可以看到目前背景執行的process，但是jobs列出來的process只有在這個session有效，session斷掉jobs就沒有東西了
- 這個背景執行在console關閉，session斷掉後，就會自動結束程序
- 想要中斷程序，可以使用kill指令，但前提是要知道PID
```
$ kill PID
```
- 想要session斷掉，還要繼續留在程序中執行，可以使用nohup
```
$ nohup your-command &
```
- nohup預設會把吐出的訊息紀錄在nohup.out檔案中
- nohup只有reboot會停止程序，不然始終會留在背景程序執行
- nohup當session斷掉重新連接後，jobs就會看不到，需要改利用lsof來找PID
```
$ lsof | grep nohup
```
- 要停止nohup的程序，一樣kill PID即可

# 在linux下，建立開機自動執行程序動作
- 建立scipt檔案放在/etc/init.d/路徑下
```
$ cd /etc/init.d
$ touch your-autoStartScript
```
- 撰寫指令執行的腳本，可參考AutoStartScript
```
$ vim your-autoStartScript
```
- 把腳本檔案權限，調整為可執行檔
```
$ sudo chmod 755 your-autoStartScript
```
- 註冊開機自動執行機制
```
$ sudo update-rc.d your-autoStartScript defaults 99
```
- 如果要移除開機自動執行動作
```
$ sudo update-rc.d your-autoStartScript remove
```
- 如果init.d裡面的script有修改的話，要執行以下指令
```
$ systemctl daemon-reload
```
- 可使用指令啟動、停止服務
```
$ sudo service your-autoStartScript start
$ sudo service your-autoStartScript stop
```
- 如果你的腳本是執行一個sh檔案，記得被執行的SH檔也要把檔案權限設定為755執行檔
- 重開機看有沒有效果
```
$ sudo reboot
```

# 安裝pyinstaller將python打包成執行檔
```
$ pip install pyinstaller
```
- 如果是在Raspberry等Linux環境，要用pip3去install pyinstaller，包出來才會跑python3的程式
- 打包執行檔
```
$ pyinstaller -F your-root-python.py
```

# 安裝flask，提供webAPI讓外界讀取溫度數據
```
$ pip install flask
```

# 同時讀取多組w1 interface的溫控模組
- 讀取一組w1 interface時，查看/boot/config.txt，會看到只有一行dtoverlay=w1-gpio
- 如果要支援多組，則要編輯這個檔案，修改為以下內容
```
dtoverlay=w1-gpio,gpiopin=4
dtoverlay=w1-gpio,gpiopin=17
```

# 開啟使用enc28j60網路模組
- 根據針腳對應圖連接到raspberrypi gpio後，編輯/boot/config.txt的檔案，在最後面加上以下內容，即可啟動enc28j60網路模組
```
dtoverlay=enc28j60
```

# 把溫度數值，顯示載OLED模組
- 首先要先到raspi-config開啟i2C介面
- 安裝i2c-tool，可以用來偵測連接到樹梅派上面的i2C裝置
```
$ sudo apt-get install i2c-tools
```
- i2cdetect -l 可以列舉連到樹梅派的裝置
- i2cdetect -y 1 則是顯示第一個裝置的記憶體位址
- 安裝第三方寫好的OLED驅動python套件由Adafruit公司開發開源的(pip)
```
$ pip3 install Adafruit-SSD1306
```
- 安裝python繪圖套件(pip)
```
$ pip3 install Pillow
```
- 如果出現Pillow: libopenjp2.so.7: cannot open shared object file: No such file or directory，就安裝libopenjp2-7試試看
```
$ sudo apt-get install libopenjp2-7
$ sudo apt-get install libtiff5
```
- 安裝RPi.GPIO
```
$ sudo apt-get install python3-rpi.gpio
```

# 換了Raspberrypi zero，裝OS Lite，有些python套件要自己裝
```
$ sudo apt-get install python3-tk
```