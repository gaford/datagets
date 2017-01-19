import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

class ClassifierEvaluator():
    """
    A class for evaluating the performance of a (binary) classification model.

    Parameters
    ----------
    measurements : list
        A list (or appropriate iterable) of the actual class measurements
    predictions : str
        A list (or appropriate iterable) of the classifier's predictions
    pos_label : str or int, optional
        The label for the "positive" class in the classification problem
    title : str, optional
        The title of the classifier being evaluated

    Attributes
    ----------
    title: str
        The title of the classifier being evaluated
    measurements : numpy.array
        A NumPy array of the actual class measurements
    predictions : numpy.array
        A NumPy array of the classifier's predictions
    pos_label : str or int
        The label for the "positive" class in the classification problem
    fpr : numpy.array
        A NumPy array of the false positive rates for each threshold in self.threshold
    tpr : numpy.array
        A NumPy array of the true positive rates for each threshold in self.threshold
    thresholds : numpy.array
        A NumPy array of the thresholds for positive/negative classification
    auc : float
        The area under the receiver operating characteristic curve (0. <= auc <= 1.)

    """

    def __init__(self, measurements, predictions, pos_label=1, title=None):

        # check that measured values and predicted values are arrays of the same length
        if len(measurements) != len(predictions):
            raise AttributeError("The lengths of the measurement and prediction arrays do not agree.")

        # set title
        if type(title) == str:
            self.title = title
        elif title:
            raise AttributeError("The title of a ClassifierEvaluator must be a string.")
        else:
            self.title = None

        # assign internal attributes
        self.measurements = np.array(measurements)
        self.predictions = np.array(predictions)
        self.pos_label = pos_label

        # compute false positive rate, true positive rate, and thresholds
        self.fpr, self.tpr, self.thresholds = metrics.roc_curve(measurements, predictions, pos_label=pos_label)

        # compute the area under the ROC curve
        self.auc = metrics.auc(self.fpr, self.tpr)

    def roc_plot(self):
        """
        A method for plotting the receiver operating characteristic (ROC) curve for the chosen
        binary classifier.

        Parameters
        ----------
        None

        Returns
        -------
        None

        """

        # establish figure
        plt.figure()

        # set axes' limits and labels
        plt.xlim([-0.05, 1.05])
        plt.ylim([-0.05, 1.05])
        plt.xlabel("False positive rate")
        plt.ylabel("True positive rate")

        # set the title if it has been specified
        if self.title:
            plt.title("Receiver operating characteristic:  {0}".format(self.title))
        else:
            plt.title("Receiver operating characteristic")

        # build the plot
        plt.plot(self.fpr, self.tpr, color='gold', lw=2, label='ROC curve (area = {0})'.format(self.auc))
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.legend(loc='lower right')

        # show the plot
        plt.show()
