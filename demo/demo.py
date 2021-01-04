# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import argparse
import difflib
import glob
import multiprocessing as mp
import os
import sys
import time
import cv2
import tqdm
import json
import subprocess
import shutil
import re

from detectron2.data.detection_utils import read_image
from detectron2.utils.logger import setup_logger
from predictor import VisualizationDemo
from adet.config import get_cfg

from adet.evaluation.text_evaluation import instances_to_coco_json as rec_result


# constants
WINDOW_NAME = "COCO detections"
text_output = {'time':'content'}

def str_similar(s1, s2):
    seq = difflib.SequenceMatcher(lambda x:x in " ", s1, s2)
    ratio = seq.ratio()
    return ratio

class redirect:
    content = ""

    def write(self,str):
        self.content += str
    def flush(self):
        self.content = ""

def setup_cfg(args):
    # load config from file and command-line arguments
    cfg = get_cfg()
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.FCOS.INFERENCE_TH_TEST = args.confidence_threshold
    cfg.MODEL.MEInst.INFERENCE_TH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2 Demo")
    parser.add_argument(
        "--config-file",
        default="configs/quick_schedules/e2e_mask_rcnn_R_50_FPN_inference_acc_test.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument("--webcam", action="store_true", help="Take inputs from webcam.")
    parser.add_argument("--video-input", help="Path to video file.")
    parser.add_argument("--input", nargs="+", help="A list of space separated input images")
    parser.add_argument(
        "--output",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )

    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.5,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    return parser


if __name__ == "__main__":

    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    logger = setup_logger()
    logger.info("Arguments: " + str(args))
    cfg = setup_cfg(args)
    demo = VisualizationDemo(cfg)

    #######################3just use this segment to do text_recgonize##################3
    if args.input:

        if os.path.isdir(args.input[0]):
            args.input = [os.path.join(args.input[0], fname) for fname in os.listdir(args.input[0])]
        elif len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"

        imageinput = args.input
        imageinput.sort(key = lambda x:int(x.split('/')[-1].split('.')[0]))
        i = 0
        temp = ''
        for path in tqdm.tqdm(args.input, disable=not args.output):

            current = sys.stdout
            r = redirect()
            sys.stdout = r
            #all printf saved in r.content from now

            #convert filename to video_time
            basename = os.path.basename(path)
            seconds = int(os.path.splitext(basename)[0]) - 1
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            video_time = '{0}:{1:02d}:{2:02d}'.format(h, m, s)

            # use PIL, to be consistent with evaluation
            img = read_image(path, format="BGR")
            start_time = time.time()
            predictions, visualized_output = demo.run_on_image(img)
            # logger.info(
            #     "{}: detected {} instances in {:.2f}s".format(
            #         path, len(predictions["instances"]), time.time() - start_time
            #     )
            # )
            if r.content == "":
                pass
            else:
                ratio = str_similar(temp, r.content)
                if ratio < 0.2:  #When ratio < 0.2, we seems the content is a new_text_result, it can be ajusted
                    temp = r.content
                    new_text_result = {video_time:r.content}

                    #save text_result into .json file
                    filename = 'test.json'
                    with open(filename, 'a') as file_obj:
                        json.dump(new_text_result, file_obj, indent=4)

            sys.stdout = current
            #stop to capture printf content from now

            if args.output:
                if os.path.isdir(args.output):
                    assert os.path.isdir(args.output), args.output
                    out_filename = os.path.join(args.output, os.path.basename(path))
                else:
                    assert len(args.input) == 1, "Please specify a directory with args.output"
                    out_filename = args.output
                visualized_output.save(out_filename)
            else:
                # cv2.imshow(WINDOW_NAME, visualized_output.get_image()[:, :, ::-1])
                # cv2.waitKey(1)
                print(str(i) + 'done')
                i = i + 1

                # cv2.destroyAllWindows()
                # if cv2.waitKey(0) == 1:
                #     break  # esc to quit

        # filename = 'test.json'
        # with open(filename, 'a') as file_obj:
        #     json.dump(r.content, file_obj)
        # print(r.content)
        # sys.stdout = current

    ##########################From here below are USELESS###############################
    elif args.webcam:
        assert args.input is None, "Cannot have both --input and --webcam!"
        cam = cv2.VideoCapture(0)
        for vis in tqdm.tqdm(demo.run_on_video(cam)):
            cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.imshow(WINDOW_NAME, vis)
            if cv2.waitKey(1) == 27:
                break  # esc to quit
        cv2.destroyAllWindows()
    elif args.video_input:
        video = cv2.VideoCapture(args.video_input)
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frames_per_second = video.get(cv2.CAP_PROP_FPS)
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        basename = os.path.basename(args.video_input)

        if args.output:
            if os.path.isdir(args.output):
                output_fname = os.path.join(args.output, basename)
                output_fname = os.path.splitext(output_fname)[0] + ".mkv"
            else:
                output_fname = args.output
            assert not os.path.isfile(output_fname), output_fname
            output_file = cv2.VideoWriter(
                filename=output_fname,
                # some installation of opencv may not support x264 (due to its license),
                # you can try other format (e.g. MPEG)
                fourcc=cv2.VideoWriter_fourcc(*"x264"),
                fps=float(frames_per_second),
                frameSize=(width, height),
                isColor=True,
            )
        assert os.path.isfile(args.video_input)
        for vis_frame in tqdm.tqdm(demo.run_on_video(video), total=num_frames):
            if args.output:
                output_file.write(vis_frame)
            else:
                cv2.namedWindow(basename, cv2.WINDOW_NORMAL)
                cv2.imshow(basename, vis_frame)
                if cv2.waitKey(1) == 27:
                    break  # esc to quit
        video.release()
        if args.output:
            output_file.release()
        else:
            cv2.destroyAllWindows()


    # filename = 'test.json'
    # with open(filename, 'a') as file_obj:
    #     json.dump(r.content, file_obj)
    # print(r.content)
    # sys.stdout = current


    # filename = 'result.json'
    # with open(filename, 'a') as file_obj:
    #     json.dump(output_result, file_obj, indent=4)


