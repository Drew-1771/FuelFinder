from _debug import debug
import sqlite3
from pathlib import Path
import csv
from collections import defaultdict

ROOT = Path.cwd()


class Database:
    def __init__(self) -> None:
        Path(ROOT / "database").mkdir(exist_ok=True)

        self._path = Path(ROOT / "database" / "database.db")
        debug(f"Database self._path set to {self._path}")

        # if db file is not found, perform first time setup
        if not self._path.exists():
            debug(f"Database @ {str(self._path)} does not exist, performing first time setup")  # fmt: skip
            self._connection = sqlite3.connect(self._path)
            self._cursor = self._connection.cursor()
            self._connection.execute("PRAGMA foreign_keys = ON")

            self._cursor.execute(
                """
                CREATE TABLE USERS
                (
                ID INTEGER PRIMARY KEY,
                HEIGHT INTEGER,
                WEIGHT FLOAT,
                SEX CHAR(8),
                AGE INTEGER
                )
                """
            )

            self._cursor.execute(
                """
                CREATE TABLE DISHES
                (
                DISH VARCHAR(256) PRIMARY KEY,
                CUISINE VARCHAR(256),
                RECIPE VARCHAR(256),
                USES INT DEFAULT 0
                )
                """
            )

            self._cursor.execute(
                """
                CREATE TABLE INGREDIENTS
                (
                INGREDIENT VARCHAR(256) PRIMARY KEY,
                CALORIES FLOAT,
                FAT FLOAT,
                PROTEIN FLOAT,
                SUGAR FLOAT,
                CARBS FLOAT
                )
                """
            )

            self._cursor.execute(
                """
                CREATE TABLE DISH_TO_INGREDIENTS
                (
                DISH VARCHAR(256) REFERENCES DISHES(DISH),
                INGREDIENT VARCHAR(256) REFERENCES INGREDIENTS(INGREDIENT),
                AMOUNT FLOAT
                )
                """
            )

            self._cursor.execute(
                """
                CREATE TABLE ALLERGEN
                (
                INGREDIENT VARCHAR(256) REFERENCES INGREDIENTS(INGREDIENT),
                ALLERGEN_NAME VARCHAR(256),
                BIOCHEMICAL_NAME VARCHAR(256)
                )
                """
            )

            self._cursor.execute(
                """
                CREATE TABLE USER_ALLERGENS
                (
                ID INTEGER REFERENCES USERS(ID),
                ALLERGEN_NAME VARCHAR(256)
                )
                """
            )

            self._cursor.execute(
                """
                CREATE TABLE HEALTH
                (
                DATE TIMESTAMP PRIMARY KEY,
                ID INTEGER REFERENCES USERS(ID),
                STEP_COUNT INT,
                ACTIVE_CALORIES_BURNED FLOAT,
                RESTING_CALORIES_BURNED FLOAT
                )
                """
            )

            self._connection.commit()
        # else, connect
        else:
            self._connection = sqlite3.connect(self._path)
            self._cursor = self._connection.cursor()
        debug(f"Connected to database @ {str(self._path)}")

    def addUser(self, id: int, height: int, weight: float, sex: str, age: int) -> None:
        debug(f"adding USER: {id}, {height}, {weight}, {sex}, {age}")
        self._cursor.execute(
            f"INSERT INTO USERS (ID,HEIGHT,WEIGHT,SEX,AGE) VALUES ({id}, {height}, {weight}, '{sex}', {age});"
        )
        self._connection.commit()

    def addDish(self, dish: str, cuisine: str, recipe: str) -> None:
        debug(f"adding DISH: {dish}, {cuisine}, {recipe}")
        self._cursor.execute(
            f"INSERT INTO DISHES (DISH, CUISINE, RECIPE) VALUES ('{dish}', '{cuisine}', '{recipe}');"
        )
        self._connection.commit()

    def addIngredient(
        self,
        ingredient: str,
        calories: float,
        fat: float,
        protein: float,
        sugar: float,
        carbs: float,
    ) -> None:
        debug(
            f"adding INGREDIENTS: {ingredient}, {calories}, {fat}, {protein}, {sugar}, {carbs}"
        )
        self._cursor.execute(
            f"INSERT INTO INGREDIENTS (INGREDIENT, CALORIES, FAT, PROTEIN, SUGAR, CARBS) VALUES ('{ingredient}', {calories}, {fat}, {protein}, {sugar}, {carbs});"
        )
        self._connection.commit()

    def addDishIngredient(self, dish: str, ingredient: str, amount: float) -> None:
        debug(f"adding DISH_TO_INGREDIENTS: {dish}, {ingredient}, {amount}")
        self._cursor.execute(
            f"INSERT INTO DISH_TO_INGREDIENTS (DISH, INGREDIENT, AMOUNT) VALUES ('{dish}', '{ingredient}', {amount});"
        )
        self._connection.commit()

    def addAllergen(
        self, ingredient: str, allergen_name: str, biochemical_name: float
    ) -> None:
        debug(f"adding ALLERGEN: {ingredient}, {allergen_name}, {biochemical_name}")
        self._cursor.execute(
            f"INSERT INTO ALLERGEN (INGREDIENT,ALLERGEN_NAME, BIOCHEMICAL_NAME) VALUES ('{ingredient}', '{allergen_name}', '{biochemical_name}');"
        )
        self._connection.commit()

    def addUserAllergen(self, id: int, allergen_name: str) -> None:
        debug(f"adding USER_ALLERGENS: {id}, {allergen_name}")
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._cursor.execute(
            f"INSERT INTO USER_ALLERGENS (ID,ALLERGEN_NAME) VALUES ({id}, '{allergen_name}');"
        )
        self._connection.commit()

    def addHealthStat(
        self,
        date: str,
        user_id: int,
        step_count: int,
        active_calories_burned: float,
        resting_calories_burned: float,
    ) -> None:
        debug(
            f"adding HEALTH: {date}, {step_count}, {active_calories_burned}, {resting_calories_burned}",
            debug=False,
        )
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._cursor.execute(
            f"INSERT INTO HEALTH (DATE,ID,STEP_COUNT,ACTIVE_CALORIES_BURNED,RESTING_CALORIES_BURNED) VALUES ('{date}', {user_id}, {step_count}, {active_calories_burned}, {resting_calories_burned});"
        )
        self._connection.commit()

    def view_dishes(self) -> list:
        self._connection.execute("PRAGMA foreign_keys = ON")
        return self._cursor.execute(
            """
                SELECT d.DISH, SUM(i.CALORIES * d.AMOUNT), SUM(i.FAT * d.AMOUNT), SUM(i.PROTEIN * d.AMOUNT), SUM(i.SUGAR * d.AMOUNT), SUM(i.CARBS * d.AMOUNT)
                FROM DISH_TO_INGREDIENTS as d, INGREDIENTS as i
                WHERE d.INGREDIENT = i.INGREDIENT
                GROUP BY d.DISH;
                """
        ).fetchall()

    def view_allergens(self) -> list:
        self._connection.execute("PRAGMA foreign_keys = ON")
        return self._cursor.execute(
            """
                SELECT ALLERGEN_NAME, INGREDIENT
                FROM ALLERGEN as a
                """
        ).fetchall()


