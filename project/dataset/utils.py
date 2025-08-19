import random
from .models import Data

def name_by_gender(gender):
    if gender == "Male":
        return random.choice(MALE_NAME)
    else:
        return random.choice(FEMALE_NAME)

def absences_by_behavior(behavior): #generate number of absences using a gaussian with a mu dependent by behavior
    if behavior == 'Excellent':
        while True:
            x = random.gauss(30, 1)
            if 0 <= x <= 300:
                return x
    if behavior == 'Good':
        while True:
            x = random.gauss(90, 2)
            if 0 <= x <= 300:
                return x
    if behavior == 'Sufficient':
        while True:
            x = random.gauss(120, 2)
            if 0 <= x <= 300:
                return x
    if behavior == 'Poor':
        while True:
            x = random.gauss(200, 3)
            if 0 <= x <= 300:
                return x

def weekly_study_time_generator():
    while True:
        x = round(random.gauss(12,3), 2)
        if 0 <= x <= 20:
                return x
    
def average_grade_by_weekly_study_time(weekly_study_time): #generate average_grade using a gaussian with a mu dependent by weekly_study_time
        while True:
            mu = int(weekly_study_time/2)  #normalyzing to 10 because max(weekly_study_time) is 20
            x = random.gauss(mu, 1)
            if 4 <= x <= 10:
                return x

def mass_data_generation(request,n):
    for _ in range(n):
        gender=random.choice(['Male', 'Female']) 
        weekly_study_time=weekly_study_time_generator()
        behavior = random.choices(population=['Excellent', 'Good', 'Sufficient', 'Poor'],
                                    weights=[0.1, 0.4, 0.4, 0.1],
                                    k=1)[0]
        Data.objects.create(
            user=request.user,
            gender=gender,
            name=name_by_gender(gender),
            surname=random.choice(SURNAME),
            age=random.randint(14, 20),
            weekly_study_time=weekly_study_time,
            absences=absences_by_behavior(behavior),
            average_grade=average_grade_by_weekly_study_time(weekly_study_time),
            behavior=behavior
            )

def search_data(searchdata_form,data_list):
    if searchdata_form.cleaned_data.get('name'):
        data_list = data_list.filter(name__icontains=searchdata_form.cleaned_data['name'])
    if searchdata_form.cleaned_data.get('surname'):
        data_list = data_list.filter(surname__icontains=searchdata_form.cleaned_data['surname'])
    if searchdata_form.cleaned_data.get('min_age') is not None:
        data_list = data_list.filter(age__gte=searchdata_form.cleaned_data['min_age'])
    if searchdata_form.cleaned_data.get('max_age') is not None:
        data_list = data_list.filter(age__lte=searchdata_form.cleaned_data['max_age'])
    if searchdata_form.cleaned_data.get('gender'):
        data_list = data_list.filter(gender=searchdata_form.cleaned_data['gender'])
    if searchdata_form.cleaned_data.get('min_weekly_study_time') is not None:
        data_list = data_list.filter(weekly_study_time__gte=searchdata_form.cleaned_data['min_weekly_study_time'])
    if searchdata_form.cleaned_data.get('max_weekly_study_time') is not None:
        data_list = data_list.filter(weekly_study_time__lte=searchdata_form.cleaned_data['max_weekly_study_time'])
    if searchdata_form.cleaned_data.get('min_absences') is not None:
        data_list = data_list.filter(absences__gte=searchdata_form.cleaned_data['min_absences'])
    if searchdata_form.cleaned_data.get('max_absences') is not None:
        data_list = data_list.filter(absences__lte=searchdata_form.cleaned_data['max_absences'])
    if searchdata_form.cleaned_data.get('min_average_grade') is not None:
        data_list = data_list.filter(average_grade__gte=searchdata_form.cleaned_data['min_average_grade'])
    if searchdata_form.cleaned_data.get('max_average_grade') is not None:
        data_list = data_list.filter(average_grade__lte=searchdata_form.cleaned_data['max_average_grade'])
    if searchdata_form.cleaned_data.get('behavior'):
        data_list = data_list.filter(behavior=searchdata_form.cleaned_data['behavior'])
    if searchdata_form.cleaned_data.get('final_outcome'):
        data_list = data_list.filter(final_outcome=searchdata_form.cleaned_data['final_outcome'])
    return data_list

