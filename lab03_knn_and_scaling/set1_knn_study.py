# first run knn on sample of unbalanced and unscaled database
# make sample

# change sample in percentage here
sample = 0.05

from numpy import ndarray
from pandas import DataFrame, read_csv, unique
from matplotlib.pyplot import figure, savefig, show
from sklearn.neighbors import KNeighborsClassifier
from ds_charts import plot_evaluation_results, multiple_line_chart
from sklearn.metrics import accuracy_score



def KNN(file_tag, filename, s):
    
    target = 'PERSON_INJURY'

    train: DataFrame = read_csv(f'{filename}_train.csv')
    train = train.sample(frac=s, replace=True, random_state=1)
    trnY: ndarray = train.pop(target).values
    trnX: ndarray = train.values
    labels = unique(trnY)
    labels.sort()

    test: DataFrame = read_csv(f'{filename}_test.csv')
    tstY: ndarray = test.pop(target).values
    tstX: ndarray = test.values

    nvalues = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    dist = ['manhattan', 'euclidean', 'chebyshev']
    values = {}
    best = (0, '')
    last_best = 0
    for d in dist:
        yvalues = []
        for n in nvalues:
            knn = KNeighborsClassifier(n_neighbors=n, metric=d)
            knn.fit(trnX, trnY)
            prdY = knn.predict(tstX)
            yvalues.append(accuracy_score(tstY, prdY))
            if yvalues[-1] > last_best:
                best = (n, d)
                last_best = yvalues[-1]
        values[d] = yvalues

    figure()
    multiple_line_chart(nvalues, values, title='KNN variants', xlabel='n', ylabel='accuracy', percentage=True)
    savefig(f'lab03_knn_and_scaling\images\{file_tag}\{file_tag}_knn_study.png')
    show()
    print('Best results with %d neighbors and %s'%(best[0], best[1]))

    clf = knn = KNeighborsClassifier(n_neighbors=best[0], metric=best[1])
    clf.fit(trnX, trnY)
    prd_trn = clf.predict(trnX)
    prd_tst = clf.predict(tstX)
    plot_evaluation_results(labels, trnY, prd_trn, tstY, prd_tst)
    savefig(f'lab03_knn_and_scaling\images\{file_tag}\{file_tag}_knn_best.png')
    show()

# Run KNN for all different codes
KNN('set1', 'lab03_knn_and_scaling\ew_data\set1', sample)
KNN('set1_scaled', 'lab03_knn_and_scaling\ew_data\set1_scaling', sample)