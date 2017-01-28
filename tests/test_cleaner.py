from collections import OrderedDict
import pandas as pd
import pandas.util.testing as pdt
import numpy as np


from context import datagets

def test_manual_dataframe_cleaner(monkeypatch):
    """
    Tests the 'datagets.manual_dataframe_cleaner' method.
    """

    # set up mock user inputs
    inputs = open('./test_cleaner_inputs.txt')

    def next_input(x):
        return inputs.readline().rstrip('\n')

    monkeypatch.setattr('builtins.input', next_input)

    # set up sample dataframe
    s1 = [0, 1, 2, 3, 4, 5]
    s2 = ['A', 'B', 'C', 'D', 'E', 'F']
    s3 = [0., 0.2, 0.4, 0.6, 0.8, 1.0]

    df_dict = OrderedDict([
        ("integers", s1),
        ("letters", s2),
        ("floats", s3)
    ])

    df = pd.DataFrame(df_dict)

    # set up desired output dataframe
    df2_dict = OrderedDict([
        ("AAA", s1),
        ("BBB", s3)
    ])

    df2 = pd.DataFrame(df2_dict)
    df2.AAA = df2.AAA.astype('float64')
    df2.BBB = df2.BBB.astype('object')

    # run modification process and check equality
    df2t, old, new, dtypes = datagets.manual_dataframe_cleaner(df)

    pdt.assert_frame_equal(df2t, df2)
    assert old == ["integers", "floats"]
    assert new == ["AAA", "BBB"]
    assert dtypes == {"AAA": "float64", "BBB": "object"}

    # cleanup
    inputs.close()
