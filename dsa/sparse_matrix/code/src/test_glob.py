import glob

input_pattern = r'C:\Users\USER\PycharmProjects\SparseMatrix\dsa\sparse_matrix\sample_inputs\easy_sample_*.txt'

matching_files = glob.glob(input_pattern)

print(f"Input pattern: {input_pattern}")
print(f"Matching files: {matching_files}")