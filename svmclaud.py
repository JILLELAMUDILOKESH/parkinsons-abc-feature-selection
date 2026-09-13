import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from joblib import Parallel, delayed

# Load Dataset
data = pd.read_csv("parkinsons.data")
data = data.drop(['name'], axis=1)
X = data.drop(['status'], axis=1)
y = data['status']

# Reduced Parameters
num_runs = 10
num_bees = 500    
max_iterations = 40  
limit = 10

def run_single(run):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=run
    )

    # SVM WITHOUT ABC
    model = SVC(kernel='rbf')
    model.fit(X_train, y_train)
    acc_no_abc = accuracy_score(y_test, model.predict(X_test))

    # Cached evaluation function
    cache = {}
    def evaluate_svm(solution):
        key = tuple(solution)
        if key in cache:
            return cache[key]
        if np.sum(solution) == 0:
            return 0
        cols = X.columns[np.where(solution == 1)]
        m = SVC(kernel='rbf')
        m.fit(X_train[cols], y_train)
        acc = accuracy_score(y_test, m.predict(X_test[cols]))
        cache[key] = acc
        return acc

    # ABC init
    num_features = X.shape[1]
    population = [np.random.randint(0, 2, num_features) for _ in range(num_bees)]
    fitness = [evaluate_svm(sol) for sol in population]
    trial = [0] * num_bees
    best_solution, best_accuracy = None, 0

    for iteration in range(max_iterations):
        # Employed Bees
        for i in range(num_bees):
            new_sol = population[i].copy()
            new_sol[random.randint(0, num_features - 1)] ^= 1
            new_fit = evaluate_svm(new_sol)
            if new_fit > fitness[i]:
                population[i], fitness[i], trial[i] = new_sol, new_fit, 0
            else:
                trial[i] += 1

        # Onlooker Bees
        total = np.sum(fitness)
        prob = np.array(fitness) / total if total > 0 else np.ones(num_bees) / num_bees
        for i in range(num_bees):
            if random.random() < prob[i]:
                new_sol = population[i].copy()
                new_sol[random.randint(0, num_features - 1)] ^= 1
                new_fit = evaluate_svm(new_sol)
                if new_fit > fitness[i]:
                    population[i], fitness[i], trial[i] = new_sol, new_fit, 0
                else:
                    trial[i] += 1

        # Scout Bees
        for i in range(num_bees):
            if trial[i] > limit:
                population[i] = np.random.randint(0, 2, num_features)
                fitness[i] = evaluate_svm(population[i])
                trial[i] = 0

        best_idx = np.argmax(fitness)
        best_solution = population[best_idx]
        best_accuracy = fitness[best_idx]

    print(f"Run {run+1}: No ABC={round(acc_no_abc,4)}, ABC+SVM={round(best_accuracy,4)}")
    return acc_no_abc, best_accuracy, best_solution

# Run in parallel
results = Parallel(n_jobs=-1)(delayed(run_single)(run) for run in range(num_runs))

acc_svm_no_abc = [r[0] for r in results]
acc_svm_abc    = [r[1] for r in results]
best_solutions = [r[2] for r in results]

best_run = np.argmax(acc_svm_abc)
final_best_solution = best_solutions[best_run]

print(f"\nAverage SVM without ABC: {round(np.mean(acc_svm_no_abc), 4)}")
print(f"Average SVM with ABC   : {round(np.mean(acc_svm_abc), 4)}")
print(f"Selected Features: {int(np.sum(final_best_solution))} out of {X.shape[1]}")

plt.plot(acc_svm_no_abc, label="SVM without ABC", marker='o')
plt.plot(acc_svm_abc, label="SVM with ABC", marker='o')
plt.xlabel("Runs"); plt.ylabel("Accuracy")
plt.title("SVM vs ABC + SVM")
plt.legend(); plt.grid(); plt.show()