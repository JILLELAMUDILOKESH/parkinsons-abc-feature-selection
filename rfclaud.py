# import numpy as np
# import pandas as pd
# import random
# import matplotlib.pyplot as plt
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import accuracy_score
# from joblib import Parallel, delayed

# # Load Dataset
# data = pd.read_csv("parkinsons.data")
# data = data.drop(['name'], axis=1)
# X = data.drop(['status'], axis=1)
# y = data['status']

# # Reduced Parameters
# num_runs = 10
# num_bees = 222   # was 200
# max_iterations = 29
# limit = 10

# def run_single(run):
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=0.2, random_state=run
#     )

#     # RF WITHOUT ABC
#     model = RandomForestClassifier(n_estimators=100, random_state=42)
#     model.fit(X_train, y_train)
#     acc_no_abc = accuracy_score(y_test, model.predict(X_test))

#     # Cached evaluation function
#     cache = {}
#     def evaluate_rf(solution):
#         key = tuple(solution)
#         if key in cache:
#             return cache[key]
#         if np.sum(solution) == 0:
#             return 0
#         cols = X.columns[np.where(solution == 1)]
#         m = RandomForestClassifier(n_estimators=100, random_state=42)
#         m.fit(X_train[cols], y_train)
#         acc = accuracy_score(y_test, m.predict(X_test[cols]))
#         cache[key] = acc
#         return acc

#     # ABC init
#     num_features = X.shape[1]
#     population = [np.random.randint(0, 2, num_features) for _ in range(num_bees)]
#     fitness = [evaluate_rf(sol) for sol in population]
#     trial = [0] * num_bees
#     best_solution, best_accuracy = None, 0

#     for iteration in range(max_iterations):
#         # Employed Bees
#         for i in range(num_bees):
#             new_sol = population[i].copy()
#             new_sol[random.randint(0, num_features - 1)] ^= 1
#             new_fit = evaluate_rf(new_sol)
#             if new_fit > fitness[i]:
#                 population[i], fitness[i], trial[i] = new_sol, new_fit, 0
#             else:
#                 trial[i] += 1

#         # Onlooker Bees
#         total = np.sum(fitness)
#         prob = np.array(fitness) / total if total > 0 else np.ones(num_bees) / num_bees
#         for i in range(num_bees):
#             if random.random() < prob[i]:
#                 new_sol = population[i].copy()
#                 new_sol[random.randint(0, num_features - 1)] ^= 1
#                 new_fit = evaluate_rf(new_sol)
#                 if new_fit > fitness[i]:
#                     population[i], fitness[i], trial[i] = new_sol, new_fit, 0
#                 else:
#                     trial[i] += 1

#         # Scout Bees
#         for i in range(num_bees):
#             if trial[i] > limit:
#                 population[i] = np.random.randint(0, 2, num_features)
#                 fitness[i] = evaluate_rf(population[i])
#                 trial[i] = 0

#         best_idx = np.argmax(fitness)
#         best_solution = population[best_idx]
#         best_accuracy = fitness[best_idx]

#     print(f"Run {run+1}: No ABC={round(acc_no_abc, 4)}, ABC+RF={round(best_accuracy, 4)}")
#     return acc_no_abc, best_accuracy, best_solution

# # Run in parallel
# results = Parallel(n_jobs=-1)(delayed(run_single)(run) for run in range(num_runs))

# acc_rf_no_abc = [r[0] for r in results]
# acc_rf_abc    = [r[1] for r in results]
# best_solutions = [r[2] for r in results]

# best_run = np.argmax(acc_rf_abc)
# final_best_solution = best_solutions[best_run]

# print(f"\nFinal Results:")
# print(f"RF without ABC Accuracy: {round(np.mean(acc_rf_no_abc), 4)}")
# print(f"RF with ABC Accuracy   : {round(np.mean(acc_rf_abc), 4)}")
# print(f"Selected Features: {int(np.sum(final_best_solution))} out of {X.shape[1]}")

# # Plot
# plt.plot(acc_rf_no_abc, label="RF without ABC", marker='o')
# plt.plot(acc_rf_abc, label="RF with ABC", marker='o')
# plt.xlabel("Runs"); plt.ylabel("Accuracy")
# plt.title("RF vs ABC + RF")
# plt.legend(); plt.grid(); plt.show()
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
data = load_breast_cancer()
X = data.data[:, [0, 1]] 
y = data.target 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
svm_classifier = SVC(kernel='linear', C=1.0, random_state=42)
svm_classifier.fit(X_train_scaled, y_train) 
def plot_decision_boundary(X, y, model, scaler):
    h = 0.02  # Step size for mesh
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Predict on mesh points
    Z = model.predict(scaler.transform(np.c_[xx.ravel(), yy.ravel()]))
    Z = Z.reshape(xx.shape)

    # Plot decision boundary and data points
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.3)
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, edgecolors='k')
    plt.xlabel(data.feature_names[0])
    plt.ylabel(data.feature_names[1])
    plt.title('SVM Decision Boundary')
    plt.show()

plot_decision_boundary(X_train, y_train, svm_classifier, scaler)