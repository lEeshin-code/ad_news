#파일1(원본)에 파일2(레이블링)이 없을경우 추가하는 코드
# import pandas as pd

# def update_dataset(file1_path, file2_path):
#     # 파일 1 읽기
#     file1_data = pd.read_csv(file1_path)
#     # 파일 2 읽기
#     file2_data = pd.read_csv(file2_path)

#     # 파일 1과 파일 2의 레이블이 다른 경우를 찾아서 파일 1에 추가
#     new_data = file2_data[~file2_data['뉴스 식별자'].isin(file1_data['뉴스 식별자'])]
#     updated_data = pd.concat([file1_data, new_data], ignore_index=True)

#     # 업데이트된 파일 1 저장 (인코딩을 'utf-8-sig'로 수정)
#     updated_data.to_csv(file1_path, index=False, encoding='utf-8-sig')

#     print(f"{file1_path}이(가) 업데이트되었습니다.")

# # 업데이트할 CSV 파일 경로
# file1_path = "미래산업기술전략_바이오_.csv"
# file2_path = "미래산업기술전략_바이오_2.csv"

# update_dataset(file1_path, file2_path)












#데이터 형식 확인 및 정밀 분석 코드
# import pandas as pd

# def compare_datasets(file1_path, file2_path):
#     # CSV 파일 읽기
#     file1_data = pd.read_csv(file1_path)
#     file2_data = pd.read_csv(file2_path)
    
#     # 두 데이터셋 비교
#     if file1_data.equals(file2_data):
#         print("두 데이터셋은 동일합니다.")
#     else:
#         print("두 데이터셋은 다릅니다.")
        
#         # 열 이름 비교
#         if file1_data.columns.equals(file2_data.columns):
#             print("데이터셋의 열 이름이 일치합니다.")
#         else:
#             print("데이터셋의 열 이름이 일치하지 않습니다.")

#         # 데이터 형식 비교
#         if file1_data.dtypes.equals(file2_data.dtypes):
#             print("데이터셋의 열의 데이터 형식이 일치합니다.")
#         else:
#             print("데이터셋의 열의 데이터 형식이 일치하지 않습니다.")
#             print("file1_data 데이터 형식:")
#             print(file1_data.dtypes)
#             print("\nfile2_data 데이터 형식:")
#             print(file2_data.dtypes)

#     # 빈 데이터셋인지 확인
#     if file1_data.empty:
#         print(f"{file1_path}은(는) 빈 데이터셋입니다.")
#     if file2_data.empty:
#         print(f"{file2_path}은(는) 빈 데이터셋입니다.")

# # 비교할 CSV 파일 경로
# file1_path = "미래산업기술전략_바이오_.csv"
# file2_path = "미래산업기술전략_바이오_2.csv"

# compare_datasets(file1_path, file2_path)










#데이터 형식 일치 및 업데이트 코드
import pandas as pd

def most_common_dtype(series_list):
    # 각 열의 데이터 형식 빈도수 계산
    dtype_counts = {}
    for series in series_list:
        dtype_counts[series.dtype] = dtype_counts.get(series.dtype, 0) + 1
    
    # 가장 많이 나타나는 데이터 형식 찾기
    most_common = max(dtype_counts, key=dtype_counts.get)
    return most_common

def update_dataset(file1_path, file2_path):
    # CSV 파일 읽기
    file1_data = pd.read_csv(file1_path)
    file2_data = pd.read_csv(file2_path)
    
    # 열 이름 비교
    if not file1_data.columns.equals(file2_data.columns):
        print("데이터셋의 열 이름이 일치하지 않습니다.")
        return
    
    # 파일1과 파일2의 각 열의 데이터 형식 비교 후 일치시키기
    for column in file1_data.columns:
        if file1_data[column].dtype != file2_data[column].dtype:
            most_common_type = most_common_dtype([file1_data[column], file2_data[column]])
            file1_data[column] = file1_data[column].astype(most_common_type)
            file2_data[column] = file2_data[column].astype(most_common_type)
    
    # 파일1과 파일2의 데이터를 병합하여 각각 업데이트
    updated_file1_data = pd.concat([file1_data, file2_data], ignore_index=True)
    updated_file2_data = pd.concat([file2_data, file1_data], ignore_index=True)
    
    # 파일1 업데이트 후 저장
    updated_file1_data.to_csv(file1_path, index=False, encoding='utf-8-sig')
    print(f"{file2_path}의 데이터가 {file1_path}에 업데이트되었습니다.")
    
    # 파일2 업데이트 후 저장
    updated_file2_data.to_csv(file2_path, index=False, encoding='utf-8-sig')
    print(f"{file1_path}의 데이터가 {file2_path}에 업데이트되었습니다.")

# 비교 및 업데이트할 CSV 파일 경로
file1_path = "미래산업기술전략_바이오_.csv"
file2_path = "미래산업기술전략_바이오_2.csv"

update_dataset(file1_path, file2_path)
