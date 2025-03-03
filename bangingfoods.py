import random

# Define meal dictionaries with placeholders for ingredients
BANGING_DINNERS = {
    "SWEET AND SOUR PORK": {"ingredients": ["PORK", "MUSHROOMS", "GREEN BEANS"], "leftover_friendly": True},
    "BRAISED TOFU": {"ingredients": ["TOFU", "SPRING ONIONS", "PAK CHOI", "MUSHROOMS"], "leftover_friendly": False},
    "CHICKEN PICCATA": {"ingredients": ["LEMON", "GARLIC", "WHITE WINE", "CHICKEN BREAST", "CAPERS", "LINGUINI"], "leftover_friendly": True},
    "KATSU CURRY": {"ingredients": ["BREADED CHICKEN", "CARROTS", "ONIONS", "CURRY SAUCE BLOCKS", "PICKLED CABBAGE", "GREEN BEANS"], "leftover_friendly": True},
    "CRISPY TOFU WITH GLAZE": {"ingredients": ["ORANGE JUICE", "MAPLE SYRUP", "TOFU", "BROCCOLI", "MUSHROOMS"], "leftover_friendly": False},
    "SAD PASTA": {"ingredients": ["ORZO", "CREAM", "TOMATOES", "PEPPERS", "LEMON", "BROCCOLI", "MUSHROOMS"], "leftover_friendly": False},
    "CHOW MEIN": {"ingredients": ["ONION", "PEPPERS", "NOODLES", "CHICKEN BREASTS", "TENDERSTEM BROCCOLI"], "leftover_friendly": False},
    "ROASTED GNOCCHI WITH RICOTTA": {"ingredients": ["RICOTTA", "GNOCCHI", "TOMATO", "PEPPER", "BROCCOLI", "LEMON"], "leftover_friendly": False},
    "COURGETTE RICOTTA PASTA": {"ingredients": ["RICOTTA", "LINGUINI", "COURGETTE", "LEMON"], "leftover_friendly": False},
    "TANTAMEN RAMEN": {"ingredients": ["PORK MINCE", "MUSHROOMS"], "leftover_friendly": True},
    "BEEF BROCCOLI": {"ingredients": ["BEEF", "BROCCOLI", "MUSHROOMS"], "leftover_friendly": False},
    "PIRI PIRI CHICKEN": {"ingredients": ["CHICKEN", "CHIPS", "TENDERSTEM BROCCOLI"], "leftover_friendly": False},
    "BURGERS": {"ingredients": ["BEEF MINCE","BURGER BUNS", "SALAD", "MUSHROOMS", "POTATOES"], "leftover_friendly": False},
    "SEABASS WITH RICE": {"ingredients": ["SEABASS", "PAK CHOI", "MUSHROOMS"], "leftover_friendly": False},
    "GOCHUJANG PASTA": {"ingredients": ["PRAWNS","PASTA","SPRING ONIONS", "TENDERSTEM BROCCOLI"], "leftover_friendly": False},
    "CARBONARA": {"ingredients": ["PANCETTA", "EGG", "CHEESE", "SALAD", "LINGUINI"], "leftover_friendly": False},
    "ADOBO": {"ingredients": ["CHICKEN THIGHS/PORK", "BAYLEAF", "CABBAGE"], "leftover_friendly": True},
    "HALLOUMI CURRY": {"ingredients": ["HALLOUMI", "PEPPER", "TOMATO", "MUSHROOM", "FLATBREAD"], "leftover_friendly": True}  # Fixed key casing
}

LAZY_DINNERS = {
    "TORTELLINI": {"ingredients": ["TORTELLINI", "LEMON", "BUTTER", "SALAD"], "leftover_friendly": False},
    "PANCETTA LEMON PEPPER PASTA": {"ingredients": ["PANCETTA", "LEMON", "LINGUINI", "JARRED PEPPER", "PARSLEY"], "leftover_friendly": False},
    "ROASTED VEG ORZO": {"ingredients": ["ORZO", "TOMATOES", "MUSHROOMS", "PEPPERS"], "leftover_friendly": False},  # Added missing comma
    "SALMON AND POTATOES": {"ingredients": ["SALMON", "POTATOES", "BROCCOLI", "SPINACH"], "leftover_friendly": False}
}

