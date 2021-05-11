import joblib
import matplotlib
import numpy as np
import pandas as pd
from effectiveness.classification.plots import go, py
from effectiveness.settings import DATA_DIR
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    brier_score_loss,
    f1_score,
    make_scorer,
    mean_absolute_error,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import (
    GridSearchCV,
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_validate,
    train_test_split,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.utils import shuffle

matplotlib.use('Agg')


def import_frame(*, consider_coverage=True, delimiter="quartile", operator="ALL"):
    """
    Imports all the data needed
    :param consider_coverage: boolean value to take into account or not the coverage
    :return: a tuple with the frame and the metrics
    """

    positive_example: pd.DataFrame = pd.read_csv(DATA_DIR / delimiter / operator / "good.csv")
    negative_example: pd.DataFrame = pd.read_csv(DATA_DIR / delimiter / operator / "bad.csv")
    coverage_index = list(positive_example.columns).index('line_coverage')
    index = coverage_index if consider_coverage else coverage_index + 1
    metrics = positive_example.columns[index::].tolist()
    positive_example['y'] = 1
    negative_example['y'] = 0

    frame = shuffle(pd.concat([positive_example, negative_example]))

    return frame, metrics


def plot_learning_curve(train_sizes, train_scores, test_scores):
    """Plots the learning curve"""
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.figure()
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    plt.fill_between(
        train_sizes,
        train_scores_mean - train_scores_std,
        train_scores_mean + train_scores_std,
        alpha=0.1,
        color="r",
    )
    plt.fill_between(
        train_sizes,
        test_scores_mean - test_scores_std,
        test_scores_mean + test_scores_std,
        alpha=0.1,
        color="g",
    )
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r", label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g", label="Cross-validation score")
    plt.legend(loc="best")
    plt.savefig(DATA_DIR / f'learning_curve_{coverage_suffix}.pdf', bbox_inches='tight')


def get_param_grid(algorithm, metrics):
    """
    Returns the right parameter grid according to the selected algorithm
    :param algorithm: the algorithm to choose
    :param metrics: the list of metrics
    :return: a dictionary with the parameter grid
    """
    svc = {
        'classifier': [SVC(probability=True)],
        'preprocessing': [StandardScaler(), None],
        'classifier__gamma': [0.01, 0.1, 1, 10, 100],
        'classifier__C': [0.01, 0.1, 1, 10, 100],
    }
    rfc = {
        'classifier': [RandomForestClassifier()],
        'preprocessing': [None],
        'classifier__n_estimators': [3 * x for x in range(1, 11)],
        'classifier__max_features': [int((len(metrics) / 10) * x) for x in range(1, 11)],
        'classifier__max_depth': [5 * x for x in range(1, 11)],
        'classifier__min_samples_leaf': [2 * x for x in range(1, 11)],
    }
    knn = {
        'classifier': [KNeighborsClassifier()],
        'preprocessing': [None],
        'classifier__n_neighbors': [x for x in range(1, 15)],
        'classifier__weights': ['uniform', 'distance'],
        'classifier__leaf_size': [5 * x for x in range(1, 11)],
    }
    if algorithm == 'all':
        return [svc, rfc, knn]
    elif algorithm == 'rfc':
        return [rfc]
    elif algorithm == 'svc':
        return [svc]
    elif algorithm == 'knn':
        return [knn]
    elif algorithm == 'test':
        return [
            {
                'classifier': [KNeighborsClassifier()],
                'preprocessing': [None],
                'classifier__n_neighbors': [5],
            },
            {
                'classifier': [RandomForestClassifier()],
                'preprocessing': [None],
                'classifier__n_estimators': [3],
            },
        ]
    else:
        print('Unsupported algorithm selected')
        exit(1)


