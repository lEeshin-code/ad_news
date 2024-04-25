import os
import pandas as pd

def standardize_data(input_folder, output_folder):
    errors = []
    # 출력 폴더가 없는 경우 폴더를 생성합니다.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for root, dirs, files in os.walk(input_folder):
        for file_name in files:
            if file_name.endswith(".csv"):
                input_file_path = os.path.join(root, file_name)
                output_sub_folder = os.path.relpath(root, input_folder)
                output_sub_folder_path = os.path.join(output_folder, output_sub_folder)
                if not os.path.exists(output_sub_folder_path):
                    os.makedirs(output_sub_folder_path)
                output_file_path = os.path.join(output_sub_folder_path, file_name)
                try:
                    # 파일을 UTF-8 인코딩으로 읽어옵니다.
                    df = pd.read_csv(input_file_path, encoding='utf-8')
                    # 여기에서 데이터 표준화 작업을 수행합니다.
                    # 파일을 UTF-8 with BOM 형식으로 저장합니다.
                    df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
                except Exception as e:
                    errors.append(f"파일 '{file_name}'을(를) 표준화하는 중 오류 발생: {e}")
    if len(errors) == 0:
        print(f"폴더 '{input_folder}'의 데이터를 성공적으로 표준화하여 '{output_folder}' 폴더에 저장했습니다.")
    else:
        for error in errors:
            print(error)

# ad_data_csv 폴더의 데이터 표준화
input_folder_ad = "ad_data_csv"
output_folder_ad = "ad_data_standardized"
standardize_data(input_folder_ad, output_folder_ad)

# non_ad_data_csv 폴더의 데이터 표준화
input_folder_non_ad = "non_ad_data_csv"
output_folder_non_ad = "non_ad_data_standardized"
standardize_data(input_folder_non_ad, output_folder_non_ad)
