import subprocess
import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import pickle
import warnings
import sys

def feature_extraction(video_path, directory_read):
    openface_path = 'D:/GP final/Employees_System-master/models/OpenFace_2.2.0_win_x64/FeatureExtraction.exe'
    output_dir = 'D:/GP final/Employees_System-master/models/output'

    os.makedirs(output_dir, exist_ok=True)

    command = [
        openface_path,
        "-f", video_path,
        "-out_dir", output_dir,
        "-2Dfp",
        "-3Dfp",
        "-pdmparams",
        "-pose",
        "-aus",
        "-gaze",
        "-tracked",
        "-hogalign"
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running OpenFace FeatureExtraction: {e}")
        sys.exit(1)

    output_csv = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + '.csv')
    try:
        df = pd.read_csv(output_csv)
    except FileNotFoundError:
        print("     ")
        sys.exit(1)

    gaze = df.loc[:, " gaze_0_x":" gaze_1_z"]
    pose = df.loc[:, " pose_Tx":" pose_Rz"]
    feature_2d = df.loc[:, ' x_0':' y_67']
    feature_3d = df.loc[:, ' X_0':' Z_67']
    AU_s = df.loc[:, " AU01_r":" AU45_r"]

    gaze.columns = [' x_0', ' y_0', ' z_0', ' x_1', ' y_1', ' z_1']
    pose.columns = [' Tx', ' Ty', ' Tz', ' Rx', ' Ry', ' Rz']

    gaze.to_csv(os.path.join(directory_read, "gaze.csv"), index=False)
    pose.to_csv(os.path.join(directory_read, "pose.csv"), index=False)
    feature_2d.to_csv(os.path.join(directory_read, "feature_2d.csv"), index=False)
    feature_3d.to_csv(os.path.join(directory_read, "feature_3d.csv"), index=False)
    AU_s.to_csv(os.path.join(directory_read, "AU_s.csv"), index=False)

def scaling(data_grouped):
    scaler = MinMaxScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(data_grouped), columns=data_grouped.columns)
    return scaled_data

def pca_function(csv_file, component):
    data = pd.DataFrame(csv_file)
    pca = PCA(n_components=component)
    pca.fit(data)
    pca_data = pca.transform(data)
    return pca_data

def combine_test(pca_data, folder_data2):
    pca_df = pd.DataFrame(pca_data)
    combined = pd.concat([pca_df, folder_data2], axis=1)
    return combined

def process_directory(directory_read):
    sorted_filenames = ['AU_s.csv', 'feature_2d.csv', 'feature_3d.csv', 'gaze.csv', 'pose.csv']
    last2 = []
    first3 = []

    for csv in sorted_filenames:
        file_path = os.path.join(directory_read, csv)
        data = pd.read_csv(file_path)
        #scaled_data=scaling(data)
        if 'gaze' in csv or 'pose' in csv:
            last2.append(data)
        else:
            first3.append(data)

    combined_data1 = pd.concat(first3, axis=1, join='outer')
    combined_data2 = pd.concat(last2, axis=1, join='outer')

    combined_data1.interpolate(method='linear', inplace=True)
    combined_data2.interpolate(method='linear', inplace=True)

    pca_data = pca_function(combined_data1, 3)
    combined_df = combine_test(pca_data, combined_data2)
    return combined_df

def model_predict(model, sample):
    sample.columns = sample.columns.astype(str)
    sample = sample[['0', '1', '2', ' x_0', ' y_0', ' z_0', ' x_1', ' y_1', ' z_1', ' Tx', ' Ty', ' Tz', ' Rx', ' Ry', ' Rz']]
    y_pred = model.predict(sample)
    proportion_1 = sum(y_pred == 1) / len(y_pred)
    return 1 if proportion_1 >= 0.7 else 0

def predict(val):
    return 'Depressed' if val else 'Not Depressed'

def run_code(video_path, directory_read, model_path):
    feature_extraction(video_path, directory_read)
    combined_df = process_directory(directory_read)

    with open(model_path, 'rb') as file:
        loaded_model = pickle.load(file)

    val = model_predict(loaded_model, combined_df)
    warnings.simplefilter("ignore")

    predict_val = predict(val)
    return predict_val

hi = sys.argv[1]
video_path = os.path.join('D:/GP final/Employees_System-master/Samples', hi)
directory_read = 'D:/GP final/Employees_System-master/models/output'
model_path = 'D:/GP final/Employees_System-master/models/logistic_regression_model.pkl'
predict_val = run_code(video_path, directory_read, model_path)
print(predict_val)
