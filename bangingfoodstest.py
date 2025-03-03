import random

# Define meal dictionaries with placeholders for ingredients
BANGING_DINNERS = {
    "SWEET AND SOUR PORK": ["PORK", "MUSHROOMS", "GREEN BEANS"],
    "BRAISED TOFU": ["TOFU", "SPRING ONIONS", "PAK CHOI", "MUSHROOMS"],
    "CHICKEN PICCATA": ["LEMON", "GARLIC", "WHITE WINE", "CHICKEN BREAST", "CAPERS", "LINGUINI"],
    "KATSU CURRY": ["BREADED CHICKEN", "CARROTS", "ONIONS", "CURRY SAUCE BLOCKS", "PICKLED CABBAGE", "GREEN BEANS"],
    "CRISPY TOFU WITH GLAZE": ["ORANGE JUICE", "MAPLE SYRUP", "TOFU", "BROCCOLI", "MUSHROOMS"],
    "SAD PASTA": ["ORZO", "CREAM", "TOMATOES", "PEPPERS", "LEMON", "BROCCOLI", "MUSHROOMS"],
    "CHOW MEIN": ["ONION", "PEPPERS", "NOODLES", "CHICKEN BREASTS", "TENDERSTEM BROCCOLI"],
    "ROASTED GNOCCHI WITH RICOTTA": ["RICOTTA", "GNOCCHI", "TOMATO", "PEPPER", "BROCCOLI", "LEMON"],
    "COURGETTE RICOTTA PASTA": ["RICOTTA", "LINGUINI", "COURGETTE", "LEMON"],
    "TANTAMEN RAMEN": ["PORK MINCE", "MUSHROOMS"],
    "SALMON AND POTATOES": ["SALMON", "POTATOES", "BROCCOLI", "SPINACH"],
    "BEEF BROCCOLI": ["BEEF", "BROCCOLI", "MUSHROOMS"],
    "PIRI PIRI CHICKEN": ["CHICKEN", "CHIPS"],
    "BURGERS": [],
    "SEABASS WITH RICE": [],
    "ROASTED VEG ORZO": [],
    "GOCHUJANG PASTA": [],
    "CARBONARA": [],
    "PANCETTA LEMON PEPPER PASTA": [],
    "ADOBO": [],
    "TORTELLINI": []
}

LAZY_DINNERS = {}

BANGING_LUNCHES = {
    "ROASTED VEG PASTA SALAD": [],
    "CHOW MEIN": [],
    "CURRY UDON": [],
    "PESTO ROCKET TOMATO MOZZARELLA SANDWICH": [],
    "CHORIZO BROCCOLI PASTA": [],
    "HALLOUMI CURRY": [],
    "INSTANT RAMEN": ["RAMEN PACKET", "MUSHROOMS", "PEPPERS"],
    "LEFTOVERS": []  # Placeholder for dynamic assignment
}

SUNDAY_BREAKFAST = ["TOFU HASH", "HALLOUMI IN PURGATORY", "RANDOM"]

WEEKDAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
LEFTOVER_MEALS = {"SWEET AND SOUR PORK", "CHICKEN PICCATA", "TANTAMEN RAMEN", "ADOBO", "KATSU CURRY", "PESTO ROCKET TOMATO MOZZARELLA SANDWICH", "HALLOUMI CURRY"}

def update_for_eating_out():
    out_days_input = input("Enter days and meals you'll eat out (e.g., 'MONDAY LUNCH, WEDNESDAY DINNER'): ").strip()
    if not out_days_input:
        return {}
    
    out_days_input = out_days_input.split(', ')
    out_days = {}
    for entry in out_days_input:
        try:
            day, meal = entry.split()
            if day.upper() in WEEKDAYS and meal.upper() in {"LUNCH", "DINNER"}:
                out_days.setdefault(day.upper(), []).append(meal.upper())
        except ValueError:
            print(f"Invalid entry: {entry}, please use format 'DAY MEAL'")
    return out_days

def generate_meal_plan(out_days):
    if len(BANGING_LUNCHES) < len(WEEKDAYS) or len(BANGING_DINNERS) < len(WEEKDAYS):
        raise ValueError("Not enough unique meals to generate a full week's meal plan.")
    
    random_lunches = random.sample(list(BANGING_LUNCHES.keys()), len(WEEKDAYS))
    random_dinners = random.sample(list(BANGING_DINNERS.keys()), len(WEEKDAYS) - 2) + random.sample(list(LAZY_DINNERS.keys()), 2)
    random.shuffle(random_dinners)
    
    # Ensure Sunday lunch is from the Sunday breakfast list
    random_lunches[-1] = random.choice(SUNDAY_BREAKFAST)
    
    meal_plan = list(zip(WEEKDAYS, random_lunches, random_dinners))
    
    for i, (day, lunch, dinner) in enumerate(meal_plan):
        if day in out_days:
            if "LUNCH" in out_days[day]:
                meal_plan[i] = (day, "OUT", dinner)
            if "DINNER" in out_days[day]:
                meal_plan[i] = (day, lunch, "OUT")
        elif i > 0:
            prev_day, _, prev_dinner = meal_plan[i - 1]
            if prev_dinner in LEFTOVER_MEALS:
                meal_plan[i] = (day, prev_dinner + " (LEFTOVERS)", dinner)
    
    return meal_plan

def generate_shopping_list(meal_plan):
    shopping_list = {}
    for _, lunch, dinner in meal_plan:
        for meal in [lunch, dinner]:
            if meal == "OUT" or "(LEFTOVERS)" in meal:
                continue
            base_meal = meal.replace(" (LEFTOVERS)", "")
            ingredients = BANGING_LUNCHES.get(base_meal, []) + BANGING_DINNERS.get(base_meal, []) + LAZY_DINNERS.get(base_meal, [])
            for ingredient in ingredients:
                shopping_list[ingredient] = shopping_list.get(ingredient, 0) + 1
    return shopping_list

if __name__ == "__main__":
    out_days = update_for_eating_out()
    meal_plan = generate_meal_plan(out_days)
    shopping_list = generate_shopping_list(meal_plan)

    print("\nMeal Plan:")
    for day, lunch, dinner in meal_plan:
        print(f"{day}: LUNCH - {lunch}, DINNER - {dinner}")

    print("\nShopping List:")
    for item, quantity in shopping_list.items():
        print(f"{item}: {quantity}")
