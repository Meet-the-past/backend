from subprocess import call

import os, sys

import shutil

def ai_process(uuid):
   UUID =  uuid
   inputImagePath =   "ai_image/" + UUID
   outputImagePath =  "ai_image/" + UUID
   call( f"python /backend/ai/photo_restoration/run.py --input_folder {inputImagePath} --output_folder {outputImagePath} --GPU -1 --with_scratch", shell=True)