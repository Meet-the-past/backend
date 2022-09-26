from subprocess import call
import os, sys
import shutil


def ai_process(uuid):

   UUID =  uuid
 
   inputImagePath =   "ai_image/" + UUID   
   outputImagePath =  "ai_image/" + UUID 

 
   call( f"python /backend/ai/photo_restoration/run.py --input_folder {inputImagePath} --output_folder {outputImagePath}", shell=True)
  # call(f"python run.py --input_folder {inputImagePath} --output_folder {outputImagePath} --GPU -1 --with_scratch") 

   print("AI처리가 완료되었습니다.")