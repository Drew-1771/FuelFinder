from _debug import debug
import sqlite3
from pathlib import Path
import csv


class Database:
    def __init__(self) -> None:
        Path(Path.cwd() / "database").mkdir(exist_ok=True)

        self._path = Path(Path.cwd() / "database" / "database.db")
        debug(f"Database self._path set to {self._path}")

        # if db file is not found, perform first time setup
        if not self._path.exists():
            debug(f"Database @ {str(self._path)} does not exist, performing first time setup")  # fmt: skip
            self._connection = sqlite3.connect(self._path)
            self._cursor = self._connection.cursor()
            self._connection.execute("PRAGMA foreign_keys = ON")

            self._cursor.execute(
                """
                CREATE TABLE DISHES
                (
                DISH VARCHAR(256) PRIMARY KEY,
                CUISINE VARCHAR(256),
                RECIPE VARCHAR(256)
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
            self._connection.commit()
        # else, connect
        else:
            self._connection = sqlite3.connect(self._path)
            self._cursor = self._connection.cursor()
        debug(f"Connected to database @ {str(self._path)}")

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


class DataLoader:
    def __init__(
        self,
        dishes: str = "DISHES",
        dish_to_ingredient: str = "DISH_TO_INGREDIENT",
        ingredients: str = "INGREDIENTS",
        allergens: str = "ALLERGEN",
    ) -> None:
        self._path = Path(Path.cwd() / "data")
        debug(f"Dataloader._path set to {self._path}")

        if Path(Path.cwd() / "database" / "database.db").exists():
            debug("removing old database.db")
            Path(Path.cwd() / "database" / "database.db").unlink()

        self._database = Database()

        self._dishes = dishes
        self._dish_to_ingredient = dish_to_ingredient
        self._ingredients = ingredients
        self._allergens = allergens

    def buildDatabase(self) -> None:
        dishes, ingredients, dishes_to_ingredients, allergen = True, True, True, True

        # run until all is build in correct order
        while dishes or ingredients or dishes_to_ingredients or allergen:
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

    def getDishInfo(self) -> list:
        return self._database.view_dishes()


if __name__ == "__main__":
    data = DataLoader()
    data.buildDatabase()
    for dish, calories, fat, protein, sugar, carbs in data.getDishInfo():
        print(
            f"{dish}:\n\tcalories: {round(calories, 3)}\n\tfat: {round(fat, 3)}\n\tprotein: {round(protein, 3)}\n\tsugar: {round(sugar, 3)}\n\tcarbs: {round(carbs, 3)}"
        )
