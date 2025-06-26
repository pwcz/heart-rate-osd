import os
import cv2
import glob
import platform
import argparse

from tqdm.auto import tqdm
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from fit_reader import FitReader


RGB_COLOR = (255, 0, 0)


def get_system_font(size=50):
    system = platform.system()
    if system == "Windows":
        font_path = "C:/Windows/Fonts/arialuni.ttf"
    elif system == "Darwin":  # macOS
        font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    else:  # Linux
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Fallback
    return ImageFont.truetype(font_path, size=size)


font = get_system_font()


def read_video_file(file):
    cap = cv2.VideoCapture(file)
    frame_number = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pbar = tqdm(total=frame_number, desc=f"file: {file}")
    while cap.isOpened():
        ret, frame = cap.read()
        video_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        pbar.update(1)
        if ret:
            yield frame, video_time
        else:
            break

    cap.release()


def write_osd_to_frame(frame, heart_rate):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_frame = Image.fromarray(frame)

    draw = ImageDraw.Draw(pil_frame)

    draw.text((1700, 50), f"❤ {heart_rate}", fill=RGB_COLOR, font=font, stroke_width=3, stroke_fill=(0, 0, 0))

    frame_with_text = np.array(pil_frame)
    return cv2.cvtColor(frame_with_text, cv2.COLOR_RGB2BGR)


def write_osd(file_name, fit_file):
    cap = cv2.VideoCapture(file_name)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_filename = "heart_rate_osd.MOV"
    print(f"Output file = {output_filename}")

    out = cv2.VideoWriter(output_filename, fourcc, video_fps, (frame_width, frame_height))

    fit_reader = FitReader(fit_file)
    fit_reader_gen = fit_reader.get_heart_rate()
    next(fit_reader_gen)
    for frame, time in read_video_file(file_name):
        heart_rate = fit_reader_gen.send(int(time/1000))
        out.write(write_osd_to_frame(frame, heart_rate))

    out.release()


def check_osd(video_file):
    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        raise FileNotFoundError("Failed to read video")

    ret, frame = cap.read()
    if ret:
        frame_with_text = write_osd_to_frame(frame, 90)
        cv2.imshow('Frame', frame_with_text)
        while cv2.waitKey(25) & 0xFF != ord('q'):
            pass
        cv2.imwrite("test_frame.png", frame_with_text)
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Write heart rate OSD from fit file into video')
    parser.add_argument('--preview', action=argparse.BooleanOptionalAction, help='display only one frame as preview')
    args = parser.parse_args()

    fit_files = glob.glob(os.path.join("data", '*.fit'))
    movie_files = glob.glob(os.path.join("data", '*.MOV'))
    assert len(fit_files) == 1 and len(movie_files) == 1

    if args.preview:
        check_osd(movie_files[0])
    else:
        write_osd(movie_files[0], fit_files[0])
