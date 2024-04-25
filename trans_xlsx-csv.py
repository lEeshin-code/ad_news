import os
import glob
import pandas as pd
import re

# 변환할 폴더 경로 설정
root_folder = "20240410"  # 폴더이름으로 대체하세요.

# 출력 폴더 경로 설정
output_folder = root_folder + "_csv"  # 저장할 경로로 대체하세요.

# 출력 폴더 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"출력 폴더 {output_folder}가 생성되었습니다.")

# 폴더 내의 모든 하위 폴더를 탐색하며 엑셀 파일을 찾음
excel_files = glob.glob(os.path.join(root_folder, '**/*.xlsx'), recursive=True)

# 엑셀 파일을 CSV로 변환하는 함수 정의
def excel_to_csv(file_path):
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path)
        
        # 파일 이름에서 날짜 부분과 확장자 제거
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        file_name_no_date = re.sub(r'_\d{8}-\d{8}', '_', file_name)
        
        # 파일 이름에서 숫자로 시작하는 접두어 유지
        prefix = re.match(r'^(\d+\s)?', file_name).group()
        
        # 변환된 파일 이름 설정
        csv_file_name = os.path.join(output_folder, os.path.relpath(os.path.dirname(file_path), root_folder),
                                      prefix + file_name_no_date + ".csv")
        
        # 폴더가 없는 경우 생성
        os.makedirs(os.path.dirname(csv_file_name), exist_ok=True)
        
        # CSV 파일로 저장
        df.to_csv(csv_file_name, index=False, encoding='utf-8-sig')
        
        print(f"{file_path}를 CSV로 변환하여 {csv_file_name}에 저장했습니다.")
    except Exception as e:
        print(f"{file_path} 변환 중 오류가 발생했습니다: {e}")

# 모든 엑셀 파일을 CSV로 변환
for excel_file in excel_files:
    excel_to_csv(excel_file)

print("모든 파일 변환이 완료되었습니다.")
