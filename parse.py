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
pastas = ['spaghetti', 'linguine', 'penne', 'ziti', 'ditalini', 'elbows', 'farfalle', 'angel hair', 'pastina', 'fusilli', 'tortellini', 'ravioli', 'tagliatelle']
carbs = grain + ['noodles', 'bread', 'tortillas', 'noodle', 'tortilla', 'pasta']
misc = ['salt', 'black pepper', 'bread crumbs', 'water', 'sugar', 'vinegar', 'ketchup', 'mustard', 'soy sauce', 'paste']
fish = ['salmon', 'cod', 'herring', 'mahi-mahi', 'mackerel', 'perch', 'rainbow trout', 'trout', 'sardines', 'bass',
		'striped bass', 'tuna', 'shark', 'swordfish', 'grouper', 'haddock', 'halibut', 'mahi', 'albacore', 'carp',
		'monkfish', 'snapper', 'sole', 'trout', 'rockfish', 'mullet', 'whitefish', 'saltfish', 'marlin', 'kingfish',
		'torsk', 'bonito', "anchovies", "anchovy"]
sauces = ['sauce', 'alfredo', 'alfredo sauce', 'chutney', 'mayonnaise', 'soy sauce', 'barbecue sauce',
		'mushroom sauce', 'hot sauce', 'peanut sauce', 'hollandaise sauce', 'tomato sauce',
		'pesto', 'agrodolce sauce', 'agrodolce', 'tkemali', 'tkemali sauce', 'tartar', 'tartar sauce',
		'marie rose', 'marie rose sauce', 'demi-glace', 'demi-glace sauce', 'salsa', 'gravy', 'steak sauce',
		'cocktail sauce', 'red sauce', 'white sauce', 'chimichurri', 'marinara', 'marinara sauce',
		'worcestershire sauce', 'worcestershire', 'ketchup', 'mustard', 'hummus', 'tzatziki', 'ragu',
		'teriyaki', 'tahini', 'aioli', 'checca', 'checca sauce', 'amatriciana', 'amatriciana sauce', 'guacamole',
		'fish sauce', 'duck sauce', 'sweet and sour sauce']

MEATS = meat_and_poultry + wild_game + fish

list_of_ingredients = beans_and_legumes + meat_and_poultry + wild_game + chocolate + oil + dairy + extracts + flours + fruit + herbs + spices + mushrooms + nuts_and_seeds + shellfish + vegetables + grain + misc + sauces + fish + pastas


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
    step['text'] = []

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
        step['text'] = text
    
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
    lowered = question.lower()
    key_phrases = ["how do i ", "how to "]

    if "how do i " in lowered:
        key_phrase="how do i "
    else: key_phrase="how to "
    
    look_up_phrase = lowered.partition(key_phrase)[2]
    for i in range(len(look_up_phrase)): 
        if (look_up_phrase[i] == ' '): 
            look_up_phrase = look_up_phrase.replace(look_up_phrase[i], '+') 

    google_link = "https://www.google.com/search?q=how+to+" + look_up_phrase

    return google_link

def general_question(user_input, step):
    lowered = user_input.lower()
    key_phrases = ["how do i ", "how to "]

    if "how do i " in lowered:
        key_phrase="how do i "
    else: key_phrase="how to "
    tools = set(step['tools'])
    methods = set(step['methods'])
    ingredients = set(step['ingredients'])

    google_link = "https://www.google.com/search?q=how+to"

    for tool in tools:
        google_link += '+' + tool
    for method in methods:
        google_link += '+' + method
    for ing in ingredients:
        google_link += '+' + ing
    
    return google_link

# curr_step is now a global var
curr_step = 0


