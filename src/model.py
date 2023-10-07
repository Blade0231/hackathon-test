import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

import pickle


def get_data() -> pd.DataFrame:
    data_url = "http://lib.stat.cmu.edu/datasets/boston"

    ls = [
        "CRIM",
        "ZN",
        "INDUS",
        "CHAS",
        "NOX",
        "RM",
        "AGE",
        "DIS",
        "RAD",
        "TAX",
        "PTRATIO",
        "B",
        "LSTAT",
        # "PRICE"
    ]

    raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
    data = pd.DataFrame(
        np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]]), columns=ls
    )
    data["PRICE"] = raw_df.values[1::2, 2]

    return data


def test_model(boston: pd.DataFrame):
    pickled_model = pickle.load(open("data\\regmodel.pkl", "rb"))
    scaler = pickle.load(open("data\\scaling.pkl", "rb"))
    res = pickled_model.predict(
        scaler.transform(np.array(boston.loc[0]).reshape(1, -1))
    )

    print(f"Prediction: {res[0]}")


def main():
    data = get_data()

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    pickle.dump(scaler, open("data\\scaling.pkl", "wb"))

    regression = LinearRegression()
    regression.fit(X_train, y_train)

    reg_pred = regression.predict(X_test)

    print(f"Mean Absolute Error: {mean_absolute_error(y_test,reg_pred)}")
    print(f"Mean Squared Error: {mean_squared_error(y_test,reg_pred)}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test,reg_pred))}")

    pickle.dump(regression, open("data\\regmodel.pkl", "wb"))

    test_model(data.iloc[:, :-1])
    print("Model Test Done")


if __name__ == "__main__":
    main()
