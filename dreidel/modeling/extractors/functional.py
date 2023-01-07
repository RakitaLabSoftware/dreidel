from typing import Callable

import scipy

__all__ = ["ext_min", "ext_max", "ext_avg", "ext_fft_peak"]

ExtractorType = Callable[[list[float]], float]


def ext_min(data: list[list[float]]) -> float:
    return min(data[1])


def ext_max(data: list[list[float]]) -> float:
    return max(data[1])


def ext_avg(data: list[list[float]]) -> float:
    return sum(data[1]) / len(data[1])


def ext_fft_peak(data: list[list[float]], *, peak: int = 0) -> float:
    """
    Extract First FFT (FastFourierTransformPeak)

    Parameters
    ----------
    data : list[float]
        list
    peak : int, optional
        _description_, by default 0

    Returns
    -------
    float
        _description_
    """
    transformed = scipy.fft(data[0])
    peaks = scipy.signal.find_peak(transformed[0])
    return peaks[peak]


def largest_distance(data: list[list[float]], *, y_val: float = 0.0) -> float:
    """_summary_

    Parameters
    ----------
    data : list[list[float]]
        _description_
    y_val : float, optional
        _description_, by default 0.0

    Returns
    -------
    float
        _description_
    """
    x_val_list = [x for x, y in zip(data[0], data[1]) if y == y_val]
    largest = 0.0
    for i in range(1, len(x_val_list)):
        current = x_val_list[i + 1] - x_val_list[i]
        if largest < current:
            largest = current
    return largest