def classification(
    *,
    consider_coverage=True,
    n_inner=5,
    n_outer=10,
    n_repeats=10,
    algorithm='all',
    delimiter="quartile",
    operator="ALL",
):
    """
    Runs the entire process of classification and evaluation
    :param consider_coverage: to include or not the line coverage as a feature
    :param n_inner: number of folds for the inner cross fold validation
    :param n_outer: number of folds for the outer cross fold validation
    :param algorithm: select the algorithm to run; possible choices are 'svc', 'rfc', 'knn' and 'all'
    Validate and save a ML model
    """
    global X, Y, coverage_suffix

    # the suffix for saving the files
    coverage_suffix = 'dynamic' if consider_coverage else 'static'

    # Import the data
    print('Importing data')
    frame, metrics = import_frame(
        consider_coverage=consider_coverage, delimiter=delimiter, operator=operator
    )
    print(f'Imported {len(frame)} rows with following metrics:')
    for metric in metrics:
        print(" -", metric)

    X = frame[metrics]
    Y = frame['y']
    pipe = Pipeline([('preprocessing', StandardScaler()), ('classifier', SVC())])

    # Set up the algorithms to tune, train and evaluate
    param_grid = get_param_grid(algorithm, metrics)

    inner_cv = StratifiedKFold(n_splits=n_inner, shuffle=True)
    outer_cv = RepeatedStratifiedKFold(n_splits=n_outer, n_repeats=n_repeats)

    # inner cross validation
    grid = GridSearchCV(
        estimator=pipe,
        param_grid=param_grid,
        cv=inner_cv,
        scoring=get_scoring(),
        refit='roc_auc_scorer',
        return_train_score=True,
        verbose=1,
        n_jobs=-1,
    )

    results = cross_validate(
        estimator=grid,
        cv=outer_cv,
        X=X,
        y=Y,
        scoring=get_scoring(),
        return_train_score=True,
        verbose=1,
        n_jobs=-1,
    )

    accuracy = results.get('test_accuracy').mean()
    precision = results.get('test_precision').mean()
    recall = results.get('test_recall').mean()
    f1_score = results.get('test_f1_score').mean()
    roc_auc = results.get('test_roc_auc_scorer').mean()
    mae = results.get('test_mean_absolute_error').mean()
    brier = results.get('test_brier_score').mean()

    # save performance metrics
    metrics_res = pd.DataFrame(
        {
            'accuracy': [accuracy],
            'precision': [precision],
            'recall': [recall],
            'f1_score': [f1_score],
            'ROC-AUC': [roc_auc],
            'MAE': [mae],
            'Brier': [brier],
        }
    )

    print(metrics_res.T)

    metrics_res.to_csv(DATA_DIR / f'evaluation_{coverage_suffix}_{algorithm}.csv', index=False)

    grid.fit(X, Y)
    model = grid.best_params_['classifier']
    print('Best model is:\n', model)
    model_path = DATA_DIR / f'_model_{coverage_suffix}_{algorithm}.txt'
    model_path.write_text(str(model))

    if type(model) is RandomForestClassifier:
        compute_mean_decrease_in_entropy(
            grid=model, n_outer=n_outer, metrics=metrics, algorithm=algorithm
        )

    print('Saving the model on the entire set')
    grid.fit(X, Y)
    joblib.dump(
        grid.best_estimator_,
        DATA_DIR / f'model_{coverage_suffix}_{algorithm}.pkl',
        compress=1,
    )


def compute_features_importance(grid, n_outer, metrics, algorithm):
    """
    Computes and saves the features importance with the Mean Decrease Accuracy approach
    :param grid: the model
    :param n_outer: the number of times to fit the model
    :param metrics: the list of metrics
    :param algorithm: the employed algorithm
    """
    features = [[] for _ in range(len(metrics))]

    for i in range(0, n_outer):
        grid.fit(X, Y)
        model = grid.best_params_['classifier']
        for j, elem in enumerate(model.feature_importances_):
            features[j].append(elem)
    runs = list(range(n_outer))
    features_importance = pd.DataFrame(features, columns=runs, index=metrics)
    features_importance.to_csv(
        DATA_DIR / f'features_importance_{coverage_suffix}_{algorithm}.csv'
    )
    mean = lambda x: sum(x) / len(x)
    features_average = [mean(x) for x in features]
    s = sorted(zip(map(lambda x: round(x, 3), features_average), metrics), reverse=True)


def compute_mean_decrease_in_entropy(grid, n_outer, metrics, algorithm):
    """
    Computes and saves the feature importance computed with the Mean Decrease in Entropy approach
    :param grid: the model
    :param n_outer: the number of times to fit the model
    :param metrics: the list of metrics
    :param algorithm: the employed algorithm
    """
    features = [[] for _ in range(len(metrics))]
    for _ in range(0, n_outer):
        grid.fit(X, Y)
        for j, elem in enumerate(grid.feature_importances_):
            features[j].append(elem)

    runs = list(range(n_outer))
    features_importance = pd.DataFrame(features, columns=runs, index=metrics)
    features_importance.to_csv(
        DATA_DIR / f'features_importance_{coverage_suffix}_{algorithm}.csv'
    )


def plot_roc_curve(estimator, auc):
    """
    Plots the ROC AUC curve of a given estimator
    :param estimator: the estimator
    :param auc: the roc curve
    """

    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, stratify=Y, train_size=0.8, test_size=0.2, shuffle=True
    )
    one_hot_encoder = OneHotEncoder()
    estimator.fit(x_train, y_train)
    one_hot_encoder.fit(estimator.apply(x_train))
    y_predicted = estimator.predict_proba(x_test)[:, 1]
    false_positive, true_positive, _ = roc_curve(y_test, y_predicted)

    lw = 2

    trace1 = go.Scatter(
        x=false_positive,
        y=true_positive,
        mode='lines',
        line=dict(color='darkorange', width=lw),
        name='ROC curve (area = %0.2f)' % auc,
    )

    trace2 = go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        line=dict(color='navy', width=lw, dash='dash'),
        showlegend=False,
    )

    layout = go.Layout(
        xaxis=dict(title='False Positive Rate', color='black'),
        yaxis=dict(title='True Positive Rate', color='black'),
        legend=dict(orientation="h"),
        margin=go.Margin(l=80, r=50, b=50, t=20, pad=10),
    )

    fig = go.Figure(data=[trace1, trace2], layout=layout)
    py.image.save_as(fig, filename=DATA_DIR / f'roc_{coverage_suffix}.pdf')


def get_scoring():
    """Returns the scores to evaluate the model"""
    return dict(
        accuracy=make_scorer(accuracy_score),
        precision=make_scorer(precision_score, zero_division=0),
        recall=make_scorer(recall_score, zero_division=0),
        f1_score=make_scorer(f1_score, zero_division=0),
        roc_auc_scorer=make_scorer(roc_auc_score),
        mean_absolute_error=make_scorer(mean_absolute_error),
        brier_score=make_scorer(brier_score_loss),
    )


if __name__ == '__main__':
    pass
