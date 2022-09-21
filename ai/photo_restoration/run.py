
import os
import argparse
import shutil
import sys
from subprocess import call

def run_cmd(command):
    try:
        call(command, shell=True)
    except KeyboardInterrupt:
        print("Process interrupted")
        sys.exit(1)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_folder", type=str, default="./test_images/old", help="Test images")
    parser.add_argument(
        "--output_folder",
        type=str,
        default="./output",
        help="Restored images, please use the absolute path",
    )
    opts = parser.parse_args()

    inputImagePath= opts.input_folder
    outputImagePath = opts.output_folder
    imageName = "not_Found"

    if not os.path.exists(outputImagePath):  #결과 이미지 & 폴더 생성예시 (실제로는 call함수에서 작업이 완료된 이미지를 저장함)
         os.makedirs(outputImagePath)
    if not os.path.exists(outputImagePath+"/final_output"):  #결과 이미지 & 폴더 생성예시 (실제로는 call함수에서 작업이 완료된 이미지를 저장함)
         os.makedirs(outputImagePath+"/final_output")
    
    for (root, directories, files) in os.walk(inputImagePath):
        for file in files:
            file_path = os.path.join(root, file)
            imageName = os.path.basename(os.path.normpath(file_path))
                
           

    print("aa")
    print(imageName)
    f = open(outputImagePath+"/final_output/"+imageName, 'w')  #가짜로 결과 이미지 파일을 만듦
    f.close()

    print(inputImagePath+"폴더 내부의"+imageName+"이미지를 AI처리하여"+outputImagePath+"/final_output/"+imageName+"폴더에 결과이미지를 생성했습니다.")
   