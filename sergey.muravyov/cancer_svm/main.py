##import util
##from math import log
from sklearn import svm


import numpy as np
from urllib.request import urlopen

def get_data(flag = False):
    file = urlopen("http://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data")
    x, y = [], []
    for line in file.readlines():
        field = line.decode('utf-8').strip().split(',')
        y.append(1 if field[1] == 'M' else 0)
        
        num = [float(i) for i in field[2:]]
        num.insert(0, 1.0)
        if not flag:
            num = np.array(num)
        x.append(num)
    file.close()
    return x, y

def best_regularization(xs, ys, parts=5):
    splitted_data = list(split(unzip(xs, ys), parts))

    best_C, best_error = None, None

    for deg in range(10):
        # C is a regularization constant
        C = 0.1**deg
        errors = []
        for i in range(parts):
            test_data = splitted_data[i]
            train_data = append(splitted_data[:i] + splitted_data[i+1:])

            xs, ys = zip(*train_data)
            model = svm.LinearSVC(C=C)
            model.fit(xs, ys)

            curr_error = 0.0
            xs, ys = zip(*test_data)
            predictions = model.predict(xs)
            for y, y_pred in zip(ys, predictions):
                if y != y_pred:
                    curr_error += 1
            errors.append(curr_error / len(test_data))

        curr_error = average(errors)
        if best_C is None or best_error > curr_error:
            best_error = curr_error
            best_C = C

    return best_C

def main(test_fraction=0.1):
    xs, ys = get_data(flag = True)

    test_size = int(len(xs) * test_fraction)

    train_xs = xs[:-test_size]
    train_ys = ys[:-test_size]
    C = best_regularization(train_xs, train_ys)
    model = svm.LinearSVC(C=C)
    model.fit(train_xs, train_ys)

    errors = 0
    for x, x_pred in zip(list(ys[-test_size:]), list(model.predict(xs[-test_size:]))):
        if x != x_pred:
            errors += 1
    print("error on test set: %6.2f%%" % (100 * errors / test_size))
    print("regularization constant is 1e-%d" % round(log(C, 0.1)))

if __name__ == "__main__":
    main()


