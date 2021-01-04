# import cv2
# import os
#
# EXTRACT_FREQUENCY = 1
#
#
# def extract(videopath, index=EXTRACT_FREQUENCY):
#     dst_folder = videopath.split('.', 1)[0]
#     import shutil
#     try:
#         shutil.rmtree(dst_folder)
#     except OSError:
#         pass
#
#     os.mkdir(dst_folder)
#     video = cv2.VideoCapture()
#     if not video.open(videopath):
#         print("can not open the video")
#         exit(1)
#     count = 1
#     while True:
#         _, frame = video.read()
#         if frame is None:
#             break
#         if count % EXTRACT_FREQUENCY == 0:
#             save_path = "{}/{:>d}.jpg".format(dst_folder, index)
#             cv2.imwrite(save_path, frame)
#             index += 1
#         count += 1
#     video.release()
#     print("Totally save {:d} pics".format(index - 1))
#
#
# if __name__ == '__main__':
#     extract('top-down-test2.mp4')


import time
import subprocess
import os
import subprocess
import shutil

#目录文件不存在则自动创建,存在则清空并创建
def check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)

#视频提取功能
def video_extract(source_video,to_path,speed):
    to_path = to_path+'%05d.jpg'
    #strcmd = 'ffmpeg -i "%s" -filter:v "select=not(mod(n\,%d)),setpts=N/(25*TB)" -qscale:v 1 "%s"'%(source_video,speed,to_path)
    strcmd = 'ffmpeg -i "%s" -r %d "%s"'%(source_video,speed,to_path)
    # strcmd = "ffmpeg", "-i", filename,"-r","1", dest
    #print(strcmd)
    subprocess.call(strcmd, shell=True)

#处理流程
def deal_process(src_path,to_base_path,speed):
    if not os.path.exists(src_path):
        return
    if os.path.isdir(src_path):
        for dir in os.listdir(src_path):
            path = os.path.join(src_path,dir)
            deal_process(path,to_base_path,speed)
    else:
        video_name = os.path.splitext(os.path.basename(src_path))[0]
        to_path = os.path.join(to_base_path,video_name)+'/'
        # to_path = os.path.join(to_base_path,video_name+'.jpg')
        check_dir(to_path)
        # to_path = to_path+video_name+'_'
        video_extract(src_path,to_path,speed)

if __name__ == '__main__':
    this_module_start = time.time()

    #convert video to images
    src_path = 'test2.mp4'       #原始视频目录
    to_base_path = 'datasets/CTW1500/'    #抽帧存放目录
    speed = 1        # 视频抽帧间隔   1帧/秒
    deal_process(src_path,to_base_path,speed)

    #use cmd to do text_recgonize
    demo_command = 'python demo/demo.py \
     --config-file configs/BAText/CTW1500/attn_R_50.yaml \
     --input ' + to_base_path + str(src_path.split('.')[0]) + '\
     --opts MODEL.WEIGHTS ctw1500_attn_R_50.pth'

    os.system(demo_command)

    this_module_end = time.time()
    print("This module cost " + str(this_module_end - this_module_start) + "s")


