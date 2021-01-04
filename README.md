# Text_Recognizing_Module_Alpha
Text_Recognizing_Module_Alpha

所需环境：cuda10.2, python>=3.6, Ubuntu18.04.

先装detectron2，是Facebook的一个开源包。
First install Detectron2 from a local clone:

git clone https://github.com/facebookresearch/detectron2.git
sudo python -m pip install -e detectron2

然后需要setup一下，可能有一些默认路径的设置。不做这一步会出现有的函数导不进demo。

git clone https://github.com/MingBusinessman/Text_Recognizing_Module_Alpha.git
cd Text_Recognizing_Module_Alpha
sudo python setup.py build develop

在main.py文件里设置了视频路径的接口，到时候只要把变量设置成视频路径就可以了。

快速开始的话，把想要测试的视频放在根目录下，把视频名字改成“test2”或者近main.py里把变量名改了，都可以。然后cmd里python main.py理论上即可运行。
