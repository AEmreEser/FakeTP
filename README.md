```  
  ______      _       _______  _____  
 |  ____|    | |     |__   __||  __ \ 
 | |__  __ _ | | __ ___ | |   | |__) |
 |  __|/ _` || |/ // _ \| |   |  ___/ 
 | |  | (_| ||   <|  __/| |   | |     
 |_|   \__,_||_|\_\\___||_|   |_|      by Emre Eser
```
FTP-like transfer application. Course project for cs408 Computer Networks @ Sabanci Uni.

**Check the *"gui"* branch for graphical user interface version**

### Commands List
- LIST: lists uploaded files
- UPLOAD \<filename>: uploading files
- DOWNLOAD \<owner> \<filename>: downloading files
- DELETE \<filename>: delete a file (if and only if it belongs to you)
- SHELL \<cmd>: Execute shell command. Only available if `--debug` parameter was passed

### Command Line Arguments (client and server)
- `--ip` : Ip of the server
- `--port` : Port of the server
- `--name` : Client only. Username of the client
- `--debug` : Enable debug mode
- `--maxconn` : Server only. Maximum number of connections allowed
- `--storage` : Server only. Path to server storage directory
- `--savepath` : Client only. Path to clients downloads directory

Try running with `--help` for more info

                                      
