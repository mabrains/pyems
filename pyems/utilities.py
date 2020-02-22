import sys
from bisect import bisect_left
from typing import List
import numpy as np
from CSXCAD.CSXCAD import ContinuousStructure


# TODO should set max precision instead of precision list. Precision
# should be computed automatically based on the last digit that
# differs between each value.
def pretty_print(
    data: np.array, col_names: List[str], prec: List[int], out_file=sys.stdout,
) -> None:
    """
    Data is multidimensional list, where each inner list corresponds
    to a column.
    """
    extra_space = 3
    data = np.array(data)
    col_widths = [
        int(
            _val_digits(np.amax(np.absolute(data[col])))
            + prec[col]
            + 2
            + extra_space
        )
        for col in range(len(col_names))
    ]
    for i, col in enumerate(col_names):
        out_file.write("{:{width}}".format(col, width=col_widths[i]))
    out_file.write("\n")

    data = data.T
    for row in data:
        for i, val in enumerate(row):
            out_file.write(
                "{:<{width}.{prec}f}".format(
                    val, width=col_widths[i], prec=prec[i]
                )
            )
        out_file.write("\n")


def _val_digits(val: float) -> int:
    """
    Compute the number of decimal digits needed to display the
    integral portion of a value.
    """
    # assume negative for simplicity
    extra_digits = 2

    if val < 10:
        return extra_digits + 1

    return int(np.log10(val)) + extra_digits


def array_index(val, arr) -> int:
    """
    Return the index of the closest array value to a given value.

    :param val: The value for which the closest index is desired.
    :param arr: The array from which the index is computed.

    :returns: The array index whose corresponding value is nearest the
              given value.
    """
    lbound_idx = bisect_left(arr, val)
    lbound = arr[lbound_idx]
    if lbound_idx == len(arr):
        return lbound_idx

    ubound_idx = lbound_idx + 1
    ubound = arr[ubound_idx]

    if val - lbound < ubound - val:
        return lbound_idx
    else:
        return ubound_idx


def float_cmp(a: float, b: float, tol: float) -> bool:
    """
    Return true if floats are equal to within a specified tolerance of
    each other.  This avoids erroneous errors due to finite numeric
    precision.

    :param a: first float.
    :param b: second float.
    :param tol: max acceptable value difference.

    :returns: True if within the specified tolerance, false otherwise.
    """
    if abs(a - b) <= tol:
        return True
    return False


def sort_table_by_col(arr: np.array, col: int = 0):
    """
    Sort a 2D numpy array in ascending order by column index.
    """
    return arr[np.argsort(arr[:, col])]


def table_insertion_idx(val, arr: np.array, col: int = 0):
    """
    Find the insertion index of a value for a sorted 2D numpy array.
    """
    return np.searchsorted(arr[:, col], val)


def interp_lin(xval, xlow, xhigh, ylow, yhigh):
    """
    Get the linear-interpolated y-value for a given x-value between x
    bounds.

    :param xval: The x-value for which you want the y-value.
    :param xlow: The lower-bound x-value.
    :param xhigh: The upper-bound x-value.
    :param ylow: The lower-bound y-value.
    :param yhigh: The upper-bound y-value.
    """
    if xval < xlow or xval > xhigh:
        raise ValueError("xval must be between xlow and xhigh")

    dy = (yhigh - ylow) / (xhigh - xlow)
    dx = xval - xlow
    return ylow + (dy * dx)


def table_interp_val(
    arr: np.array, target_col, sel_val, sel_col: int = 0, permit_outside=False
):
    """
    Get the interpolated column value in a table.

    :param arr: The sorted 2D numpy array.
    :param target_col: Column corresponding to the desired return
        value.
    :param sel_val: Value of the selection column for the desired
        target column.
    :param sel_col: Column index of the selection column.
    :param permit_outside: If True, return lower or upper bound value
        if sel_val is outside table bounds.
    """
    if permit_outside:
        if sel_val < arr[0][sel_col]:
            return arr[0][target_col]
        if sel_val > arr[-1][sel_col]:
            return arr[-1][target_col]

    if sel_val == arr[0][sel_col]:
        return arr[0][target_col]
    if sel_val == arr[-1][sel_col]:
        return arr[-1][sel_val]

    ins_idx = table_insertion_idx(sel_val, arr, sel_col)
    xlow = arr[ins_idx - 1][sel_col]
    xhigh = arr[ins_idx][sel_col]
    ylow = arr[ins_idx - 1][target_col]
    yhigh = arr[ins_idx][target_col]

    return interp_lin(sel_val, xlow, xhigh, ylow, yhigh)


def max_priority() -> int:
    """
    Priority that won't be overriden.

    :returns: highest priority.
    """
    return 999


def speed_of_light(unit: float) -> float:
    """
    """
    return 299792458 / unit


def wavelength(freq: np.array, unit: float) -> np.array:
    """
    Calculate the wavelength for a given frequency of light.  This
    presently assumes that the light is travelling through a vacuum.
    """
    return speed_of_light(unit) / freq


def wavenumber(freq: np.array, unit: float) -> np.array:
    """
    Calculate the wavenumber for a given frequency of light.  Assumes
    light is travelling through a vacuum.
    """
    return np.array(2 * np.pi / wavelength(freq, unit))


def get_unit(csx: ContinuousStructure) -> float:
    """
    """
    return csx.GetGrid().GetDeltaUnit()