MALE_NAME = [
    'Luca', 'Marco', 'Andrea', 'Matteo', 'Francesco', 'Giovanni', 'Alessandro', 'Davide', 'Simone', 'Gabriele',
    'Federico', 'Riccardo', 'Lorenzo', 'Tommaso', 'Emanuele', 'Daniele', 'Nicola', 'Stefano', 'Antonio', 'Fabio',
    'Paolo', 'Giuseppe', 'Vincenzo', 'Roberto', 'Salvatore', 'Claudio', 'Enrico', 'Michele', 'Alberto', 'Maurizio',
    'James', 'John', 'Michael', 'David', 'William', 'Richard', 'Joseph', 'Charles', 'Thomas', 'Christopher',
    'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua', 'Kenneth',
    'Kevin', 'Brian', 'George', 'Edward', 'Ronald', 'Timothy', 'Jason', 'Jeffrey', 'Ryan', 'Jacob',
    'Liam', 'Noah', 'Mason', 'Ethan', 'Logan', 'Lucas', 'Jackson', 'Aiden', 'Oliver', 'Elijah',
    'Gabriel', 'Carter', 'Jayden', 'Matthew', 'Isaac', 'Caleb', 'Dylan', 'Nathan', 'Luke', 'Christian',
    'Hunter', 'Aaron', 'Connor', 'Adrian', 'Jonathan', 'Charles', 'Thomas', 'Jeremiah', 'Cameron', 'Robert',
    'Alex', 'Oscar', 'Sebastian', 'Diego', 'Javier', 'Carlos', 'Fernando', 'Luis', 'Hugo', 'Sergio',
    'Mateo', 'Nicolas', 'Juan', 'Miguel', 'Andres', 'Angel', 'Pedro', 'Jose', 'Eduardo', 'Rafael',
    'Vincent', 'Dominic', 'Evan', 'Brandon', 'Justin', 'Aaron', 'Kyle', 'Zachary', 'Thomas', 'Jesse',
    'Nathaniel', 'Bryan', 'Charles', 'Christian', 'Sean', 'Jonathan', 'Cody', 'Austin', 'Luke', 'Jeremy',
    'Adrian', 'Elias', 'Jeremiah', 'Colton', 'Austin', 'Robert', 'Hunter', 'Jason', 'Jordan', 'Angel',
    'Eric', 'Isaiah', 'Caleb', 'Nathan', 'Aaron', 'Owen', 'Thomas', 'Jose', 'Connor', 'Brandon',
    'Cameron', 'Luis', 'Kyle', 'Zachary', 'Jack', 'Eli', 'Isaac', 'Alex', 'Max', 'Adam',
    'Miguel', 'Nolan', 'Sean', 'Xavier', 'Damian', 'Jaxon', 'Ezekiel', 'Carson', 'Micah', 'Jace',
    'Parker', 'Sawyer', 'Roman', 'Luis', 'Axel', 'Theodore', 'Kevin', 'Jonah', 'Jameson', 'Hudson',
    'Tyler', 'Cooper', 'Easton', 'Kayden', 'Jason', 'Nathan', 'Brody', 'Declan', 'Micah', 'Silas',
    'Miles', 'Ezra', 'Emmett', 'Greyson', 'Elias', 'Colin', 'Justin', 'Maxwell', 'Carlos', 'Emmanuel',
    'Ryder', 'Jasper', 'Landon', 'Brayden', 'Jason', 'Amir', 'Marcus', 'Patrick', 'Paul', 'Tristan',
    'Christian', 'Dominic', 'Gianni', 'Lorenzo', 'Stefano', 'Roberto', 'Alessio', 'Dario', 'Giuseppe', 'Fabio',
    'Mattia', 'Salvatore', 'Giorgio', 'Vittorio', 'Simone', 'Enzo', 'Nicolo', 'Carlo', 'Raffaele', 'Leonardo',
    'Tomas', 'Martin', 'Peter', 'Alex', 'David', 'John', 'Tom', 'Oliver', 'Harry', 'Oscar',
    'Charlie', 'George', 'Alfie', 'James', 'Theo', 'William', 'Jack', 'Henry', 'Edward', 'Samuel',
    'Benjamin', 'Mason', 'Logan', 'Jacob', 'Lucas', 'Ryan', 'Ethan', 'Caleb', 'Nathan', 'Owen'
]

