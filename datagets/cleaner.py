import pandas as pd
from collections import OrderedDict

# constants
_YES = ['Y', 'y', 'yes', 'Yes']
_NO = ['N', 'n', 'no', 'No']
_QUIT = ['q', 'Q', 'quit', 'Quit']

def manual_dataframe_cleaner(dataframe, confirmation="stepwise"):
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
    modified_dataframe : pandas.DataFrame
        The new dataframe containing the modified columns
    chosen_columns : list
        The columns selected from the *original* dataframe
    modified_columns : list
        The new names for the chosen columns
    modified_dtypes : dict
        The new dtypes for the chosen columns


    """

    # check type of `dataframe`
    if not isinstance(dataframe, pd.DataFrame):
        raise AttributeError("The argument of 'dataframe_cleaner' must be a 'pandas.DataFrame'.")

    old_columns = dataframe.columns
    old_dtypes = dataframe.dtypes
    N = len(old_columns)
    N_digits = len(str(N))

    chosen_columns = []

    new_columns = []
    new_dtypes = []

    out_dict = OrderedDict()

    # initizliating
    window_width = 80
    print("Beginning to clean.")
    print("=" * window_width)

    for j in range(N):
        old_name = old_columns[j]
        old_type = old_dtypes[j]
        confirmed = False

        # print separator
        if j != 0:
            print("=" * window_width)

        # print column information
        print("Column {0:{width}} of {1:{width}}".format(j+1, N, width=N_digits))
        print("-" * (11 + 2*N_digits))
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
            # mark as chosen
            chosen_columns.append(old_name)

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
            break

    # compile the output
    modified_dataframe = pd.DataFrame(out_dict)
    modified_columns = [col for col in new_columns if col is not None]
    modified_dtypes_list = [dtype for dtype in new_dtypes if dtype is not None]
    modified_dtypes = dict(zip(modified_columns, modified_dtypes_list))

    out = (modified_dataframe, chosen_columns, modified_columns, modified_dtypes)

    # run through ending confirmation if called
    if confirmation == 'end':
        print("=" * window_width)

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
            print("=" * window_width)
            print("Cleaning completed.")
            return out
        else:
            raise Exception("Incorrect input!  Try again.")

    print("=" * window_width)
    print("Cleaning completed.")
    return out
