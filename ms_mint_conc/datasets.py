import pandas as pd
from .calibration_curves import calibration_curves, calibration_curves_variable_slope


def make_curve():
    curve = pd.DataFrame(columns={'peak_label'})
    curve.peak_label = ['M1','M2','M3','M4']
    curve['10nm'] = [10., 20., 50., 5.]
    curve['100nm'] = 10*curve['10nm']
    curve['1000nm'] = 100*curve['10nm']
    curve['10000nm'] = 1000*curve['10nm']
    curve['100000nm'] = 10000*curve['10nm']
    curve['1000000nm'] = 100000*curve['10nm']
    curve['10000000nm'] = 1000000*curve['10nm']
    curve.at[0, '10000000nm'] /= 20.
    curve.at[1, '10nm'] *= 20.
    curve.at[1, '100nm'] /= 5.
    curve.at[2, '10nm'] *=5.
    curve.at[2, '10000000nm'] /=5.
    return curve


def make_calibration_data():
    curve = make_curve()

    curve_long = curve.melt(id_vars='peak_label', var_name='Conc', value_name='value')
    curve_long['Conc'] = curve_long.Conc.apply(lambda x: float( x.replace('nm', '')) )

    X_train = curve_long[['peak_label', 'value']]
    y_train = curve_long['Conc']

    cc = calibration_curves(X_train, y_train)
    return X_train, y_train, cc


def make_calibration_data_variable_slope():
    curve = make_curve()

    curve_long = curve.melt(id_vars='peak_label', var_name='Conc', value_name='value')
    curve_long['Conc'] = curve_long.Conc.apply(lambda x: float( x.replace('nm', '')) )

    X_train = curve_long[['peak_label', 'value']]
    y_train = curve_long['Conc']

    cc = calibration_curves_variable_slope(X_train, y_train)
    return X_train, y_train, cc