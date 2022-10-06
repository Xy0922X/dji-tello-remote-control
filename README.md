项目名称
大疆Tello无人机的远程5G操控及视频回传。目前现有的无人机的操控都是在无人机的WiFi的范围内进行操控的，本项目的使用场景为无论与无人机相隔多远，PC都可远程根据视频控制无人机的飞行。

上手指南
以下指南将帮助你在本地机器上安装和运行该项目，进行开发和测试。关于如何将该项目部署到在线环境，请参考部署小节。

安装要求
本实验使用到的软件有Pycharm、Xshel(可以直接官网安装，安装步骤这里就省略了)，另外需要租用一个云服务器(阿里云、华为云都可以)，使用语言为python。硬件需要一个5G移动路由器，用来给连接无人机的PC1提供有线网络来与远程控制PC2进行通信。

项目目的及思路
因为tello无人机的操控距离有限，这样我们就无法完成远距离操控，本项目就是解决这个问题。首先有一台能连接无人机的(PC1)，还需要一台实际操控(PC2)，首先完成PC1与PC2的通信，PC2发送指令PC1接收然后操控无人机飞行，与此同时PC1获取无人机的视频图像与电量信息再回传给PC2，这样我们就可以实现可视化的远程操控了。


项目步骤
首先要解决PC1与PC2的通信，这里选取的是socket通信，当PC1，PC2处于局域网是，可以直接通信，但两台设备处于不同局域网时，由于PC1和PC2是两个私网IP，无法直接进行通信，所以我们需要一个云服务器作为中转，就可以实现socket通信了。租用服务器的步骤这里就不详细介绍了，配置方法如下：
1)设置云服务器端口


设置你需要的端口，源：0.0.0.0/0，保存。
2)云服务器linux系统配置frps端
在PC1上打开xshell软件，点击左上角文件，新建窗口，名称为云服务器的公网IP，然后点确定。

连接之后进入linux系统，mkdir xy（xy可随易改变，目的为了方便查找）
(1)下载frp，命令为：
wget https://github.com/fatedier/frp/releases/download/v0.34.1/frp_0.34.1_linux_amd64.tar.gz  
注意事项：提前查清楚你所购买的阿里云服务器是什么系统，什么架构的，几位的操作系统。查清楚以后再下载相应的frp版本。以我的为例，我的是Linux Ubuntu18.04 64位的操作系统。所以要选frp_0.34.1_linux_amd64.tar.gz(0.34.1版本可不同)
(2)解压
命令为：tar xzvf frp_0.34.1_linux_amd64.tar.gz
解压完以后会有名为frp_0.34.1_linux_amd64的文件夹，由于经常用到这个文件夹，给它重命名为一个简单的名字frp，命令为：mv frp_0.34.1_linux_amd64 frp，打开frp命令为：cd frp，查看frps.ini配置文件命令为cat frps.ini。

这里默认为7000端口，如果你再上一步设置的是其他端口，请保持一致，修改命令如下：
vim frps.ini，修改好了之后运行frps，命令为：./frps -c ./frps.ini，如果看到frps tcp listen on 0.0.0.0:7000；Start frps success代表开启成功。
(3)在PC1上配置frpc
我的PC1是windows系统，操作步骤为A，如果你的系统是linux系统，操作步骤为B
A：首先下载frp，地址如下https://github.com/fatedier/frp/releases；
   解压之后用记事本打开frpc.ini，并配置；

启动frpc服务(shift+右键点击在此处打开Powershell窗口，使用命令：./frpc.exe)


B:与云服务器配置类似，
首先下载frp，保证云服务器与PC1的版本是一致的；
解压；
修改frpc.ini配置与A中的一致，命令为：vim frpc.ini
启动frpc服务,命令为：./frpc -c ./frpc.ini

至此，我们已经配置好云服务器与PC1的连接，也实现了PC1与PC2的通信。

运行程序
先打开PC1的WiFi与Tello无人机相连，然后启动PC1_control代码，再在PC2上运行PC2_remote_image即刻看到无人机的视频，再运行PC2_remote_control代码，在运行窗口输入指令即可控制无人机飞行。

贡献者
https://blog.csdn.net/weixin_41735859/article/details/118160856
https://blog.csdn.net/m0_46445041/article/details/109387129?ops_request_misc=&request_id=&biz_id=102&utm_term=socket%E5%B1%80%E5%9F%9F%E7%BD%91%E4%B8%8E%E5%B1%80%E5%9F%9F%E7%BD%91%E9%80%9A%E4%BF%A1&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduweb~default-0-109387129.142^v50^control,201^v3^add_ask&spm=1018.2226.3001.4187








