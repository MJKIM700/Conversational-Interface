import requests
import nltk
from bs4 import BeautifulSoup
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# ingredient corpuses
beans_and_legumes = ['black bean', 'black-eyed pea', 'cannellini bean', 'chickpea', 'fava bean', 'great northern bean', 'kidney bean', 'lentil bean', 'lima bean', 'pinto bean', 'soybean', 'edamame', 'white bean']
meat_and_poultry = ['beef', 'chicken', 'wild game', 'goat', 'ham', 'lamb', 'pork', 'sausage', 'turkey']
wild_game = ['venison', 'elk', 'duck', 'goose', 'buffalo', 'bison', 'rabbit']
chocolate = ['chocolate', 'cocoa']
oil = ['coconut oil', 'olive oil', 'sesame oil', 'avocado oil', 'vegetable oil', 'canola oil', 'peanut oil', 'oil', 'cooking oil']
dairy = ['cheese', 'butter', 'buttermilk', 'sour cream', 'egg']
extracts = ['vanilla extract', 'anise extract', 'peppermint extract', 'lemon extract', 'orange extract', 'butter extract', 'almond extract', 'maple extract', 'rum extract']
flours = ['white rice flour', 'tapioca flour', 'chickpea flour', 'almond meal', 'coconut flour', 'brown rice flour', 'soy flour', 'corn flour', 'oat flour']
fruit = ['apple', 'apricot', 'avocado', 'banana', 'berry', 'cranberry', 'blueberry', 'raspberry', 'strawberry', 'blackberry', 'cherry', 'citrus', 'lemon', 'orange', 'lime', 'grapefruit', 'coconut', 'dates', 'fig', 'fruit', 'grape', 'kiwi', 'mango', 'melon', 'watermelon', 'cantaloupe', 'honeydew', 'nectarine', 'papaya', 'peach', 'pear', 'persimmon', 'pineapple', 'plum', 'pomegranate', 'raisin', 'tamarind']
herbs = ['basil', 'bay leaves', 'bay leaf' 'chervil', 'chives', 'cilantro', 'dill', 'lemongrass', 'marjoram', 'dill', 'lemongrass', 'marjoram', 'mint', 'oregano', 'parsley', 'rosemary', 'sage', 'savory', 'tarragon', 'thyme', 'lavender', 'rose']
spices = ['seasoning', 'allspice', 'anise', 'annatto', 'cajun', 'caraway', 'cardamom', 'celery seed', 'chili powder', 'cinnamon', 'cloves', 'coriander', 'cumin', 'curry', 'curry powder', 'fennel seed', 'fenugreek', 'garam masala', 'jerk spice', 'mace', 'mustard', 'nutmeg', 'paprika', 'pickling spice', 'poppy seed', 'cayenne pepper', 'saffron', 'sesame seed', 'turmeric', 'vanilla bean', 'white pepper', 'peppercorn', 'ginger', 'star anise']
mushrooms = ['chanterelle mushroom', 'crimini mushroom', 'enoki mushroom', 'morel mushroom', 'oyster mushroom', 'porcini mushroom', 'portobello mushroom', 'shiitake mushroom']
nuts_and_seeds = ['chia seed', 'peanut', 'peanut butter', 'pecan', 'almond', 'flax seed', 'walnut', 'amaranth']
shellfish = ['clam', 'crab', 'crawfish', 'lobster', 'mussel', 'octopus', 'squid', 'oyster', 'scallop', 'shrimp']
vegetables = ['vegetable', 'artichoke', 'artichoke', 'asparagus', 'beet', 'bell pepper', 'bok choy', 'broccoli', 'brussels sprout', 'mushroom', 'green bean', 'corn', 'cucumber', 'eggplant', 'fennel', 'garlic', 'greens', 'green pea', 'pea', 'radish', 'rhubarb', 'sweet potato', 'tomato', 'tomatillo', 'nopales', 'turnip', 'snow pea', 'sugar snap pea', 'potato', 'squash', 'carrot', 'mixed vegetable', 'cauliflower', 'cabbage', 'leek', 'onion', 'parsnip', 'rutabaga', 'shallot', 'yam', 'water chestnut', 'jicama', 'okra', 'chile pepper', 'olive', 'celery root', 'celery']
grain = ['barley', 'rice', 'buckwheat', 'bulgur', 'cornmeal', 'millet', 'oat', 'quinoa', 'spelt']
carbs = grain + ['noodles', 'bread', 'tortillas', 'noodle', 'tortilla', 'pasta']
misc = ['salt', 'black pepper', 'water', 'sugar', 'vinegar', 'ketchup', 'mustard', 'soy sauce', 'paste']
fish = ['salmon', 'cod', 'herring', 'mahi-mahi', 'mackerel', 'perch', 'rainbow trout', 'trout', 'sardines', 'bass',
		'striped bass', 'tuna', 'shark', 'swordfish', 'grouper', 'haddock', 'halibut', 'mahi', 'albacore', 'carp',
		'monkfish', 'snapper', 'sole', 'trout', 'rockfish', 'mullet', 'whitefish', 'saltfish', 'marlin', 'kingfish',
		'torsk', 'bonito']
