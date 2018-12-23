import math
import time


def load_data(filename):
    features = []
    file = open(filename, "r")
    for line in file:
        split = line.split()
        temp = []
        for line in split:
            temp.append(float(line))
        features.append(temp)
    return features


def distance(a, b, current_features, k):
    distance = 0

    for feature in current_features:
        x = float((b[feature] - a[feature]) ** 2)
        distance += x

    distance += ((b[k] - a[k]) ** 2)

    return float(math.sqrt(distance))


def distance_2(a, b, current_features):
    distance = 0

    for feature in current_features:
        x = float((b[feature] - a[feature]) ** 2)
        distance += x

    return float(math.sqrt(distance))


def leave_one_out_cross_validation(data, feature_set, k, option):
    correct = 0
    """
    Run a single instance with the rest of the data set and calculate accuracy by checking if the class of the instance is
    equal to the instance class of the shortest distance. calculating the average by # correct/ total instances
    """
    for x in data:
        min_dist = 1000
        for y in data:
            if x != y:
                if option == 1:
                    dist = distance(x, y, feature_set, k)
                else:
                    dist = distance_2(x, y, feature_set)
                if dist < min_dist:
                    min_dist = dist
                    class_a = x[0]
                    class_b = y[0]
        if class_a == class_b:
            correct += 1
    accuracy = (correct / len(data))

    return accuracy


def leave_one_out_cross_validation_custom(data, feature_set, k, option):
    correct = 0
    incorrect = 0
    counter = 0
    """
    Run a single instance with the rest of the data set and calculate accuracy by checking if the class of the instance is
    equal to the instance class of the shortest distance. calculating the average by # correct/ total instances
    """
    for x in data:
        min_dist = 1000
        counter += 1
        for y in data:
            if x != y:
                if option == 1:
                    dist = distance(x, y, feature_set, k)
                else:
                    dist = distance_2(x, y, feature_set)
                if dist < min_dist:
                    min_dist = dist
                    class_a = x[0]
                    class_b = y[0]
        if class_a == class_b:
            correct += 1

        if correct/counter < .80:
            break

    accuracy = (correct / len(data))

    return accuracy


def Forward_selection(data):
    """
    Algorithm will search down a tree starting with 0 features and combine
    x amount of features that will produce the best accuracy

    :param data: data set with y instances and x features
    :return: Best set of features with highest rate of accuracy
    """
    current_set_of_features = set()
    best_so_far_accuracy = 0

    for i in range(len(data[0]) - 1):
        print("On level " + str(i + 1) + " of the search tree")
        feature_to_add_at_this_level = 1000
        for k in range(1, len(data[0])):
            if k not in current_set_of_features:
                accuracy = leave_one_out_cross_validation(data, current_set_of_features, k, 1)
                print("Consider adding feature " + str(k) + " with accuracy " + str(accuracy))
                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    feature_to_add_at_this_level = k
        if feature_to_add_at_this_level != 1000:
            current_set_of_features.add(feature_to_add_at_this_level)
            temp = []
            for feature in current_set_of_features:
                temp.append(feature)
            current_feature = temp[i]
            print("-- On level " + str(i + 1) + " added feature " + str(current_feature) + " to current set")
            print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
        else:
            print(" Warning, Accuracy has decreased ! CONTINUING SEARCH in case of local maxima")
            #break

    print("Best set of features to use: ", current_set_of_features, "with accuracy", best_so_far_accuracy)
    return current_set_of_features


def Backward_elimination(data):
    """
    Algorithm that starts with entire feature set and calculates best accuracy by
    process of removing features down a tree.

    :param data: data set with y instances and x features
    :return: Best set of features with highest rate of accuracy
    """
    current_set_of_features = set()
    total_accuracy = 0
    for x in range(1, len(data[0])):  # initalizing set with all features
        current_set_of_features.add(x)

    for i in range(len(data[0])):
        print("On level " + str(i + 1) + " of the search tree")
        feature_to_remove = 1000
        best_so_far_accuracy = 0
        for k in range(1, (len(data[0]))):
            if k in current_set_of_features:
                temp_set = current_set_of_features.copy()
                temp_set.remove(k)
                accuracy = leave_one_out_cross_validation(data, temp_set, k, 2)
                print("Consider removing feature " + str(k) + " with accuracy " + str(accuracy))
                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    feature_to_remove = k
        if feature_to_remove != 1000:
            current_set_of_features.remove(feature_to_remove)
            print("-- On level " + str(i + 1) + " removed feature " + str(feature_to_remove) + " from current set")
            print("* * * * * * * * * * * * * * * * * * * * * * * * * * * *  \n")

        if best_so_far_accuracy > total_accuracy:
            total_accuracy = best_so_far_accuracy
            current_best = current_set_of_features.copy()
        elif best_so_far_accuracy < total_accuracy:
            print(" Warning, Accuracy has decreased ! CONTINUING SEARCH in case of local maxima")
    print("\n\n")
    print("Best set of features to use:", current_best, "with accuracy", total_accuracy)

    return current_best


def third_algorithm(data):
    current_set_of_features = set()
    best_so_far_accuracy = 0

    for i in range(len(data[0]) - 1):
        print("On level " + str(i + 1) + " of the search tree")
        feature_to_add_at_this_level = 1000
        for k in range(1, len(data[0])):
            if k not in current_set_of_features:
                accuracy = leave_one_out_cross_validation_custom(data, current_set_of_features, k, 1)
                print("Consider adding feature " + str(k) + " with accuracy " + str(accuracy))
                if accuracy > best_so_far_accuracy:
                    best_so_far_accuracy = accuracy
                    feature_to_add_at_this_level = k
        if feature_to_add_at_this_level != 1000:
            current_set_of_features.add(feature_to_add_at_this_level)
            temp = []
            for feature in current_set_of_features:
                temp.append(feature)
            current_feature = temp[i]
            print("-- On level " + str(i + 1) + " added feature " + str(current_feature) + " to current set")
            print("* * * * * * * * * * * * * * * * * * * * * * * * * * * * ")
        else:
            print(" Warning, Accuracy has decreased ! CONTINUING SEARCH in case of local maxima")
            # break

    print("Best set of features to use: ", current_set_of_features, "with accuracy", best_so_far_accuracy)
    return current_set_of_features


def main():
    filename = 'CS170_LARGEtestdata__87.txt'
    data = load_data(filename)

    t0 = time.time()
    search = Backward_elimination(data)
    print(search)
    t1 = time.time()
    total_time = t1 - t0
    print("seconds" + str(total_time))
    print("minutes" + str(total_time / 60))
"""
    t0 = time.time()
    search = Backward_selection(data)
    print(search)
    t1 = time.time()
    total_time = t1 - t0
    print("seconds" + str(total_time))
    print("minutes" + str(total_time / 60))

    t0 = time.time()
    search = third_algorithm(data)
    print(search)
    t1 = time.time()
    total_time = t1 - t0
    print("seconds" + str(total_time))
    print("minutes" + str(total_time / 60))
"""

if __name__ == '__main__':
    main()
