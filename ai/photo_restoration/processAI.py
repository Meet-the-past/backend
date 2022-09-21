from subprocess import call
import os, sys
import shutil


def ai_process(uuid, imageName):

   '''
   전체 진행과정 요약
   1. http://localhost:8000/api/images API요청 -> 요청한 이미지를 inputImagePath/uuid 폴더에 랜덤이름으로 저장
   2. mtpAi.py 함수 실행  image_url =  mtpAi(uuid , imgName)   (uuid, imgName을 매개변수로 넘김)
		(uuid는 이미지 테이블의 식별 기본키)
   3. mtpAi함수 (현재 정의된 코드)에서는 아래의 과정을 진행
   3-1 inputImagePath/uuid , outputImagePath/uuid 변수를 지정해 "어떤 폴더의 이미지"에서 처리된 결과를 "어떤 폴더"에 저장할 지 명시
   ( inputImagePath/uuid 폴더내부의 모든 이미지를 다 AI처리하기때문에 uuid값은 고유하게 폴더를 식별해야함)
   ( 처리된 결과는 outputImagePath/uuid/final_output/imgName 의 이름으로 이미지가 저장된다.)
   3-2 call("python run.py --input_folder ./test_images/old --output_folder ./output/ --GPU -1 --with_scratch") 실제 AI코드 돌리기
   4. 처리된 이미지 inputImagePath/uuid/final_output/imgName 경로에서 결과 이미지를 가져와 버킷에 업로드 및 변수에 url저장
   5. inputImagePath/uuid , outputImagePath/uuid 폴더 내부의 이미지 전부 삭제
   6. (4)번에서 저장한 결과이미지 url return  (해당 값은 이제 프론트로 함수를 타고 넘어간다.)
	결과 값으로 uuid를 념겨서 (이미지 객체의 기본키) , DB에서 해당 uuid값을 가지고 origin_url
  processed_url을 꺼내 프론트로 보낸다
   '''
   #call("cd /backend/ai/photo_restoration/")
   UUID =  uuid
   TEMPIMAGENAME = imageName


   inputImagePath =   "ai_image/" + UUID   
   outputImagePath =  "ai_image/" + UUID 

 
   if not os.path.exists(inputImagePath):  #입력 이미지 폴더 생성예시 (실제로는 앞의 api에서 이미 이미지를 특정폴더에 저장)
         os.makedirs(inputImagePath)

   f = open(inputImagePath+"/"+TEMPIMAGENAME+".png", 'w')  #실제로는 사용자가 api로 요청한 이미지를 해당 경로에 저장해야하지만 테스트용으로 따로 만든 코드
   f.close()

   call( f"python /backend/ai/photo_restoration/run.py --input_folder {inputImagePath} --output_folder {outputImagePath}", shell=True)
   # call("python run.py --input_folder ./test_images/old --output_folder ./output/ --GPU -1 --with_scratch") (실제 돌리는 명령어)


#    url = get_img_url("backend/ai/photo_restoration/"+outputImagePath+"/final_output/"+TEMPIMAGENAME)
   print("버킷에 파일을 업로드")
   print("버킷 url은 ~~입니다.") #구현필요

   
#    if os.path.exists(inputImagePath):  #input 폴더내부의 이미지 삭제
#     shutil.rmtree(inputImagePath)
   
#    if os.path.exists(outputImagePath): #output 폴더내부의 이미지 삭제
#     shutil.rmtree(outputImagePath)

#    print(inputImagePath+"폴더 내부의 이미지와" + "photo_restoration/"+outputImagePath+"폴더 내부의 이미지를 모두 삭제합니다.")
   print("결과 url을 return합니다.")