from os import mkdir, path

from matplotlib import pyplot as plt

import numpy as np

from County import County


def _get_datasets(county, dataset_names):
    datasets = []
    dataset_labels = []
    if 'cases' in dataset_names:
        datasets.append(county.cases)
        dataset_labels.append('Cases')
    if 'deaths' in dataset_names:
        datasets.append(county.deaths)
        dataset_labels.append('Deaths')
    if 'new' in dataset_names:
        datasets.append(county.new_per_day)
        dataset_labels.append('New Cases')
    return county.dates, datasets, dataset_labels


def generate_plot(county, datasets):
    colors = ['black', 'red', 'blue', 'green', 'orange', 'purple']

    dates, datasets, dataset_labels = _get_datasets(county, datasets)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    # Iterate through different datasets
    for i in range(len(datasets)):
        data = np.array(datasets[i])
        datanew = np.zeros_like(data)
        if dataset_labels[i] == 'New Cases':
            for j, val in enumerate(data):
                datanew[j] = np.sum(data[(j-14):j])
                dataset_labels[i] = 'Active Cases'
            data = datanew
            ax1.plot(dates, data, c=colors[i], label=dataset_labels[i], linestyle='-')

    plt.xticks([dates[i] for i in range(0, len(dates), len(dates) // 4)])
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.title(county.name.capitalize() + ' County')

    if not path.exists('images'):
        mkdir('images')

    filepath = f'images/{county.name}_{dates[-1]}.png'
    plt.savefig(filepath)
    return filepath
