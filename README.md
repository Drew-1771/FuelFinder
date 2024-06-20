**This is a demo made for the CS125 2024 Winter Quarter Final @ UCI**

# FuelFinder

&nbsp;&nbsp;&nbsp;&nbsp;There are currently many free and paid services on the market that track food intake, provide dietary recommendations, and organize recipes. These can be great ways to achieve fitness and health goals. However, many of these apps don’t take into account the current circumstances of the user (how many calories you have burned, what ingredients you have on hand, etc). It’s always disheartening to find a recipe you want to follow, only to find out it contains something you are allergic to, or that it makes too much or too little food compared to how hungry you are.

## System Overview

![Overview of the system and how it works. The front end and back end work in sync based on data from a compiled database to generate recommendations for the user.](https://github.com/Drew-1771/FuelFinder/blob/main/assets/cs125_system_diagram.png?raw=true)

### The system contains 4 key parts:

- **Compiled Dataset**
- **Backend**
- **Frontend**
- **User Device**

### Compiled Dataset

- **Entity–relationship diagram for the Compiled Dataset**

![Entity-relationship diagram of the Compiled Dataset.](https://github.com/Drew-1771/FuelFinder/blob/main/assets/cs125_ER_Diagram.png?raw=true)

The **Compiled Dataset** is an Excel sheet of recipes and their respective information (ingredients, allergens, etc) that we have built specifically for this demo. The tables get parsed into their respective SQL tables by the **Backend**. The SQL tables are as follows:

- **USERS** table stores the (mostly) static information about the user (the only live value is weight). This is gathered using HealthKit (https://developer.apple.com/documentation/healthkit) from the user's device, specifically the values:

  - HKQuantityTypeIdentifierHeight
  - HKQuantityTypeIdentifierBodyMass (weight)
  - HKCharacteristicTypeIdentifierBiologicalSex
  - HKCharacteristicTypeIdentifierDateOfBirth (converted to an integer for age)

- **HEALTH** table stores the live data collected from the users device (live data stream). This is also gathered using HealthKit (https://developer.apple.com/documentation/healthkit), the values being:

  - HKQuantityTypeIdentifierStepCount
  - HKQuantityTypeIdentifierActiveEnergyBurned
  - HKQuantityTypeIdentifierBasalEnergyBurned (resting calories burned)

- **DISHES** table holds all the recipes we have curated for our backend database. We hand-constructed the information for this, as recipe websites are a mess (if you have ever used one you will understand) and it was faster to just get the information by hand than it was to use a web crawler.

- **INGREDIENTS** table holds the nutritional value for all the ingredients used in the recipes.

- **DISH_TO_INGREDIENTS** table maps the ingredients to the dishes.

- **ALLERGENS** table contains the allergens and which ingredients contain them.
- **USER_ALLERGENS** table stores each user's allergen information.

- **Summary:**

  - We store user information in the **USERS**, **HEALTH**, and **USER_ALLERGENS** tables
    - Information in the **USERS** and **HEALTH** table is live
  - We store recipe information in the **DISHES**, **INGREDIENTS**, **DISH_TO_INGREDIENTS**, and **ALLERGENS** tables

### Backend

- The **Backend** loads the **Compiled Dataset** into a SQL database, making tables, views, and useful statistics from the data. The **Backend** also generates the recommendations for the user using a **Personal Contextual Model** (a summary of which is shown below).

* **Personal Contextual Model**

  - The user's data is used to generate their feature vector (this is described in depth in the RECOMMENDATION.md file). The **Frontend** sends the data from HealthKit to generate the User feature vector on the **Backend**. The User feature vector is transformed into the Final feature vector for the user, the calories, protein, and carbs needed. The **Backend** then generates a parallel vector of information for each dish, and they are compared using Euclidean distance.

  ![Overview of the personal contextual model and how it works. The front end and the back end generate feature vectors that are processed and turned into recommendations that are pushed to the user](https://github.com/Drew-1771/FuelFinder/blob/main/assets/cs125_recommendation_diagram.png?raw=true)

### Frontend and User Device

#### Home Tab

- The Home tab allows users to see their generic daily recommendations. These recommendations are shown to encourage the user to explore. This is beneficial because it allows us to tune their personalized recommendations. The Home tab also has 2 horizontal scrollers for personal recommendations, which is what we generate on the **Backend**, and popular foods, which is also an attempt to get the user to explore.

#### Search Tab

- The Search tab allows users to search dishes. We use Levenshtein distance between strings to help users find what they are looking for fast.

#### Saved Recipes Tab

- The Saved Recipes tab shows users their saved recipes and shareable groups of recipes. We thought users could group recipes together to make something along the lines of a virtual cookbook, which they could send and share with friends.

![Overview of the app and features. The Home tab allows users to see their generic daily recommendations, as well as 2 horizontal scrollers for personal recommendations and popular foods. The Search tab allows users to search dishes. The Saved Recipes tab shows users their saved recipes and shareable groups of recipes.](https://github.com/Drew-1771/FuelFinder/blob/main/assets/cs125_app_diagram.png?raw=true)
