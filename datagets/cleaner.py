import pandas as pd
from collections import OrderedDict

# constants
_YES = ['Y', 'y', 'yes', 'Yes']
_NO = ['N', 'n', 'no', 'No']
_QUIT = ['q', 'Q', 'quit', 'Quit']

def dataframe_cleaner(dataframe, confirmation="stepwise"):
    """
    A method for selecting, retyping, and renaming the columns of a pandas dataframe.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        The input (raw) dataframe
    confirm : None or "none" or "stepwise" or "end", optional
        The type of user confirmation desired in the cleaning process

    Returns
    -------
    pandas.DataFrame
        The new dataframe

    """

    # check type of `dataframe`
    if not isinstance(dataframe, pd.DataFrame):
        raise AttributeError("The argument of 'dataframe_cleaner' must be a 'pandas.DataFrame'.")

    old_columns = dataframe.columns
    old_dtypes = dataframe.dtypes
    N = len(old_columns)

    new_columns = []
    new_dtypes = []

    out_dict = OrderedDict()

    for j in range(N):
        old_name = old_columns[j]
        old_type = old_dtypes[j]
        confirmed = False

        # print separator
        if j != 0:
            print("-" * 80)

        # print column information
        print("Column {0} of {1}".format(j+1, N))
        print("Column name:  {0}".format(old_name))
        print("Column type:  {0}".format(old_type))

        valid = False
        while not valid:
            # determine if column is to be kept
            keep = input("Keep column? [Y/n/q]  ")

            # mark valid input
            if keep in _YES + _NO + _QUIT + ['']:
                print()
                valid = True

            else:
                print("Invalid input:  {0}".format(keep))

        if keep in _YES + ['']:

            # establish confirmation loop
            while not confirmed:

                # choose new attributes
                new_name = input("New column name (press enter to keep name):  ")
                if new_name == '':
                    new_name = old_name

                valid = False
                while not valid:
                    new_type = input("New column type (press enter to keep type):  ")

                    if new_type == '':
                        new_type = old_type

                    try:
                         new_series = dataframe[old_name].astype(new_type)
                         valid = True
                    except TypeError:
                        print("Invalid type:  {0}".format(new_type))
                    except ValueError:
                        print("Column cannot be recast as selected type:  {0}".format(new_type))

                if confirmation == 'stepwise':
                    print()
                    print("Column name:  {0} --> {1}".format(old_name, new_name))
                    print("Column type:  {0} --> {1}".format(old_type, new_type))

                    valid = False
                    while not valid:
                        correct = input("Is this correct? [Y/n]  ")

                        if correct in _YES + _NO + ['']:
                            valid = True
                        else:
                            print("Invalid input:  {0}".format(correct))

                    if correct in _YES + ['']:
                        confirmed = True
                    else:
                        confirmed = False

                # if no stepwise confirmation is desired
                else:
                    confirmed = True

            # add modified column to output
            out_dict[new_name] = new_series

            # mark column as kept
            new_columns.append(new_name)
            new_dtypes.append(new_type)

        elif keep in _NO:
            # mark column as dropped
            new_columns.append(None)
            new_dtypes.append(None)

            print("Discarding column.")
            continue

        elif keep in _QUIT:
            # mark remaining columns as dropped
            remainder = [None] * (N - j)
            new_columns.extend(remainder)
            new_dtypes.extend(remainder)

            print("Quitting cleaning process.")
            print()
            break

    if confirmation == 'end':
        print("-" * 80)

        for j in range(N):
            if new_columns[j]:
                print("Column {0}:  ({1}, {2}) --> ({3}, {4})".format(j,\
                    old_columns[j], old_dtypes[j], new_columns[j], new_dtypes[j]))
            else:
                print("Column {0}:  Dropped".format(j))

        print()

        valid = False
        while not valid:
            correct = input("Is this correct? [Y/n]  ")

            if correct in _YES + _NO + ['']:
                valid = True
            else:
                print("Invalid input:  {0}".format(correct))

        if correct in _YES + ['']:
            return pd.DataFrame(out_dict)
        else:
            raise Exception("Failed input!  Try again.")

    return pd.DataFrame(out_dict)



