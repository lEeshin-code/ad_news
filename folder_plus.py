import os
import shutil
import pandas as pd

# 두 개의 폴더 경로 설정
folder1 = "ad_data_csv"  # 폴더1의 경로로 대체하세요.
folder2 = "non_ad_data_csv"  # 폴더2의 경로로 대체하세요.

# 결과를 저장할 폴더 경로 설정
output_folder = "plus_folder"  # 저장할 경로로 대체하세요.

# 폴더 내의 모든 파일을 탐색하며 CSV 파일을 찾음
def find_csv_files(folder):
    csv_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

# 두 폴더에서 찾은 동일한 이름의 폴더 목록 가져오기
folder1_folders = set(os.listdir(folder1))
folder2_folders = set(os.listdir(folder2))
common_folders = folder1_folders.intersection(folder2_folders)

# 결과를 저장할 폴더 생성
os.makedirs(output_folder, exist_ok=True)

# 동일한 이름의 폴더에서 CSV 파일 병합 및 결과 폴더에 저장
for folder_name in common_folders:
    folder1_csv_files = find_csv_files(os.path.join(folder1, folder_name))
    folder2_csv_files = find_csv_files(os.path.join(folder2, folder_name))
    merged_csv_files = folder1_csv_files + folder2_csv_files
    
    # 결과 저장 폴더 생성
    output_folder_path = os.path.join(output_folder, folder_name)
    os.makedirs(output_folder_path, exist_ok=True)
    
    for csv_file in merged_csv_files:
        # 결과 폴더에 복사하여 저장
        relative_path = os.path.relpath(csv_file, folder1 if csv_file in folder1_csv_files else folder2)
        output_file = os.path.join(output_folder_path, os.path.basename(relative_path))
        shutil.copyfile(csv_file, output_file)
        print(f"{csv_file}를 {output_file}로 복사하여 저장했습니다.")

print("모든 파일 병합이 완료되었습니다.")