def parse_input(user_input, steps):
    global curr_step
    num_steps = len(steps)
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokens = tokenizer.tokenize(user_input.lower())
    if 'how' in tokens:
        if "do that" in user_input:
            link = general_question(user_input, steps[curr_step])
            print("I found this reference for you: " + link)
            return 'recipe'
        else:
            link = specific_question(user_input)
            print("I found this reference for you: " + link)
            return 'recipe'
    if 'yes' in tokens:
        if curr_step < num_steps:
            curr_step += 1
            print("Step " + str(curr_step) + ':')
            print(steps[curr_step]['text'])
            # check if last step
            if curr_step == num_steps:
                    print('That was the last step.')
                    return "done"
            return 'recipe'
        else:
            return "invalid"

    if 'no' in tokens:
        return 'done'

    if 'ingredients' in tokens:
        return 'ingredients'
    
    if 'go' in tokens or 'take' in tokens:
        if 'next' in tokens:
            if curr_step < num_steps:
                curr_step += 1
                print("Step " + str(curr_step) + ':')
                print(steps[curr_step]['text'])
                if curr_step == num_steps:
                    print('That was the last step.')
                    return "done"
                return 'recipe'
            else:
                #error checking: cannot access a step above num_steps
                print("There are no further steps.")
                return "invalid step number"
        elif 'previous' in tokens:
            if curr_step >= 1:
                curr_step -= 1
                print("Step " + str(curr_step) + ':')
                print(steps[curr_step]['text'])
                return 'recipe'
            else:
                # error checking: cannot access a step below 1
                print("There are no previous steps.")
                return "invalid step number"
        elif 'step' in tokens:
            idx = tokens.index('step')
            target_step = int(tokens[idx+1])
            if target_step > 0 and target_step <= num_steps:
                curr_step = int(tokens[idx+1])
                print("Step " + str(curr_step) + ':')
                print(steps[curr_step]['text'])
                if curr_step == num_steps:
                    print('That was the last step.')
                    return "done"
                return 'recipe'
            else:
                #error checking, step number outside bounds
                return 'invalid step number'
        else:
            #triggers with a malformed step request
            return 'invalid'


    if 'quit' in tokens:
        return 'exit'
    
    # general catch-all for malformed queries
    return 'invalid'

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
    global curr_step
    while not exit:
        if previous_output == 'intro':
            user_input = input("Thanks for choosing " + name + ". Would you like to [1] go over the ingredients or [2] go over the recipe steps? ")
            while user_input != '1' and user_input != '2':
                user_input = input("Invalid input! Try entering it again. Would you like to [1] go over the ingredients or [2] go over the recipe steps? ")
            
            if user_input == '1':
                previous_output = 'ingredients'
                
            if user_input == '2':
                previous_output = parse_input('yes', steps)
                #TODO handle recipe

        if previous_output == 'ingredients':
            ingredients_dump(name, ingredients)
            user_input = input("Would you like me to go to the recipe steps? ")
            previous_output = parse_input(user_input, steps)

        if previous_output == 'recipe':
            user_input = input("Would you like me to continue the recipe steps? ")
            previous_output = parse_input(user_input, steps)

        if previous_output == 'invalid step number':
            # handles when a user attempts to navigate to an invalid step
            user_input = input('You tried to access a step that does not exist. Try something else: ')
            previous_output = parse_input(user_input, steps)
        
        if previous_output == 'done':
            # Done with steps or user says "no" to a question
            user_input = input("If you have any other requests, give them now. If not, respond with 'quit'. ")
            previous_output = parse_input(user_input, steps)
        
        if previous_output == 'exit':
            # When they enter "quit", exit is set to True
            print('Glad to be of service. Hope I was helpful! Goodbye.')
            exit = True
            break

        if previous_output == 'invalid':
            # Handles general invalid input. 
            user_input = input("Sorry, I didn't quite catch that. What did you say? ")
            previous_output = parse_input(user_input, steps)

        #exit = check_exit() #TODO make exit conditions

if __name__ == "__main__":
    # execute only if run as a script
    print("Hello! My name is CrockBot, and I'm here to help you cook like a pro. Let's make something delicious!")
    recipe_link = input("Please enter an AllRecipes.com recipe url: ")
    invalid = validate_url(recipe_link)
    while invalid:
        recipe_link = input("Invalid URL! Try entering it again: ")
        invalid = validate_url(recipe_link)
    name, ingredients, steps = initialize(recipe_link)
    #print(name, ingredients, steps)
    listener(name, ingredients, steps)