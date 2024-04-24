**This is a demo made for the CS125 2024 Winter Quarter Final @ UCI**

# FuelFinder
&nbsp;&nbsp;&nbsp;&nbsp;There are currently many free and paid services on the market that track food intake, provide dietary recommendations, and organize recipes. These can be great ways to acheive fitness and health goals. However, many of these apps don’t take into account the current circumstances of the user (how many calories you have burned, what ingredients you have on hand, etc). It’s always disheartening to find a recipe you want to follow only to find out it contains something you are allergic too, or that it makes too much or too little food compared to how hungry you are.

## System overview
![Overview of the system and how it works. The front end and back end work in sync based off data from a compiled database to generate recommendations for the user.](https://github.com/Drew-1771/FuelFinder/blob/main/assets/cs125_system_diagram.png?raw=true)

### The system contains 4 key parts:
- **Compiled Dataset**
- **Backend**
- **Frontend**
- **User Device**

### Compiled Dataset
The **Compiled Dataset** is an excel sheet of recipes and their respective information (ingredients, allergens, etc) that we have built specifically for this demo. The tables get parsed into their respective SQL tables by the **Backend**. The SQL tables are as follows:

* **USERS** table stores the (mostly) static information about the user (the only live value is weight). This is gathered using HealthKit (https://developer.apple.com/documentation/healthkit) from the users device, specifically the values: 
  - HKQuantityTypeIdentifierHeight
  - HKQuantityTypeIdentifierBodyMass (weight)
  - HKCharacteristicTypeIdentifierBiologicalSex
  - HKCharacteristicTypeIdentifierDateOfBirth (converted to an integer for age)

* **HEALTH** table stores the live data collected from the users device (live datastream). This is also gathered using HealthKit (https://developer.apple.com/documentation/healthkit), the values being:
  - HKQuantityTypeIdentifierStepCount
  - HKQuantityTypeIdentifierActiveEnergyBurned
  - HKQuantityTypeIdentifierBasalEnergyBurned (resting calories burned)

* **DISHES** table holds all the recipes we have curated for our backend database. We hand constructed the information for this, as recipe websites are a mess (if you have ever used one you will understand) and it was faster to just get the information by hand than it was to use a web crawler.

* **INGREDIENTS** table holds the nutrition value for all the ingredients used in the recipes.

* **DISH_TO_INGREDIENTS** table maps the ingredients to the dishes.

* **ALLERGENS** table contains the allergens and which ingredients contain them.
* **USER_ALLERGENS** table stores each user's allergen information.

* Summary:
  - We store user information in the **USER**, **HEALTH**, and **USER_ALLERGENS** tables
    - Information in the **USER** and **HEALTH** table is live
  - We store recipe information in the **DISHES**, **INGREDIENTS**, **DISH_TO_INGREDIENTS**, and **ALLERGENS** tables


![Overview of the personal contextual model and how it works. The front end and the back end generate feature vectors that are processed and turned into recommendations that are pushed to the user](https://github.com/Drew-1771/FuelFinder/blob/main/assets/cs125_recommendation_diagram.png?raw=true)
