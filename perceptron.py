import math

import data

# HW3 Perceptron
# Name: Roberto J. Nares
# Perm: 9727702
# E-mail: rjnares@ucsb.edu

def dot_kf(u, v):
    """
    The basic dot product kernel returns u*v+1.

    Args:
        u: list of numbers
        v: list of numbers

    Returns:
        dot(u,v) + 1
    """
    # TODO
    result = 0.0
    if len(u) == len(v):
        for i in range(len(u)):
            result += u[i] * v[i]
        result += 1.0
    return result

def poly_kernel(d):
    """
    The polynomial kernel.

    Args:
        d: a number

    Returns:
        A function that takes two vectors u and v,
        and returns (u*v+1)^d.
    """
    def kf(u, v):
        # TODO: implement the kernel function
        return pow(dot_kf(u, v), d)
    return kf

def exp_kernel(s):
    """
    The exponential kernel.

    Args:
        s: a number

    Returns:
        A function that takes two vectors u and v,
        and returns exp(-||u-v||/(2*s^2))
    """
    def kf(u, v):
        # TODO: implement the kernel function
        euclidean_dist = 0
        for i in range(len(u)):
            euclidean_dist += pow(u[i] - v[i], 2)
        euclidean_dist = math.sqrt(euclidean_dist)
        return math.exp(-euclidean_dist/(2.0 * pow(s, 2)))
    return kf

class Perceptron(object):

    def __init__(self, kf):
        """
        Args:
            kf - a kernel function that takes in two vectors and returns
            a single number.
        """
        self.kf = kf
        self.wrong_data = []
        self.wrong_labs = []
        # TODO: add more fields as needed

    def update(self, point, label):
        """
        Updates the parameters of the perceptron, given a point and a label.

        Args:
            point: a list of numbers
            label: either 1 or -1

        Returns:
            True if there is an update (prediction is wrong),
            False otherwise (prediction is accurate).
        """
        # TODO
        return self.predict(point) != label

    def predict(self, point):
        """
        Given a point, predicts the label of that point (1 or -1).
        """
        # TODO
        prediction = 0
        for i in range(len(self.wrong_data)):
            prediction += self.wrong_labs[i] * self.kf(self.wrong_data[i], point)
        if prediction <= 0:
            return -1
        else:
            return 1

# Feel free to add any helper functions as needed.


if __name__ == '__main__':
    val_data, val_labs = data.load_data('data/validation.csv')
    test_data, test_labs = data.load_data('data/test.csv')
    # TODO: implement code for running the problems

    # RUN DOT PRODUCT KERNEL FUNCTION
    print("--- Validation Set: Avg. Loss of Dot Product Perceptron Every 100 Steps ---")
    dp_perceptron = Perceptron(dot_kf)
    for i in range(len(val_data)):
        if dp_perceptron.update(val_data[i], val_labs[i]):
            dp_perceptron.wrong_data.append(val_data[i])
            dp_perceptron.wrong_labs.append(val_labs[i])
        if ((i + 1) % 100) == 0:
            print("Step " + str(i + 1) + ": " + str(len(dp_perceptron.wrong_data)/float(i + 1)))

    
    # RUN POLYNOMIAL KERNEL FUNCTION
    print("--- Validation Set: Avg. Loss of Polynomial Perceptron At 1000 Steps ---")
    degree = [1, 3, 5, 7, 10, 15, 20]
    for d in degree:
        poly_perceptron = Perceptron(poly_kernel(d))
        for i in range(len(val_data)):
            if poly_perceptron.update(val_data[i], val_labs[i]):
                poly_perceptron.wrong_data.append(val_data[i])
                poly_perceptron.wrong_labs.append(val_labs[i])
            if (i + 1) == 1000:
                print("Degree " + str(d) + ": " + str(len(poly_perceptron.wrong_data)/float(i + 1)))

    # RUN EXPONENTIAL KERNEL FUNCTION VS POLYNOMIAL KERNEL FUNCTION WITH DEGREE = 5
    print("--- Test Set: Avg. Loss of Polynomial Perceptron For Degree = 5, Every 100 Steps ---")
    poly_perceptron = Perceptron(poly_kernel(5))
    for i in range(len(test_data)):
        if poly_perceptron.update(test_data[i], test_labs[i]):
            poly_perceptron.wrong_data.append(test_data[i])
            poly_perceptron.wrong_labs.append(test_labs[i])
        if ((i + 1) % 100) == 0:
            print("Step " + str(i + 1) + ": " + str(len(poly_perceptron.wrong_data)/float(i + 1)))
    
    print("--- Test Set: Avg. Loss of Exponential Perceptron For Sigma = 10, Every 100 Steps ---")
    exp_perceptron = Perceptron(exp_kernel(10))
    for i in range(len(test_data)):
        if exp_perceptron.update(test_data[i], test_labs[i]):
            exp_perceptron.wrong_data.append(test_data[i])
            exp_perceptron.wrong_labs.append(test_labs[i])
        if ((i + 1) % 100) == 0:
            print("Step " + str(i + 1) + ": " + str(len(exp_perceptron.wrong_data)/float(i + 1)))


        


    


    
    