FEMALE_NAME = [
    'Giulia', 'Francesca', 'Sara', 'Martina', 'Chiara', 'Alessia', 'Valentina', 'Federica', 'Elena', 'Ilaria',
    'Laura', 'Simona', 'Angela', 'Anna', 'Maria', 'Sofia', 'Claudia', 'Veronica', 'Camilla', 'Eleonora',
    'Paola', 'Cristina', 'Silvia', 'Barbara', 'Roberta', 'Alice', 'Marta', 'Beatrice', 'Nicole', 'Elisa',
    'Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Harper', 'Evelyn',
    'Abigail', 'Emily', 'Ella', 'Elizabeth', 'Camila', 'Luna', 'Sofia', 'Avery', 'Mila', 'Aria',
    'Scarlett', 'Penelope', 'Layla', 'Chloe', 'Victoria', 'Madison', 'Eleanor', 'Grace', 'Nora', 'Riley',
    'Zoey', 'Hannah', 'Hazel', 'Lily', 'Ellie', 'Violet', 'Lillian', 'Zoe', 'Stella', 'Aurora',
    'Natalie', 'Emilia', 'Everly', 'Leah', 'Aubrey', 'Willow', 'Addison', 'Lucy', 'Audrey', 'Bella',
    'Claire', 'Skylar', 'Samantha', 'Paisley', 'Kennedy', 'Kinsley', 'Allison', 'Maya', 'Sarah', 'Madelyn',
    'Adeline', 'Alexa', 'Ariana', 'Elena', 'Gabriella', 'Naomi', 'Alice', 'Sadie', 'Hailey', 'Eva',
    'Emery', 'Autumn', 'Quinn', 'Nevaeh', 'Piper', 'Ruby', 'Serenity', 'Willow', 'Everleigh', 'Cora',
    'Kaylee', 'Lydia', 'Alyssa', 'Gianna', 'Clara', 'Vivian', 'Reagan', 'Madeline', 'Peyton', 'Julia',
    'Rylee', 'Melanie', 'Mackenzie', 'Kennedy', 'Kylie', 'Camila', 'Elliana', 'Maria', 'Alina', 'Rose',
    'Isabelle', 'Morgan', 'Brooke', 'Jasmine', 'Delilah', 'Lila', 'Sienna', 'Molly', 'Margaret', 'Brianna',
    'Kate', 'Alexis', 'Faith', 'Luna', 'Isabel', 'Valeria', 'Ada', 'Eloise', 'Harmony', 'Madilyn',
    'Faith', 'Lola', 'Rebecca', 'Rosemary', 'Addilyn', 'Maya', 'Jade', 'Melody', 'Catherine', 'Esther',
    'Luna', 'Eva', 'Giovanna', 'Rosa', 'Lucia', 'Angelica', 'Martina', 'Diana', 'Alessandra', 'Serena',
    'Caterina', 'Giorgia', 'Monica', 'Elisa', 'Giada', 'Irene', 'Arianna', 'Serena', 'Valeria', 'Carlotta',
    'Federica', 'Simona', 'Giovanna', 'Lara', 'Debora', 'Diana', 'Eleonora', 'Nina', 'Olga', 'Sofia',
    'Yulia', 'Anastasia', 'Tatiana', 'Natalia', 'Ekaterina', 'Irina', 'Daria', 'Alina', 'Maya', 'Elena',
    'Ingrid', 'Astrid', 'Freja', 'Karin', 'Helena', 'Sofia', 'Lena', 'Mira', 'Clara', 'Elsa',
    'Anja', 'Greta', 'Maja', 'Liv', 'Ida', 'Vera', 'Stina', 'Alba', 'Luz', 'Marina',
    'Carmen', 'Isabel', 'Lucia', 'Marta', 'Nuria', 'Rosa', 'Patricia', 'Sandra', 'Sonia', 'Teresa',
    'Cristina', 'Elena', 'Gabriela', 'Irene', 'Laura', 'Miriam', 'Pilar', 'Raquel', 'Silvia', 'Sofia'
]

