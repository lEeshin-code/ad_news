import os
import pandas as pd

def update_csv_files_in_folder(folder_path):
    # 폴더 내의 모든 CSV 파일을 탐색
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                
                # cleaned 파일 경로 설정
                cleaned_file_path = os.path.join(root, file.replace('.csv', 'cleaned.csv'))
                
                if os.path.exists(cleaned_file_path):
                    print(f"파일 업데이트 중: {file_path}")
                    
                    # CSV 파일 읽어오기
                    df = pd.read_csv(file_path)
                    
                    # cleaned 파일 불러오기
                    cleaned_df = pd.read_csv(cleaned_file_path)
                    
                    # 분석 제외 여부 열을 광고성 여부 열로 변경
                    if '분석제외 여부' in df.columns:
                        df.rename(columns={'분석제외 여부': '광고성 여부'}, inplace=True)
                    
                        # 중복되는 데이터를 찾아서 광고성 여부 열 추가 (0과 1로 이진 분류)
                        df['광고성 여부'] = 1  # 기본값은 광고로 설정
                        for index, row in df.iterrows():
                            duplicate_rows = cleaned_df[cleaned_df['제목'] == row['제목']]
                            if not duplicate_rows.empty:
                                df.at[index, '광고성 여부'] = 0  # 중복된 데이터는 광고 아님으로 설정
                                
                        # 업데이트된 CSV 파일 저장 (원본 파일에 열을 추가하여 업데이트)
                        df.to_csv(file_path, index=False, encoding='utf-8-sig')
                        print(f"{file_path} 업데이트 완료")
                    else:
                        print(f"{file_path}에 '분석제외 여부' 열이 존재하지 않습니다.")

# 데이터셋 폴더 경로 설정
folder_path = "plus_folder"  # 폴더 경로로 대체하세요.

# CSV 파일 업데이트 및 저장
update_csv_files_in_folder(folder_path)

print("모든 파일 업데이트가 완료되었습니다.")