class DataLoader:
    def __init__(
        self,
        users: str = "USERS",
        dishes: str = "DISHES",
        dish_to_ingredient: str = "DISH_TO_INGREDIENT",
        ingredients: str = "INGREDIENTS",
        allergens: str = "ALLERGEN",
        user_allergens: str = "USER_ALLERGENS",
    ) -> None:
        self._path = Path(ROOT / "data")
        debug(f"Dataloader._path set to {self._path}")

        if Path(ROOT / "database" / "database.db").exists():
            debug("removing old database.db")
            Path(ROOT / "database" / "database.db").unlink()

        self._database = Database()

        self._users = users
        self._dishes = dishes
        self._dish_to_ingredient = dish_to_ingredient
        self._ingredients = ingredients
        self._allergens = allergens
        self._user_allergens = user_allergens

    def buildDatabase(self) -> None:
        dishes, ingredients, dishes_to_ingredients, allergen, users, user_allergen = (
            True,
            True,
            True,
            True,
            True,
            True,
        )

        # run until all is build in correct order
        while (
            dishes
            or ingredients
            or dishes_to_ingredients
            or allergen
            or users
            or user_allergen
        ):
            for filename in Path(self._path).iterdir():

                # build dishes table
                if dishes and (self._dishes in filename.name):
                    debug(f"reading {filename.name}")
                    with open(filename, "r") as file:
                        data = list(csv.reader(file))

                        for dish, cuisine, recipe in data[1:]:
                            self._database.addDish(
                                str.lower(dish).strip(),
                                str.lower(cuisine).strip(),
                                str.lower(recipe).strip(),
                            )
                    dishes = False

                # build ingredients table
                if (
                    ingredients
                    and (self._ingredients in filename.name)
                    and not (self._dish_to_ingredient in filename.name)
                ):
                    debug(f"reading {filename.name}")
                    with open(filename, "r") as file:
                        data = list(csv.reader(file))

                        for ingredient, calories, fat, protein, sugar, carbs in data[
                            1:
                        ]:
                            self._database.addIngredient(
                                str.lower(ingredient).strip(),
                                float(calories) if calories != "" else 0,
                                float(fat) if fat != "" else 0,
                                float(protein) if protein != "" else 0,
                                float(sugar) if sugar != "" else 0,
                                float(carbs) if carbs != "" else 0,
                            )
                    ingredients = False

                # build allergen table if ingredients table already exists
                if (
                    allergen
                    and (not ingredients)
                    and (self._allergens in filename.name)
                    and (not self._user_allergens in filename.name)
                ):
                    debug(f"reading {filename.name}")
                    with open(filename, "r") as file:
                        data = list(csv.reader(file))

                        for ingredient, allergen_name, biochemical_name in data[1:]:
                            self._database.addAllergen(
                                str.lower(ingredient).strip(),
                                str.lower(allergen_name).strip(),
                                str.lower(biochemical_name).strip(),
                            )
                    allergen = False

                # build dish_to_ingredient_table if dishes and ingredients table already exist
                if (
                    dishes_to_ingredients
                    and (not dishes and not ingredients)
                    and (self._dish_to_ingredient in filename.name)
                ):
                    debug(f"reading {filename.name}")
                    with open(filename, "r") as file:
                        data = list(csv.reader(file))

                        for dish, ingredient, amount in data[1:]:
                            self._database.addDishIngredient(
                                str.lower(dish).strip(),
                                str.lower(ingredient).strip(),
                                float(amount) if amount != "" else 0,
                            )
                    dishes_to_ingredients = False

                # build users table
                if (
                    users
                    and not self._user_allergens in filename.name
                    and self._users in filename.name
                ):
                    debug(f"reading {filename.name}")
                    with open(filename, "r") as file:
                        data = list(csv.reader(file))

                        ids = list()
                        for id, height, weight, sex, age in data[1:]:
                            self._database.addUser(
                                int(str.lower(id).strip()),
                                int(str.lower(height).strip()) if height != "" else -1,
                                (
                                    float(str.lower(weight).strip())
                                    if weight != ""
                                    else -1
                                ),
                                str.lower(sex).strip(),
                                int(str.lower(age).strip()) if age != "" else -1,
                            )
                            ids.append(id)

                        for id in ids:
                            possible_path_to_health_stats = (
                                self._path / f"health_stats - health_data_user{id}.csv"
                            )
                            if possible_path_to_health_stats.exists():
                                self.buildHealthInfo(
                                    id,
                                    possible_path_to_health_stats,
                                )
                                pass
                    users = False

                # build users_allergens table
                if (
                    user_allergen
                    and not users
                    and not allergen
                    and (not self._users in filename.name)
                    and (self._user_allergens in filename.name)
                ):
                    debug(f"reading {filename.name}")
                    with open(filename, "r") as file:
                        data = list(csv.reader(file))
                        print(data)
                        for id, allergen_name in data[1:]:
                            self._database.addUserAllergen(
                                int(str.lower(id).strip()),
                                str.lower(allergen_name).strip(),
                            )
                    user_allergen = False

    def buildHealthInfo(self, id_target: int, health_stats: Path) -> None:
        debug(f"reading {health_stats.name}")
        with open(health_stats, "r") as file:
            data = list(csv.reader(file))

            for (
                id,
                index,
                date,
                step_count,
                active_calories_burned,
                resting_calories_burned,
            ) in data[1:]:
                if id == id_target:
                    self._database.addHealthStat(
                        str.lower(date).strip(),
                        id,
                        int(str.lower(step_count).strip()),
                        float(str.lower(active_calories_burned).strip()),
                        float(str.lower(resting_calories_burned).strip()),
                    )

    def getDishInfo(self) -> list:
        return self._database.view_dishes()

    def getAllergenInfo(self) -> list:
        return self._database.view_allergens()


if __name__ == "__main__":
    data = DataLoader()
    data.buildDatabase()

    print("Dishes:")
    for dish, calories, fat, protein, sugar, carbs in data.getDishInfo():
        print(
            f"{dish}:\n\tcalories: {round(calories, 3)}\n\tfat: {round(fat, 3)}\n\tprotein: {round(protein, 3)}\n\tsugar: {round(sugar, 3)}\n\tcarbs: {round(carbs, 3)}"
        )

    print("\nAllergens:")
    allergens = defaultdict(list)
    for allergen_name, ingredient in data.getAllergenInfo():
        allergens[allergen_name].append(ingredient)

    for allergen_name, ingredients in allergens.items():
        print(f"{allergen_name}:")
        for ingredient in ingredients:
            print(f"\t{ingredient}")