sauces = ['sauce', 'alfredo', 'alfredo sauce', 'chutney', 'mayonnaise', 'soy sauce', 'barbecue sauce',
		'mushroom sauce', 'hot sauce', 'peanut sauce', 'hollandaise sauce', 'tomato sauce',
		'pesto', 'agrodolce sauce', 'agrodolce', 'tkemali', 'tkemali sauce', 'tartar', 'tartar sauce',
		'marie rose', 'marie rose sauce', 'demi-glace', 'demi-glace sauce', 'salsa', 'gravy', 'steak sauce',
		'cocktail sauce', 'red sauce', 'white sauce', 'chimichurri', 'marinara', 'marinara sauce',
		'worcestershire sauce', 'worcestershire', 'ketchup', 'mustard', 'hummus', 'tzatziki', 'ragu',
		'teriyaki', 'tahini', 'aioli', 'checca', 'checca sauce', 'amatriciana', 'amatriciana sauce', 'guacamole',
		'fish sauce', 'duck sauce', 'sweet and sour sauce']

MEATS = meat_and_poultry + wild_game + fish

list_of_ingredients = beans_and_legumes + meat_and_poultry + wild_game + chocolate + oil + dairy + extracts + flours + fruit + herbs + spices + mushrooms + nuts_and_seeds + shellfish + vegetables + grain + misc + sauces + fish


URL = 'https://www.allrecipes.com/recipe/17167/sicilian-spaghetti/'
URL = 'https://www.allrecipes.com/recipe/279987/'

def load_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    return soup

def extract_text(soup):
    name = soup.find("h1", class_="headline").text
    #print(name)

    #print('ingredients')
    list_i = []
    ingredients = soup.find_all("span", class_="ingredients-item-name")
    for i in ingredients:
        list_i.append(i.text.strip())
        #print(i.text.strip())
    
    #print('directions')
    list_d = []
    directions = soup.find_all("div", class_="paragraph")
    for d in directions:
        list_d.append(d.text)
        #print(d.text)

    return(name, list_i, list_d)

