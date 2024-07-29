import argparse
import numpy as np
import pandas as pd
from fastdtw import fastdtw
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference_path", type=str, default="../dataset/third_test.txt")
    parser.add_argument("--predicted_path", type=str, default="../dataset/results/claude-3-opus-20240229-third_test.txt")
    args = parser.parse_args()

    reference_path_df = pd.read_csv(args.reference_path, sep='	', header=None)
    reference_path_df.columns = ['VehicleName', 'TimeStamp', 'POS_X', 'POS_Y', 'POS_Z', 'Q_W', 'Q_X', 'Q_Y', 'Q_Z', 'ImageFile']
    reference_path_df = reference_path_df.iloc[1: , :]

    predicted_path_df = pd.read_csv(args.predicted_path, sep='	', header=None)
    predicted_path_df.columns = ['VehicleName', 'TimeStamp', 'POS_X', 'POS_Y', 'POS_Z', 'Q_W', 'Q_X', 'Q_Y', 'Q_Z', 'ImageFile']
    predicted_path_df = predicted_path_df.iloc[1: , :]

    reference_path_df[['POS_X', 'POS_Y', 'POS_Z']] = reference_path_df[['POS_X', 'POS_Y', 'POS_Z']].apply(pd.to_numeric)
    predicted_path_df[['POS_X', 'POS_Y', 'POS_Z']] = predicted_path_df[['POS_X', 'POS_Y', 'POS_Z']].apply(pd.to_numeric)

    reference_path_df['-POS_X'] = reference_path_df['POS_X'].apply(lambda x: x*-1)
    reference_path_df['-POS_Y'] = reference_path_df['POS_Y'].apply(lambda x: x*-1)
    reference_path_df['-POS_Z'] = reference_path_df['POS_Z'].apply(lambda x: x*-1)

    predicted_path_df['-POS_X'] = predicted_path_df['POS_X'].apply(lambda x: x*-1)
    predicted_path_df['-POS_Y'] = predicted_path_df['POS_Y'].apply(lambda x: x*-1)
    predicted_path_df['-POS_Z'] = predicted_path_df['POS_Z'].apply(lambda x: x*-1)

    reference_path = get_locs(reference_path_df)
    predicted_path = get_locs(predicted_path_df)
    
    print(f"PL (Predicted path): {path_length(predicted_path).round(1)}")
    print(f"PL (Reference path): {path_length(reference_path).round(1)}")
    print(f"SR: {success_rate(predicted_path, reference_path, 20)}")
    print(f"OSR: {oracle_success_rate(predicted_path, reference_path, 20)}")
    print(f"NE: {euclidian_distance(np.array(predicted_path[-1]), np.array(reference_path[-1])).round(2)}")
    print(f"nDTW: {ndtw(predicted_path, reference_path, 20).round(2)}")
    print(f"SDTW: {sdtw(predicted_path, reference_path, 20).round(2)}")
    print(f"CLS: {cls(predicted_path, reference_path, 20).round(2)}")
    
    plot_paths(predicted_path, reference_path)

# Returns locations in np array
def get_locs(df):
    res = []
    for row in df.iterrows():
        res.append(np.array([row[1]['-POS_X'], row[1]['POS_Y'], row[1]['-POS_Z']]))
    return np.array(res)

# Returns euclidian distance between point_a and point_b
def euclidian_distance(position_a, position_b) -> float:
    return np.linalg.norm(np.array(position_b) - np.array(position_a), ord=2)

# Returns Success Rate (SR) that indicates the navigation is considered successful 
# if the agent stops within success_distance_threshold of the destination
def success_rate(p_path, r_path, success_distance_threshold):
    distance_to_target = euclidian_distance(np.array(p_path[-1]), np.array(r_path[-1]))
    #print(distance_to_target)
    if distance_to_target <= success_distance_threshold:
        return 1.0
    else:
        return 0.0

# Returns Oracle Success Rate (OSR) where one navigation is considered oracle success
# if the distance between the destination and any point on the trajectory is less than success_distance_threshold
def oracle_success_rate(p_path, r_path, success_distance_threshold):
    for p in p_path:
        if euclidian_distance(p, r_path[-1]) <= success_distance_threshold:
            #print(p, r_path[-1])
            return 1.0
    return 0.0

# Returns normalized dynamic time warping metric score
def ndtw(p_path, r_path, success_distance_threshold):
    dtw_distance = fastdtw(p_path, r_path, dist=euclidian_distance)[0]
    nDTW = np.exp(-dtw_distance / (len(r_path) * success_distance_threshold))
    return nDTW

# Returns Success weighted by normalized Dynamic Time Warping 
# where one navigation is considered successful if one is returned
def sdtw(p_path, r_path, success_distance_threshold):
    return success_rate(p_path, r_path, success_distance_threshold) * ndtw(p_path, r_path, success_distance_threshold)

# Returns path length
def path_length(path):
    path_length = 0.0
    previous_position = path[0]
    for current_position in path[1:]:
        path_length += euclidian_distance(current_position, previous_position)    
        previous_position = current_position
    return path_length

# Returns path coverage score that indicates how well the reference path
# is covered by the predicted path
def path_coverage(p_path, r_path, success_distance_threshold):
    coverage = 0.0
    for r_loc in r_path:
        min_distance = float('inf')
        for p_loc in p_path:
            distance = euclidian_distance(p_loc, r_loc)
            if distance < min_distance:
                min_distance = distance
        coverage += np.exp(-min_distance / success_distance_threshold)
    return coverage / len(r_path)

# Returns the expected optimal length score given reference path’s coverage of predicted path
def epl(p_path, r_path, success_distance_threshold):
    return path_coverage(p_path, r_path, success_distance_threshold) * path_length(r_path)

# Returns length score of predicted path respect to reference path
def ls(p_path, r_path, success_distance_threshold):
    return epl(p_path, r_path, success_distance_threshold) / (epl(p_path, r_path, success_distance_threshold) + np.abs(epl(p_path, r_path, success_distance_threshold) - path_length(p_path)))

# Returns Coverage weighted by Length Score (CLS) indicates
# how closely predicted path conforms with the entire reference path 
def cls(p_path, r_path, success_distance_threshold):
    return path_coverage(p_path, r_path, success_distance_threshold) * ls(p_path, r_path, success_distance_threshold)

# Plots the reference and predicted paths
def plot_paths(p_path, r_path):
    ax = plt.axes(projection='3d')
    ax.plot3D(r_path[:, 0], r_path[:, 1], r_path[:, 2], 'red')
    ax.plot3D(p_path[:, 0], p_path[:, 1], p_path[:, 2], 'blue')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.legend (["Reference Path", "Predicted Path"])
    plt.show()

if __name__ == '__main__':
    main()