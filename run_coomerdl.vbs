Set shell = CreateObject("WScript.Shell")

shell.Run "cmd.exe /c python ""C:\Users\Administrator\Desktop\Packet\CoomerDL-main\cookie1.py""", 0, True

shell.CurrentDirectory = "C:\Users\Administrator\Desktop\Packet\CoomerDL-main\CoomerDL-latest"
shell.Run "cmd.exe /c python main.py", 0, False