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