BANGING_LUNCHES = {
    "CHOW MEIN": [],
    "CURRY UDON": [],
    "PESTO ROCKET TOMATO MOZZARELLA SANDWICH": [],
    "CHORIZO BROCCOLI PASTA": [],
    "LEFTOVERS": []
}

OFFICE_LUNCHES = {
    "SALAD": [],
    "ITALIAN PASTA SALAD": [],
    "INSTANT RAMEN": [],
    "ROASTED VEG PASTA SALAD": [],
    "INSTANT RAMEN": ["RAMEN PACKET", "MUSHROOMS", "PEPPERS"],
}

for meal, details in BANGING_DINNERS.items():
    if details["leftover_friendly"]:
        OFFICE_LUNCHES[f"{meal} LEFTOVERS"] = []

SUNDAY_BREAKFAST = {
    "TOFU HASH": [],
    "HALLOUMI IN PURGATORY": [],
    "RANDOM": []
}

WEEKDAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

def update_for_eating_out():
    out_days_input = input("Enter days and meals you'll eat out (e.g., 'MONDAY LUNCH, WEDNESDAY DINNER'): ").strip()
    if not out_days_input:
        return {}
    
    out_days = {}
    for entry in out_days_input.split(', '):
        try:
            day, meal = entry.split()
            out_days.setdefault(day.upper(), []).append(meal.upper())
        except ValueError:
            print(f"Invalid entry: {entry}, please use format 'DAY MEAL'")
    return out_days

def update_for_office_days():
    office_days_input = input("Enter days you are in the office (e.g., 'MONDAY, WEDNESDAY'): ").strip()
    return set(office_days_input.upper().split(', ')) if office_days_input else set()

def generate_meal_plan(out_days, office_days):
    random_dinners = []
    lazy_dinner_count = max(2, len(office_days))
    available_banging_dinners = list(BANGING_DINNERS.keys())

    for i, day in enumerate(WEEKDAYS):
        next_day = WEEKDAYS[i + 1] if i + 1 < len(WEEKDAYS) else None

        if day in office_days:
            dinner = random.choice(list(LAZY_DINNERS.keys()))  # Lazy dinner on office days
        else:
            leftover_friendly_options = [d for d in available_banging_dinners if BANGING_DINNERS[d]["leftover_friendly"]]

            if next_day in office_days and leftover_friendly_options and random.random() < 0.6:  
                # 60% chance of picking a leftover-friendly dinner before an office day
                dinner = random.choice(leftover_friendly_options)
            else:
                dinner = random.choice(available_banging_dinners)
        
        random_dinners.append(dinner)

    random.shuffle(random_dinners)

    random_lunches = []
    previous_dinner = None

    for i, day in enumerate(WEEKDAYS):
        if previous_dinner and BANGING_DINNERS.get(previous_dinner, {}).get("leftover_friendly"):
            if day in office_days:
                lunch = f"OFFICE LUNCH: LEFTOVERS FROM {previous_dinner}"
            else:
                lunch = f"LEFTOVERS FROM {previous_dinner}"
        else:
            lunch = random.choice(list(BANGING_LUNCHES.keys()) if day not in office_days else list(OFFICE_LUNCHES.keys()))

        random_lunches.append(lunch)
        previous_dinner = random_dinners[i]

    meal_plan = list(zip(WEEKDAYS, random_lunches, random_dinners))

    print("\nMeal Plan:")
    for day, lunch, dinner in meal_plan:
        print(f"{day}: Lunch - {lunch}, Dinner - {dinner}")

    shopping_list = set()
    for _, _, dinner in meal_plan:
        shopping_list.update(BANGING_DINNERS.get(dinner, {}).get("ingredients", []))

    print("\nShopping List:")
    for item in sorted(shopping_list):
        print(f"- {item}")





out_days = update_for_eating_out()
office_days = update_for_office_days()
generate_meal_plan(out_days, office_days)
