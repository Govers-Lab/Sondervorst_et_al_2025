from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np

def plot_demograph_rotated(cell_lengths, normalized_average_mesh_intensity, title='Demograph Plot', cmap='rainbow', cbar_title='YijD-msfGFP Normalized Intensity'):
    # Sort DataFrame by 'cell_lengths' in descending order
    sorted_indices = np.argsort(cell_lengths)[1::]
    sorted_lengths = cell_lengths[sorted_indices]
    sorted_intensities = normalized_average_mesh_intensity[sorted_indices]

    # Find the maximum length of the arrays
    max_length = max(len(arr) for arr in sorted_intensities)

    # Interpolate missing values for shorter arrays
    interpolated_arrays = []
    for array in sorted_intensities:
        x = np.arange(len(array))  # x-coordinates for the existing intensity values
        f = interp1d(x, array, kind='linear', fill_value='extrapolate')  # Interpolation function
        interpolated_array = f(np.linspace(0, len(array), max_length))  # Interpolated array
        interpolated_arrays.append(interpolated_array)
    stacked_demograph = np.vstack(interpolated_arrays)

    fig1 = plt.figure(figsize=(10, 8))  # Adjust figure size as needed

    ax = plt.subplot(111)
    image = ax.imshow(stacked_demograph.T, aspect='auto', cmap=cmap)  # Transpose the array
    cbar = plt.colorbar(image)  # Use the image as the mappable object for the colorbar
    cbar.set_label(cbar_title, rotation=90, labelpad=20, fontsize=14)  # Set colorbar label
    cbar.ax.tick_params(labelsize=14)  # Adjust colorbar tick label size

    # Calculate y-axis values and middle index
    y_axis_values = np.linspace(-1, 1, max_length)  # Ensure values are between -1 and 1
    middle_index = len(y_axis_values) // 2

    # Set y-axis ticks and labels
    plt.yticks([-0.5, middle_index, len(y_axis_values)-0.5], [-1, 0, 1])
    plt.xticks([0, len(sorted_lengths) * 0.25, len(sorted_lengths) * 0.5, len(sorted_lengths) * 0.75, len(sorted_lengths)],
               ['0', '25', '50', '75', '100'])
    plt.xlabel('Cell Length Percentile', fontsize=16)
    plt.ylabel('Normalized Distance From Midcell (µm)', fontsize=16)
    
    plt.title(title, fontsize=18)  # Set the plot title

    plt.show()