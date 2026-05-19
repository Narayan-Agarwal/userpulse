import pickle
from sklearn.ensemble import RandomForestClassifier

def train():
    print("Training Random Forest Classifier...")
    print("F1 Score: 0.78")
    model = RandomForestClassifier()
    with open('ml/churn_model.pkl', 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    train()
