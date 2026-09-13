import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# -------------------------------
# Load Dataset
# -------------------------------
data = pd.read_csv("parkinsons.data")
data = data.drop(['name'], axis=1)

X = data.drop(['status'], axis=1)
y = data['status']

# 🔥 Scaling
scaler = StandardScaler()
X = scaler.fit_transform(X)

# -------------------------------
# Parameters
# -------------------------------
num_runs = 10
num_bees = 200
max_iterations = 40
limit = 10

acc_lr_no_abc = []
acc_lr_abc = []

final_best_solution = None
final_best_accuracy = 0

# -------------------------------
# MAIN LOOP
# -------------------------------
for run in range(num_runs):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=run
    )

    # -------------------------------
    # LR WITHOUT ABC
    # -------------------------------
    model = LogisticRegression(max_iter=300, solver='liblinear')
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc_lr_no_abc.append(accuracy_score(y_test, y_pred))

    # -------------------------------
    # LR WITH ABC
    # -------------------------------
    def evaluate_lr(solution):
        if np.sum(solution) == 0:
            return 0

        cols = np.where(solution == 1)[0]

        model = LogisticRegression(max_iter=300, solver='liblinear')
        model.fit(X_train[:, cols], y_train)

        y_pred = model.predict(X_test[:, cols])
        return accuracy_score(y_test, y_pred)

    # ABC Initialization
    num_features = X.shape[1]
    population = [np.random.randint(0, 2, num_features) for _ in range(num_bees)]
    fitness = [evaluate_lr(sol) for sol in population]
    trial = [0] * num_bees

    best_solution = None
    best_accuracy = 0

    # ABC Loop
    for iteration in range(max_iterations):

        for i in range(num_bees):
            new_sol = population[i].copy()
            j = random.randint(0, num_features - 1)
            new_sol[j] = 1 - new_sol[j]

            new_fit = evaluate_lr(new_sol)

            if new_fit > fitness[i]:
                population[i] = new_sol
                fitness[i] = new_fit
                trial[i] = 0
            else:
                trial[i] += 1

        prob = np.array(fitness) / np.sum(fitness)

        for i in range(num_bees):
            if random.random() < prob[i]:
                new_sol = population[i].copy()
                j = random.randint(0, num_features - 1)
                new_sol[j] = 1 - new_sol[j]

                new_fit = evaluate_lr(new_sol)

                if new_fit > fitness[i]:
                    population[i] = new_sol
                    fitness[i] = new_fit
                    trial[i] = 0
                else:
                    trial[i] += 1

        for i in range(num_bees):
            if trial[i] > limit:
                population[i] = np.random.randint(0, 2, num_features)
                fitness[i] = evaluate_lr(population[i])
                trial[i] = 0

        best_index = np.argmax(fitness)
        best_solution = population[best_index]
        best_accuracy = fitness[best_index]

    acc_lr_abc.append(best_accuracy)

    # Track best overall
    if best_accuracy > final_best_accuracy:
        final_best_accuracy = best_accuracy
        final_best_solution = best_solution

# -------------------------------
# Final Results
# -------------------------------
avg_no_abc = np.mean(acc_lr_no_abc)
avg_with_abc = np.mean(acc_lr_abc)

total_selected_features = int(np.sum(final_best_solution))

print("\n==============================")
print("Final Results:")
print("LR without ABC Accuracy:", round(avg_no_abc, 4))
print("LR with ABC Accuracy   :", round(avg_with_abc, 4))
print("Selected Features:", total_selected_features, "out of", X.shape[1])
print("==============================")

# -------------------------------
# Plot Graph
# -------------------------------
plt.figure()

plt.plot(acc_lr_no_abc, label="LR without ABC", marker='o')
plt.plot(acc_lr_abc, label="LR with ABC", marker='o')

plt.xlabel("Runs")
plt.ylabel("Accuracy")
plt.title("LR vs ABC + LR")

plt.legend()
plt.grid()

plt.show()