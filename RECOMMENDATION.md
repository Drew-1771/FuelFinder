# System Overview

## Quick Introduction

- The recommendation system we built here is simple and computationally efficient. We spent the first week of the 2 weeks for the project creating this system based on numerous methods and models discussed in lecture.
- If we were to further improve upon it, we agreed we would add a PyTorch TorchRec model to better approximate the user's needs. We also wanted to improve the allergen information to help with the constraint satisfaction problem that arises during the computation of a recommended dish.

## Personal Model

- Generated from the data collected from the user's device and when they create our account. This data is stored in the USERS, HEALTH, and USER_ALLERGENS tables in the database. This is used as the starting point of the recommendation algorithm. We preprocess using the user's food allergies as a filter (we don’t want to recommend something that will kill them) and then generate a feature vector from their data:
  ```
    User Feature Vector
    {
        Height
        Weight (live)
        Sex
        Age
        Active Calories Burned (live)
        Resting Calories Burned (live)
        Step Count (live)
    }
  ```

## Context

- We apply context to our model by applying our utility function. Using the live data sources from the user feature vector in conjunction with the users static information, the utility function (described step by step in the section below) generates a final feature vector we will be using to make the recommendation:
  ```
  Feature Vector:
  {
    Calories_needed (live)
    Protein_needed (live)
    Carbs_needed (live)
  }
  ```

## Recommendation

- We generate the recommendations using the Feature Vector and the Dish Information Vector (shown below) of each Recipe (internally referred to as Dishes).

  ```
  Dish Information Vector:
  {
    Calories
    Protein
    Carbs
  }
  ```

- Now we just generate the recommendations. We then calculate the Euclidean distance between the Feature vector and the Dish Information Vector and generate a List<Euclidean Distance, Dish> and sort it by the distance. While we sort, we also take into account the sugar and fat content. We sort by this order, first distance (minimize), then sugar (minimize), then fat (minimize). We did this in order to make sure we recommend the healthiest dish possible to the user.

These 3 systems are what create the **Personal Contextual Model**

A basic overview of the control flow goes as follows:

1. We iterate over all the valid dishes (result from the preprocessing done with the user's allergen information) and generate the Dish Information Vector. We calculate the Euclidean distance between the Feature Vector and the Dish Information Vector and store it in a list. We sort that list and iterate over it in place, minimizing similar dishes sugar and fat content

2. We now have a list of recommendations we can make to the user, so we choose the first 5 and send it back to the device. This is our full Personal Contextual Recommender System.

# Generating the recommendation

The recommendation is generated as follows. First, we use the user's dietary limitations as a preprocessing filter, removing any recipes with incompatible ingredients or allergens. We then generate a vector based on the information we have gathered from them. This is the personal part of our model. Their data and statistics have been gathered here into this user feature vector:

```
User Feature Vector
{
  Height
  Weight (live)
  Sex
  Age
  Active Calories Burned (live)
  Resting Calories Burned (live)
  Step Count (live)
}
```

Now, we apply context to our model. First, Height and Weight get calculated into BMI, and we replace Height with BMI. A Healthy BMI is between 18.5-24.9, so subtract 21.7 from the BMI ([source](https://www.nhlbi.nih.gov/health/educational/healthdisp/pdf/tipsheets/Are-You-at-a-Healthy-Weight.pdf)). Now a positive number corresponds to overweight and negative means underweight. Resulting vector now looking like:

```
Transitional Feature Vector
{
  BMI (live)
  Weight (live)
  Sex
  Age
  Active Calories Burned (live)
  Resting Calories Burned (live)
  Step Count (live)
}
```

We sum the Active and Resting Calories burned to get an approximation of the amount of calories they have burned as Calories_needed:

```
Transitional Feature Vector
{
  BMI (live)
  Weight (live)
  Sex
  Age
  Calories_needed (live)
  Step Count (live)
}
```

We then calculate their Protein_needed by multiplying their weight by 0.4536 (convert to kg), then multiplying by 0.8 (0.8 grams of protein per 1 kg of body weight) and dividing it by 3 (to account for daily consumption) ([source](https://www.health.harvard.edu/blog/how-much-protein-do-you-need-every-day-201506188096)):

```
Transitional Feature Vector
{
  BMI (live)
  Sex
  Age
  Calories_needed (live)
  Protein_needed (live)
  Step Count (live)
}
```

We then calculate Carbs needed. 50% of your daily calories should come from carbohydrates ([source](https://www.mayoclinic.org/healthy-lifestyle/nutrition-and-healthy-eating/in-depth/carbohydrates/art-20045705#:~:text=The%20Dietary%20Guidelines%20for%20Americans,grams%20of%20carbs%20a%20day.)), so we use by the BMI (decreases by 2% for every BMI point since the healthy BMI is now 0) and Step count (increases by 1% for every 500 steps) to calculate Carbs_needed as = (Calories_needed / 2) - (BMI \* (Calories_needed \* 0.02)) + (StepCount / 500 \* (Calories_needed \* 0.01)):

```
Transitional Feature Vector
{
  BMI (live)
  Sex
  Age
  Calories_needed (live)
  Protein_needed (live)
  Carbs_needed (live)
}
```

We then use sex and age to make some final adjustments. As people get older, their metabolism slows down, so to model that we will be adding 200 calories for people under 30 and removing 200 calories for people over 50, modeled as the formula: Calories_needed = Calories_needed + [(age \* -20) + 800] (bounded between 200 and -200). This formula just means that when x <= 30, y = 200, when 30 < x < 50, y will be between 200 and -200, and when x >= 50, y will be -200 ([source](https://pubmed.ncbi.nlm.nih.gov/8361073/)):

```
Final Feature Vector:
{
  Calories_needed (live)
  Protein_needed (live)
  Carbs_needed (live)
}
```

This is the final feature vector we will be using to make the recommendation. We then search the Dishes query (virtual table from the database). Each dish (that has not been removed from the preprocessing with the users allergen information) will have the following information vector:

```
Full Dish Information Vector
{
Calories
Fat
Protein
Sugar
Carbs
}
```

And subsequently, a subset of that vector we will be using to search, stated as the Dish Information Vector:

```
Dish Information Vector
{
Calories
Protein
Carbs
}
```

Now we just generate the recommendations. We then calculate the Euclidean distance between the Feature vector and the Dish Information Vector and generate a List\<Euclidean Distance, Dish\> and sort it by the distance. We then iterate over the list in place and gather groups of dishes (3 max) that are close in distance. We do this so we can use the last two stats of the Dish to actually make a healthy recommendation. Those groups of 3 are sorted in place by minimizing the sugar and then minimizing the fat. We did this in order to make sure we recommend the healthiest dish possible to the user.

Finally, we simply return the top 5 results (in order) as recommendations to the user. This ensures that we don’t query more than 15-20% of the data and bomb the user's device with data.
