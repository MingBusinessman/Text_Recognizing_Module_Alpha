import json
import sys

#
#
# test = {'time': 'content'}
# print(test)
#
# ttt ={'nice': 'codein'}
# test.update(ttt)
#
# sss = {'nice' : 'codeout'}
# test.update(sss)
# print(test)


# class redirect:
#     content = ""
#
#     def write(self,str):
#         self.content += str
#     def flush(self):
#         self.content = ""
#
# current = sys.stdout
# r = redirect()
# sys.stdout = r
#
# i = 0
# while i < 10:
#     print(i)
#     i += 1
#
# filename = 'test.json'
# with open(filename, 'a') as file_obj:
#        json.dump(r.content, file_obj)
# print(r.content)
# sys.stdout = current
# print(r.content)

#
# import subprocess
# import os
# import subprocess
# import shutil
#
# #目录文件不存在则自动创建,存在则清空并创建
# def check_dir(path):
#     if not os.path.exists(path):
#         os.makedirs(path)
#     else:
#         shutil.rmtree(path)
#         os.mkdir(path)
#
# #视频提取功能
# def video_extract(source_video,to_path,speed):
#     to_path = to_path+'%05d.jpg'
#     #strcmd = 'ffmpeg -i "%s" -filter:v "select=not(mod(n\,%d)),setpts=N/(25*TB)" -qscale:v 1 "%s"'%(source_video,speed,to_path)
#     strcmd = 'ffmpeg -i "%s" -r %d "%s"'%(source_video,speed,to_path)
#     # strcmd = "ffmpeg", "-i", filename,"-r","1", dest
#     #print(strcmd)
#     subprocess.call(strcmd, shell=True)
#
# #处理流程
# def deal_process(src_path,to_base_path,speed):
#     if not os.path.exists(src_path):
#         return
#     if os.path.isdir(src_path):
#         for dir in os.listdir(src_path):
#             path = os.path.join(src_path,dir)
#             deal_process(path,to_base_path,speed)
#     else:
#         video_name = os.path.splitext(os.path.basename(src_path))[0]
#         to_path = os.path.join(to_base_path,video_name)+'/'
#         # to_path = os.path.join(to_base_path,video_name+'.jpg')
#         check_dir(to_path)
#         # to_path = to_path+video_name+'_'
#         video_extract(src_path,to_path,speed)
#
# if __name__ == '__main__':
#
#     src_path = 'test2.mp4'       #原始视频目录
#     to_base_path = 'datasets/CTW1500/'    #抽帧存放目录
#     speed = 1        # 视频抽帧间隔   1帧/秒
#     deal_process(src_path,to_base_path,speed)
#
#     # os.system('python demo/demo.py \
#     # --config-file configs/BAText/CTW1500/attn_R_50.yaml \
#     # --input datasets/CTW1500/test2/ \
#     # --opts MODEL.WEIGHTS ctw1500_attn_R_50.pth')


import difflib
def str_similar(s1, s2):
    seq = difflib.SequenceMatcher(lambda x:x in " ", s1, s2)
    ratio = seq.ratio()
    return ratio

s1 = "to high reward\nSteps\ncontroller\nCarnegie Mallon University\nAchiyst\nGos\nDymamics\naigonthm\nHuman\nModd!\nFunachom\nInpuits\nvalues that lead\nconrolur\nPhysics brssed\n400\nDARPA\nEatimulor\n300\nPtysccs\nSOrecor\n200\nDeeD RL\nouickly learrs\nCopecol\ngood paramneter\nPzonngr\nCOLLDOUIUM\nEnd-to-end leamiig of diferentiable physics\nSuone\nDAD\nDagg PLL\n100\nProfeesional human game fester\nBma to Era fre telichl  hheppoopperrasringernas artel Meunts. 1012 1122 \n10\nEeVECEE\n10\nPlofessoonlhhuman game CerC.\n10\n"
s2 = "to high reward\nSteps\ncontroller\nCarnegie Meltom University\nACHRTS\nGov\nDyrumics\nHuman\nvalues that lead\naigonthm\nModool\nFunchoon\nInpaits\nDARPA\nconrolur\nPhysics brssed\n400\nEatimulor\n$8pooor\nConacol\n300\n200\nDeeD RL\nPhysccs\ngood paraineter\ngucclyy earns\nPlonngr\nCOLLDOUUUM\nEnd-to-end learning of diferentiable physics\nDAD\n10\nStone\nProfiessional human game fester\n100\nDang 2L\nDna bo Era brkerathe Bigappoo orracrresren worte  oonts ants 2118: 112\nEEESON\n10\n10\n"
ratio = str_similar(s1, s2)
print(ratio)
