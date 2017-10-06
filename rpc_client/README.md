## 客户端说明
### 1.运行环境
python 3.x

### 2.依赖库安装
```angular2html
pip install pika
```
### 3.配置说明
```angular2html
根据注释填写即可
```
### 4.运行程序
```angular2html
进入bin目录后
python start.py
```
## 5.使用说明
#### 5.1执行命令(多个IP用空格隔开)
```angular2html
>>run "ping -c 5 8.8.8.8" --hosts 10.135.115.186
TaskID:93677
Command execution successful. Please use check_task 'id' to see the result！
```
#### 5.2查看命令结果
```angular2html
>>check_task 93677

[ServerIP:10.135.115.186] 

 PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=41 time=22.5 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=41 time=22.6 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=41 time=22.6 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=41 time=22.5 ms
64 bytes from 8.8.8.8: icmp_seq=5 ttl=41 time=22.5 ms

--- 8.8.8.8 ping statistics ---
5 packets transmitted, 5 received, 0% packet loss, time 4006ms
rtt min/avg/max/mdev = 22.584/22.601/22.622/0.015 ms

Print Done
```
#### 5.3查看已执行过的命令对应的任务ID(只保留50条记录，可通过settings.py进行设置)
```angular2html
>>check_all
SN:0 TaskID:73367 Command:ping -n 20 127.0.0.1
SN:1 TaskID:86326 Command:dir
SN:2 TaskID:65099 Command:dir
SN:3 TaskID:84036 Command:ls
...
Print Done
```

### 5.其它
```angular2html
1.此程序支持多台Server
2.支持命令异步执行
3.通过配置文件可设置历史记录条数
```