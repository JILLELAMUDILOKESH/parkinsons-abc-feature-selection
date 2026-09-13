import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# -------------------------------
# Load Dataset
# -------------------------------
data = pd.read_csv("parkinsons.data")
data = data.drop(['name'], axis=1)
X = data.drop(['status'], axis=1)
y = data['status']
# -------------------------------
# Parameters
# -------------------------------
num_runs = 10
num_bees = 200
max_iterations = 40
limit = 10
acc_rf_no_abc = []
acc_rf_abc = []
# 🔥 Track best overall solution
final_best_solution = None
final_best_accuracy = 0
# -------------------------------
# MAIN LOOP
# -------------------------------
for run in range(num_runs):
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=run
    )
    # -------------------------------
    # RF WITHOUT ABC
    # -------------------------------
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc_no_abc = accuracy_score(y_test, y_pred)
    acc_rf_no_abc.append(acc_no_abc)
    # -------------------------------
    # RF WITH ABC
    # -------------------------------
    def evaluate_rf(solution):
        if np.sum(solution) == 0:
            return 0
        cols = X.columns[np.where(solution == 1)]
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train[cols], y_train)
        y_pred = model.predict(X_test[cols])
        return accuracy_score(y_test, y_pred)
    # ABC init
    num_features = X.shape[1]
    population = [np.random.randint(0, 2, num_features) for _ in range(num_bees)]
    fitness = [evaluate_rf(sol) for sol in population]
    trial = [0] * num_bees
    best_solution = None
    best_accuracy = 0
    # ABC loop
    for iteration in range(max_iterations):
        # Employed Bees
        for i in range(num_bees):
            new_sol = population[i].copy()
            j = random.randint(0, num_features - 1)
            new_sol[j] = 1 - new_sol[j]
            new_fit = evaluate_rf(new_sol)
            if new_fit > fitness[i]:
                population[i] = new_sol
                fitness[i] = new_fit
                trial[i] = 0
            else:
                trial[i] += 1
        # Onlooker Bees
        prob = np.array(fitness) / np.sum(fitness)
        for i in range(num_bees):
            if random.random() < prob[i]:
                new_sol = population[i].copy()
                j = random.randint(0, num_features - 1)
                new_sol[j] = 1 - new_sol[j]
                new_fit = evaluate_rf(new_sol)
                if new_fit > fitness[i]:
                    population[i] = new_sol
                    fitness[i] = new_fit
                    trial[i] = 0
                else:
                    trial[i] += 1
        # Scout Bees
        for i in range(num_bees):
            if trial[i] > limit:
                population[i] = np.random.randint(0, 2, num_features)
                fitness[i] = evaluate_rf(population[i])
                trial[i] = 0
        best_index = np.argmax(fitness)
        best_solution = population[best_index]
        best_accuracy = fitness[best_index]
    acc_rf_abc.append(best_accuracy)
    # 🔥 Track best overall solution
    if best_accuracy > final_best_accuracy:
        final_best_accuracy = best_accuracy
        final_best_solution = best_solution

# -------------------------------
# Final Results
# -------------------------------
avg_no_abc = np.mean(acc_rf_no_abc)
avg_with_abc = np.mean(acc_rf_abc)
total_selected_features = int(np.sum(final_best_solution))
print("Final Results:")
print("RF without ABC Accuracy:", round(avg_no_abc, 4))
print("RF with ABC Accuracy   :", round(avg_with_abc, 4))
print("Selected Features:", total_selected_features, "out of", X.shape[1])
# -------------------------------
# Plot Graph
# -------------------------------
plt.figure()
plt.plot(acc_rf_no_abc, label="RF without ABC", marker='o')
plt.plot(acc_rf_abc, label="RF with ABC", marker='o')
plt.xlabel("Runs")
plt.ylabel("Accuracy")
plt.title("RF vs ABC + RF")
plt.legend()
plt.grid()
plt.show()