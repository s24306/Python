import sqlite3
import argparse
import sys

conn = sqlite3.connect("food_blog.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")
cur.execute("""CREATE TABLE IF NOT EXISTS measures (
            measure_id INTEGER PRIMARY KEY,
            measure_name TEXT UNIQUE
            );""")
cur.execute("""CREATE TABLE IF NOT EXISTS ingredients (
            ingredient_id INTEGER PRIMARY KEY,
            ingredient_name TEXT NOT NULL UNIQUE
            );""")
cur.execute("""CREATE TABLE IF NOT EXISTS meals (
            meal_id INTEGER PRIMARY KEY,
            meal_name TEXT NOT NULL UNIQUE
            );""")
cur.execute("""CREATE TABLE IF NOT EXISTS recipes (
            recipe_id INTEGER PRIMARY KEY,
            recipe_name TEXT NOT NULL,
            recipe_description TEXT
            );""")
cur.execute("""CREATE TABLE IF NOT EXISTS serve (
            serve_id INTEGER PRIMARY KEY,
            meal_id INTEGER NOT NULL,
            recipe_id INTEGER NOT NULL,
            FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
            FOREIGN KEY(meal_id) REFERENCES meals(meal_id)
            );""")
cur.execute("""CREATE TABLE IF NOT EXISTS quantity (
            quantity_id INTEGER PRIMARY KEY,
            quantity INTEGER NOT NULL,
            recipe_id INTEGER NOT NULL,
            measure_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),
            FOREIGN KEY(measure_id) REFERENCES measures(measure_id),
            FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id)
            );""")
conn.commit()
conn.row_factory = sqlite3.Row

data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
            "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
            "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

parser = argparse.ArgumentParser(description="This program prints recipes \
consisting of the ingredients you provide.")

parser.add_argument("-i", "--ingredients", type=str,
                    help="You need to choose only one ingredient from the list.")
parser.add_argument("-m", "--meals", type=str,
                    help="You need to choose only one ingredient from the list.")
parser.add_argument('food_blog.db', nargs='?', default='')


args = parser.parse_args()
if len(sys.argv) > 3:

    not_ingredients = args.ingredients.split(",")
    not_meals = args.meals.split(",")
    ingredients = [[i] for i in not_ingredients]
    meals = [[i] for i in not_meals]



    def find_a_recipe(ingredients, meals):
        bad_data = False
        for i in not_ingredients:
            if i not in data["ingredients"]:
                bad_data = True
            else:
                continue
        for i in not_meals:
            if i not in data["meals"]:
                bad_data = True
            else:
                continue
        if not bad_data:
            ingredients_id_list = []
            ingredients_query = "SELECT ingredient_id FROM ingredients WHERE ingredient_name = (?)"
            for i in range(len(ingredients)):
                ingredients_id_list.append(cur.execute(ingredients_query, ingredients[i]).fetchone()[0])
            meals_id_list = []
            meals_query = "SELECT meal_id FROM meals WHERE meal_name = (?)"
            for i in range(len(meals)):
                meals_id_list.append(cur.execute(meals_query, meals[i]).fetchone()[0])
            ingredients_matching_recipes = []
            if len(ingredients_id_list) > 1:
                ingr_rec_query = """SELECT DISTINCT recipe_id
                                 FROM quantity AS rec_quantity
                                 WHERE ingredient_id = (?)
                                 AND EXISTS (SELECT recipe_id
                                 FROM quantity
                                 WHERE ingredient_id = (?) AND recipe_id = 		 rec_quantity.recipe_id);"""
            else:
                ingr_rec_query = """SELECT recipe_id
                                 FROM quantity
                                 WHERE ingredient_id = (?)"""

            ingr_recipes = cur.execute(ingr_rec_query, ingredients_id_list).fetchall()
            for row in ingr_recipes:
                ingredients_matching_recipes.append(row[0])
            meals_matching_recipes = []
            if len(meals_id_list) > 1:
                meal_rec_query = """SELECT DISTINCT recipe_id
                                 FROM serve AS rec_serve
                                 WHERE meal_id = (?)
                                 AND EXISTS (SELECT recipe_id
                                 FROM serve
                                 WHERE meal_id = (?) AND recipe_id = rec_serve.recipe_id);"""
            else:
                meal_rec_query = "SELECT recipe_id FROM serve WHERE meal_id = (?)"
            meal_recipes = cur.execute(meal_rec_query, meals_id_list).fetchall()
            for row in meal_recipes:
                meals_matching_recipes.append(row[0])
            recipes = set()
            recipes.update(ingredients_matching_recipes)
            recipes.update(meals_matching_recipes)
            recipes = list(recipes)
            rec_query = "SELECT recipe_name FROM recipes WHERE recipe_id = (?)"
            available_recipes = []
            for i in range(len(recipes)):
                available_recipes.append(cur.execute(rec_query, [recipes[i]]).fetchone()[0])
            print("Recipes selected for you: ", end="", flush=True)
            print(*available_recipes, sep=', ')
            conn.close()
        else:
            print("There are no such recipes in the database.")
            conn.close()

    find_a_recipe(ingredients, meals)
