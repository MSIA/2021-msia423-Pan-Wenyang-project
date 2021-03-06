import logging
from typing import Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

logger = logging.getLogger(__name__)


def get_a_mod_list_and_dict(df: pd.DataFrame,
                            cluster_range: List,
                            seed: int = 10) -> Tuple:
    """Fit multiple KMeans model and store them in both a list and a dictionary

    Args:
        df (pd.DataFrame): the preprocessed and standardized dataframe
        cluster_range (List): the range of cluster we will try to fit
        seed (int, optional): the random state for the KMeans model. Defaults to 10.

    Returns:
        Tuple: a tuple with two elements: 
            mod_dict - a dictionary where each key is a str of the number of clusters, the value is the fitted value
            mod_list - a list of fitted models
    """
    if (np.abs(df.select_dtypes('number').max().values > 10)).any():
        logger.warning('Values larger than 10 appear to be too large. Did you standardize the data?')
    mod_dict = {}
    for k in cluster_range:
        mod = KMeans(n_clusters=k, random_state=seed).fit(df)
        mod_dict[str(k)] = mod
    mod_list = list(mod_dict.values())
    return mod_dict, mod_list


def cluster_selection_plot(df: pd.DataFrame,
                           mod_list: List,
                           cluster_range: List,
                           output_path: str) -> None:
    """Make and save inertia and silhouette plot

    Args:
        df (pd.DataFrame): the preprocessed and standardized dataframe
        mod_list (List): a list of fitted KMeans model
        cluster_range (List): the range of cluster including in the list of fitted model
        output_path (str): the path to save the cluster selection plots
    """
    within_ss = [i.inertia_ for i in mod_list]
    silhouette_list = [silhouette_score(df, i.labels_) for i in mod_list]

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))
    axs[0].plot(cluster_range, within_ss, color='royalblue')
    axs[1].plot(cluster_range, silhouette_list, color='green')

    # Format x and y label in the plot
    for i in range(2):
        axs[i].set_xlabel('number of clusters')
    for idx, name in zip([0, 1, 2], ['inertia', 'silhouette score']):
        axs[idx].set_ylabel(name)

    fig.savefig(output_path)
    logger.info('The figure is saved to %s', output_path)


def save_model(model_dict: Dict, best_num: int, output_path: str) -> None:
    """Save a KMeans model with selected number of clusters to output path

    Args:
        model_dict (Dict): a dictionary that stores KMeans model where the key represents the number of clusters
        best_num (int): the selected number of cluster for Kmeans
        output_path (str): the place to store the model 
    """
    joblib.dump(model_dict[best_num], output_path)
    logger.info('The model is saved to %s', output_path)