# CORPORA
ALL_TOOLS = ['grill', 'whisk', 'pot', 'pan', 'dish', 'grater', 'knife', 'board', 'pin', 'skillet', 'griddle', 'blender', 'dish', 'sifter', 'strainer', 'mallet', 'bowl', 'oven', 'stove', 'sheet', 'masher', 'beater', 'wok', 'iron', 'ladle']
# For handling special two word tools
SPEC_TOOLS = ['dish', 'pan', 'pin', 'sheet', 'iron', 'board']
TOOL_PREF = ['baking', 'cookie', 'rolling', 'waffle', 'cutting']
# Methods
ALL_METHODS = ['refrigerate', 'toss', 'sprinkle', 'whisk', 'press', 'bake', 'saute', 'preheat', 'fry', 'boil', 'broil', 'chop', 'cut', 'mash', 'blend', 'tenderize', 'heat', 'preheat', 'chop', 'grate', 'stir', 'shake', 'mince', 'crush', 'squeeze']
# Times
TIME_WORDS = ['minute', 'minutes', 'second', 'seconds', 'hour', 'hours']
# For vegetarian transformations
#MEATS = ['chicken', 'duck', 'venison', 'rabbit', 'bison', 'goat', 'shrimp', 'clams', 'lobster', 'crab', 'beef', 'steak', 'pork', 'ham', 'turkey', 'fish', 'tuna', 'salmon', 'cod', 'lamb']
VEG_PROTEINS = ['tofu', 'beans', 'lentils', 'chickpeas']
# For healthy transformations
UNHEALTHY_ING = ['butter', 'sugar', 'salt', 'oil', 'cheese', 'dressing', 'ketchup', 'mayonnaise']
# Because fractions suck and so does allrecipes.com
fractiondict = {'½':0.5, '⅓':0.333, '⅔': 0.667, '¼':0.25, '¾':0.75, '⅝':0.625, '⅛':0.125, '⅜':0.375, '⅞':0.875, '1 ½':1.5}

# parse_steps calls parse_step on all text in list of steps and returns a dictionary of all steps
def parse_steps(steps, ingredients):
    # Steps dictionary
    # Key is step number, value is another dictionary with key strings ingredients, tools, methods, time
    # Sub dictionary values are lists of strings returned by parse_step
    stepdict = {}
    for i in range(len(steps)):
        stepdict[i+1] = parse_step(steps[i], ingredients)
    return stepdict

# parse_step(str:text, listof str:ingredients) -> tools:listof str, methods:listof str, times: listof str
def parse_step(text, ingredients):

    # Initialize
    text = text.lower()
    step = {}
    step['ingredients'] = []
    step['tools'] = []
    step['methods'] = []
    step['times'] = []

    # Tokenize and tag text using nltk
    tokens = nltk.word_tokenize(text)
    
    # Check verbs for methods and nouns for tools 
    # (can later add ability to check for ingredients once ingr list is made)
    
    for i in range(len(tokens)):
        
        word = tokens[i]

        if word in ALL_TOOLS:
            if word in SPEC_TOOLS and tokens[i-1] in TOOL_PREF:
                step['tools'].append(tokens[i-1] + ' ' + word)
            else:
                step['tools'].append(word)
        if word in TIME_WORDS:
            step['times'].append(tokens[i-1] + ' ' + word)
        if word in ingredients:
            step['ingredients'].append(word)
        if word in ALL_METHODS:
            step['methods'].append(word)
    
    return step

fractiondict = {'½':0.5, '⅓':0.333, '⅔': 0.667, '¼':0.25, '¾':0.75, '⅝':0.625, '⅛':0.125, '⅜':0.375, '⅞':0.875, '1 ½':1.5}

measures = ['tablespoon', 'teaspoon', 'pound', 'cup', 'ounce']

# need to integrate into extract_text
def parse_ingredients(ingredients):
    dict_ingredient = {}
    for i in ingredients:
        match, lst = parse_ingredient(i)
        dict_ingredient[match] = lst
    return dict_ingredient

def parse_ingredient(ingredient):
    # ingredient name
    length = 0
    match = ''
    for i in list_of_ingredients:
        if i in ingredient:
            if len(i) > length:
                match = i
                length = len(i)
    # measure
    measure = ''
    for m in measures:
        if m in ingredient:
            measure = m
    # quantity
    quantity = 0
    tokens = nltk.word_tokenize(ingredient)
    
    for t in tokens:
        if t in fractiondict:
            quantity += fractiondict[t]
        elif t.isnumeric():
            quantity += int(t)   
    if quantity == 0:
        quantity = ''  
    return match, [quantity, measure, '']