else:


    sql = "INSERT INTO measures (measure_name) VALUES (?)"
    val = list(data["measures"])
    val2 = [[x] for x in val]
    cur.executemany(sql, val2)
    conn.commit()

    sql = "INSERT INTO ingredients (ingredient_name) VALUES (?)"
    val = list(data["ingredients"])
    val2 = [[x] for x in val]
    cur.executemany(sql, val2)
    conn.commit()

    sql = "INSERT INTO meals (meal_name) VALUES (?)"
    val = list(data["meals"])
    val2 = [[x] for x in val]
    cur.executemany(sql, val2)
    conn.commit()

    print("Pass the empty recipe name to exit.")

    """
    Loop for inserting recipes to the recipes table
    """

    while True:
        recipe_name = input("Recipe name: ")
        if recipe_name != "":
            recipe_description = input("Recipe description: ")
            print("1) breakfast  2) brunch  3) lunch  4) supper ")
            serving = [int(i) for i in list(input("Enter proposed meals separated by a space: ").split(" "))]
            meals = []
            for i in serving:
                result = cur.execute("SELECT meal_id FROM meals WHERE meal_id = (?)", (i,))
                meals.append(result.fetchone())
            cur.execute("""INSERT INTO recipes (recipe_name, recipe_description)
                            VALUES (?, ?);""", (recipe_name, recipe_description))
            conn.commit()
            rec_id = cur.execute("SELECT * FROM recipes").lastrowid
            for i in meals:
                cur.execute("INSERT INTO serve (meal_id, recipe_id) VALUES (?, ?);", (i[0], rec_id))
            conn.commit()

            """
            Loop for adding ingredients and measures to the quantity table
            in order to link them with inserted recipe
            """

            while True:
                quantity = input("Input quantity of ingredient <press enter to stop>: ")
                if quantity != "":
                    quantity_list = list(quantity.split(" "))
                    try:
                        quantity_list[0] = int(quantity_list[0])
                    except ValueError:
                        print("quantity should be an integer")
                        continue
                    quantity_of_ingredient = quantity_list[0]
                    if len(quantity_list) == 3:
                        measure = quantity_list[1]
                        ingredient = quantity_list[2]
                        values = []
                        for value in data["measures"]:
                            if measure in value:
                                values.append(value)
                        if len(values) == 1:
                            measure = values[0]
                            values = []
                            for value in data["ingredients"]:
                                if ingredient in value:
                                    values.append(value)
                            if len(values) == 1:
                                ingredient = values[0]
                                measure_id = cur.execute("""SELECT measure_id
                                                         FROM measures
                                                         WHERE measure_name in (?)""", [measure]).fetchone()
                                ingredient_id = cur.execute("""SELECT ingredient_id
                                                         FROM ingredients
                                                         WHERE ingredient_name = (?)""", [ingredient]).fetchone()
                                cur.execute("""INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id)
                                            VALUES (?, ?, ?, ?);""", (quantity_of_ingredient, rec_id, measure_id[0], ingredient_id[0]))
                                a = cur.execute("SELECT * FROM quantity").fetchall()
                                print(a)
                                name = "quantity"
                                b = cur.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
                                print(b)
                            else:
                                print("The ingredient is not conclusive!")
                        else:
                            print("The measure is not conclusive!")
                    else:
                        measure = data["measures"][7]
                        ingredient = quantity_list[1]
                        values = []
                        for value in data["ingredients"]:
                            if ingredient in value:
                                values.append(value)
                        if len(values) == 1:
                            ingredient = values[0]
                            measure_id = cur.execute("""SELECT measure_id
                                                     FROM measures
                                                     WHERE measure_name = (?)""", [measure]).fetchone()
                            ingredient_id = cur.execute("""SELECT ingredient_id
                                                        FROM ingredients
                                                        WHERE ingredient_name = (?)""", [ingredient]).fetchone()
                            cur.execute("""INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id)
                                                                    VALUES (?, ?, ?, ?);""",
                                        (quantity_of_ingredient, rec_id, measure_id[0], ingredient_id[0]))
                            a = cur.execute("SELECT * FROM quantity").fetchall()
                            print(a)
                        else:
                            print("The ingredient is not conclusive!")
                else:
                    break
        else:
            break
    conn.commit()
    conn.close()
