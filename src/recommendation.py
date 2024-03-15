from dataclasses import dataclass
from _debug import debug
import numpy as np


@dataclass
class UserFeatureVector:
    height: int
    weight: float
    sex: str
    age: float
    activeCaloriesBurned: float
    restingCaloriesBurned: float
    stepCount: int


@dataclass
class DishInfoVector:
    caloriesNeeded: float
    proteinNeeeded: float
    carbsNeeded: float


def utility_function(id: int, data) -> DishInfoVector:
    _debug = False
    _, height, weight, sex, age = data.getUserInfo(id)[0]
    (
        date,
        _,
        stepCount,
        activeCaloriesBurned,
        restingCaloriesBurned,
    ) = data.getHealthInfo(id)[
        -1
    ]  # latest

    # ensure all values are inititalized into the feature vector
    userVector = UserFeatureVector(
        height=height,
        weight=weight,
        sex=sex,
        age=age,
        activeCaloriesBurned=activeCaloriesBurned,
        restingCaloriesBurned=restingCaloriesBurned,
        stepCount=stepCount,
    )

    # put into dict and begin transforms
    vector = {
        "height": userVector.height,
        "weight": userVector.weight,
        "sex": userVector.sex,
        "age": userVector.age,
        "activeCaloriesBurned": userVector.activeCaloriesBurned,
        "restingCaloriesBurned": userVector.restingCaloriesBurned,
        "stepCount": userVector.stepCount,
    }
    debug(vector, _debug)
    # calculate BMI
    vector = {
        "bmi": np.divide(vector["weight"], vector["height"] ** 2),
        "weight": vector["weight"],
        "sex": vector["sex"],
        "age": vector["age"],
        "activeCaloriesBurned": vector["activeCaloriesBurned"],
        "restingCaloriesBurned": vector["restingCaloriesBurned"],
        "stepCount": vector["stepCount"],
    }
    debug(vector, _debug)
    # calculate calories needed
    vector = {
        "bmi": vector["bmi"],
        "weight": vector["weight"],
        "sex": vector["sex"],
        "age": vector["age"],
        "caloriesNeeded": vector["activeCaloriesBurned"]
        + vector["restingCaloriesBurned"],
        "stepCount": vector["stepCount"],
    }
    debug(vector, _debug)
    # calculate protein needed
    vector = {
        "bmi": vector["bmi"],
        "sex": vector["sex"],
        "age": vector["age"],
        "caloriesNeeded": round(vector["caloriesNeeded"], 1),
        "proteinNeeded": np.divide(vector["weight"] * float(0.4536) * float(0.8), 3),
        "stepCount": vector["stepCount"],
    }
    debug(vector, _debug)
    # calculate carbs needed
    carbsNeeded = np.abs(
        (np.divide(vector["caloriesNeeded"], 2))
        - (vector["bmi"] * (vector["caloriesNeeded"] * float(0.02)))
        + (vector["stepCount"] * (vector["caloriesNeeded"] * float(0.01)))
    )
    vector = {
        "sex": vector["sex"],
        "age": vector["age"],
        "caloriesNeeded": vector["caloriesNeeded"],
        "proteinNeeded": round(vector["proteinNeeded"], 1),
        "carbsNeeded": round(carbsNeeded, 1),
    }
    debug(vector, _debug)
    # adjust with sex and age
    caloriesNeeded = vector["caloriesNeeded"] + ((vector["age"] * -20) + 800)
    if caloriesNeeded > 200:
        caloriesNeeded = 200
    elif caloriesNeeded < -200:
        caloriesNeeded = -200
    vector = {
        "caloriesNeeded": caloriesNeeded,
        "proteinNeeded": vector["proteinNeeded"],
        "carbsNeeded": vector["carbsNeeded"],
    }
    debug(vector, _debug)
    return DishInfoVector(
        vector["caloriesNeeded"], vector["proteinNeeded"], vector["carbsNeeded"]
    )


def recommend(id: int, data, dishes: list, recipes: list):
    dishInfoV = utility_function(id, data)

    recommendations = list()
    for dish, nutrition in dishes.items():
        # apply preprocess filter
        if dish not in recipes.keys():
            debug(f"skipping {dish}")
        else:
            # calculate euclidean distance of vectors
            distance = np.sqrt(
                ((dishInfoV.caloriesNeeded - nutrition["calories"]) ** 2)
                + ((dishInfoV.proteinNeeeded - nutrition["protein"]) ** 2)
                + ((dishInfoV.carbsNeeded - nutrition["carbs"]) ** 2)
            )
            debug(f"distance of {dish} is {distance}", False)

            recommendations.append((distance, (dish, nutrition)))

    # sort to find the best match, and minimize fat and sugar
    recommendations.sort(key=lambda x: (x[0], (x[1][1])["sugar"], (x[1][1])["fat"]))
    debug(recommendations, False)

    # return only the first 5
    recommendations = {index: item[1][0] for index, item in enumerate(recommendations)}
    recommendations_list_to_return = list()
    count = 0
    for _, value in sorted(recommendations.items()):
        if count == 5:
            break
        recommendations_list_to_return.append(value)
        count += 1
    return {
        int(index): item for index, item in enumerate(recommendations_list_to_return)
    }