def parse_recipe(recipe):
    ingredients = parse_ingredients(recipe[1])
    steps = parse_steps(recipe[2], ingredients.keys())
    return ingredients, steps

def make_human_readable_ingredients(ingredients):
    print('INGREDIENTS:')
    for i in ingredients:
        for x in ingredients[i]:
            if x!='':
                print(x, end=" ")
        print(i)

def make_human_readable_steps(steps):
    print('STEPS:')
    for i in steps:
        print(i)
        for x in steps[i]:
            print(x+':')
            for t in steps[i][x]:
                print(t)
            print('\n')
        print('\n')

def human_format(ingredients, steps):
    make_human_readable_ingredients(ingredients)
    make_human_readable_steps(steps)

validate = URLValidator()

def validate_url(url):
    try:
        validate(url)
        return 0
    except ValidationError as exception:
        return 1

def initialize(url):
        p = load_page(url)
        recipe = extract_text(p)
        name = recipe[0]
        ingredients, steps = parse_recipe(recipe)
        return name, ingredients, steps

def specific_question(question):
    # key_phrases = ["how do I ", "How do I ", "how do i ", "how to ", "How to "]
    key_phrase = 'how do I '
    look_up_phrase = question.partition(key_phrase)[2]
    # add_pluses = look_up_phrase.split(' ').join('+')
    for i in range(len(look_up_phrase)): 
        if (look_up_phrase[i] == ' '): 
            look_up_phrase = look_up_phrase.replace(look_up_phrase[i], '+') 

    google_link = "https://www.google.com/search?q=how+to+" + look_up_phrase

    return google_link

def parse_input(user_input):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(user_input.lower())
    if 'how' in tokens:
        if len(tokens) <= 4:
            #TODO handle how do i do that?
            pass
        else:
            link = specific_question(user_input)
            print("I found this reference for you: " + link)
            return 'recipe'
    if 'yes' in tokens:
        pass #TODO handle recipe next step

    if 'ingredients' in tokens:
        return 'ingredients'
    
    if 'go' in tokens or 'take' in tokens:
        pass #TODO navigation utterances



def check_exit():
    pass #TODO

def ingredients_dump(name, ingredients):
    print("The ingredients of " + name + " recipe are:")
    for key in ingredients.keys():
        value = ingredients[key]
        print(str(value[0]) + ' ' + value[1] + ' ' + key)

def listener(name, ingredients, steps):
    exit = False
    previous_output = 'intro'
    curr_step = 0 #for recipe
    while not exit:
        if previous_output == 'intro':
            user_input = input("Thanks for choosing " + name + ". Would you like to [1] go over the ingredients or [2] go over the recipe steps? ")
            while user_input != '1' and user_input != '2':
                user_input = input("Invalid input! Try entering it again. Would you like to [1] go over the ingredients or [2] go over the recipe steps? ")
            
            if user_input == '1':
                previous_output = 'ingredients'
                
            if user_input == '2':
                previous_output = 'recipe'
                #TODO handle recipe

        if previous_output == 'ingredients':
            ingredients_dump(name, ingredients)
            user_input = input("Would you like me to go to the recipe steps? ")
            previous_output = parse_input(user_input) #TODO parse_intput

        if previous_output == 'recipe':
            user_input = input("Would you like me to continue the recipe steps? ") #TODO add step number
            previous_output = parse_input(user_input)  # TODO parse_intput

        exit = check_exit() #TODO make exit conditions


if __name__ == "__main__":
    # execute only if run as a script
    recipe_link = input("enter recipe url: ")
    invalid = validate_url(recipe_link)
    while invalid:
        recipe_link = input("Invalid URL! Try entering it again.")
        invalid = validate_url(recipe_link)
    name, ingredients, steps = initialize(recipe_link)
    print(name, ingredients, steps)

    listener(name, ingredients, steps)