SURNAME = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
    "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes",
    "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham",
    "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson",
    "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens",
    "Harrison", "Fernandez", "Mcdonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen",
    "Freeman", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter",
    "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks",
    "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Salazar", "Fox",
    "Warren", "Mills", "Meyer", "Rice", "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens",
    "Soto", "Weaver", "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins",
    "Arnold", "Pierce", "Vazquez", "Hansen", "Peters", "Santos", "Hart", "Bradley", "Knight", "Elliott",
    "Cunningham", "Duncan", "Armstrong", "Hudson", "Carroll", "Lane", "Riley", "Andrews", "Alvarado", "Ray",
    "Delgado", "Berry", "Perkins", "Hoffman", "Johnston", "Matthews", "Pena", "Richards", "Contreras", "Willis",
    "Carpenter", "Lawrence", "Sandoval", "Guerrero", "George", "Chapman", "Rios", "Estrada", "Ortega", "Watkins",
    "Greene", "Nunez", "Wheeler", "Valdez", "Harper", "Burke", "Larson", "Santiago", "Maldonado", "Morrison",
    "Franklin", "Carlson", "Austin", "Dominguez", "Carr", "Lawson", "Jacobs", "O’Brien", "Lynch", "Singh",
    "Vega", "Bishop", "Montgomery", "Oliver", "Jensen", "Harvey", "Williamson", "Gilbert", "Dean", "Sims",
    "Espinoza", "Howell", "Li", "Wong", "Reid", "Hanson", "Le", "Mccoy", "Garrett", "Burton",
    "Fuller", "Wang", "Weber", "Welch", "Rojas", "Lucas", "Marquez", "Fields", "Park", "Yang",
    "Little", "Banks", "Padilla", "Day", "Walsh", "Bowman", "Schultz", "Luna", "Fowler", "Mejia",
    "Davidson", "Acosta", "Brewer", "May", "Holland", "Juarez", "Newman", "Pearson", "Curtis", "Cross",
    "Valencia", "Ward", "Wilkins", "Baldwin", "Graves", "Lowery", "Reeves", "Navarro", "Moran", "Morales",
    "Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco",
    "Bruno", "Gallo", "Conti", "De Luca", "Mancini", "Costa", "Giordano", "Rizzo", "Lombardi", "Moretti",
    "Barbieri", "Fontana", "Santoro", "Mariani", "Rinaldi", "Caruso", "Ferraro", "Fabbri", "Galli", "Martini",
    "Leone", "Longo", "Gentile", "Martinelli", "Serra", "Villa", "Cattaneo", "Sala", "Pellegrini", "Farina",
    "Orlando", "Sanna", "Piras", "Lopes", "Grassi", "De Santis", "Monti", "Bellini", "Marchetti", "Valentini",
    "Bernardi", "Benedetti", "Bianco", "Caputo", "Coppola", "Damico", "D’Angelo", "Esposito", "Ferraro", "Ferri",
    "Fiorentino", "Fontana", "Gatti", "Greco", "Lamberti", "Lanzetti", "Lucchese", "Marinelli", "Marino", "Mazzoni",
    "Messina", "Montanari", "Morelli", "Napolitano", "Negri", "Palumbo", "Parisi", "Pellegrino", "Perrone", "Pirozzi",
    "Ruggiero", "Russo", "Santini", "Schiavo", "Serafini", "Silvestri", "Taddei", "Tomaselli", "Valente", "Vitali",
    "Vitale", "Zanetti", "Zito"
]