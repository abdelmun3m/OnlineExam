import  random


#list of questions objects
questionsPoll = []

#list of integers which reprisent questions ids from questions poll
decoding = []

#list of candidates ( fitnes -> number ,sample ->list)
#[candidate , candidate, .... numberOfSamlplesInPopulation]
population = []

#list 0f generations -> (satisfaction, questions ->list )
#[generation , generation]
history = []

sampleSize = 0
numberOfSamlplesInPopulation = 0
NumberOfGenerations = 10
optimalFitnes = 6
context ={}

def startGeneration(_context):
    global context
    context = _context
    global questionsPoll 
    questionsPoll = context["questionsPoll"]
    global sampleSize 
    sampleSize= context["sampleSize"]
    global numberOfSamlplesInPopulation 
    numberOfSamlplesInPopulation = context["numberOfChapters"]
    global decoding 
    decoding= [question.id for question in questionsPoll]
    global NumberOfGenerations 
    NumberOfGenerations= context["NumberOfGenerations"]
    global population
    population = []
    global history
    history = []

    generatePopulations()
    geneticAlgorithm()
    print(maxGeneration())
    return maxGeneration()    


#get random numberOfSamlplesInPopulation questions in a list 
#generate new candidate
#append candidate population
def generatePopulations():
    global decoding
    for i in range(numberOfSamlplesInPopulation): 
        random.shuffle(decoding)
        if len(decoding) >= sampleSize:
            sample = decoding[ 0 : sampleSize]
            decoding = decoding[sampleSize:]
            candidate = (FitnesFunction(sample)  ,sample)
            population.append(candidate) 
    
def geneticAlgorithm():
    global NumberOfGenerations
    global population
    while(satisfaction(population) or NumberOfGenerations > 0):
        newPopulation = []
        for i in range(len(population)):
            x = getCandidate()
            y = getCandidate()
            child1,child2 = reproduce(x,y)
            if child1:
                newPopulation.append(child1) if child1[0] >= optimalFitnes - 2 else newPopulation.append(mutate(child1))
            if child2:
                newPopulation.append(child2) if child2[0] >= optimalFitnes - 2 else newPopulation.append(mutate(child2))
        population = newPopulation
        NumberOfGenerations = NumberOfGenerations-1


#@input _population [(fitnes,sample),(fitnes,sample),...numberOfSamlplesInPopulation]
#return true if all candidates in population fitnes equal optimal fitnes to stop generations creations    
#add genrations to history
def satisfaction(_population):
    global history
    satisfactionRation = 0
    for i in _population:
        satisfactionRation = satisfactionRation+i[0]

    #extraxt question from candidate and add  new generation to history
    listOfQuestion = extractQuestions(_population)
    generation = (satisfactionRation , listOfQuestion) 
    history.append(generation)    
    return 1 if satisfactionRation == numberOfSamlplesInPopulation * optimalFitnes else 0
        
#return a candidate from population 
#the remove it to avoid candidates repetition 
def getCandidate():
    global population
    x = ()
    if len(population) > 0:
        x = random.sample(population , 1)[0]
        population.remove(x)
    return x


#get two candidate 
#select a randome index and reproduce new candidates from the intial candidates
#if intial candidate one or both are empty 
#it return the intial candidates without changes
#else  generate new candidates and return list of new candidates 
def reproduce(candidateX,candidateY):
    if candidateX and candidateY:
        newX,newY = candidateX,candidateY
        if sampleSize > 0:
            index = random.randint(0, sampleSize - 1)
            newX = candidateX[1][0:index]
            newX.extend(candidateY[1][index:])
            newY = candidateY[1][0:index]
            newY.extend(candidateX[1][index:])
            return [( FitnesFunction(newX),newX), ( FitnesFunction(newY) , newY)]
    return candidateX , candidateY

#mutate candidate to get more fitnes
#select random question from candidate list 
#change it with new question from decoded poll
#if  decoded poll is empty then no mutaion
#and return the same candidate
#@input candidate (fitnes,sample)
def mutate(candidate):
    if len(decoding) > 0:
        global decoding
        if sampleSize > 0:
            index = random.randint(0, sampleSize - 1 )
            if len(decoding) > 0:
                mutation = random.sample(decoding , 1)[0]
                decoding.remove(mutation)
                candidate[1][index] = mutation
                return ( FitnesFunction(candidate[1]) ,candidate[1])
    return candidate

#get max generation from history
def maxGeneration():
    max = history[0]
    for i in history:
        if i[0] > max[0]:
            max = i
    return max


#@input population[(),(),...]
#@Output list of question []
def extractQuestions(_population):
    tempList = []
    for i in _population:
        tempList.extend(i[1])
    return tempList



#@input sample [1,2,3,4,5,.....sampleSize]
#Output evaluation of sample out of 6 according the following criterias 
#chapter semetrics, each chapter shout participate with 1 / number of chapters 
#each level participation, each level should partisipate with
# number of question per level / total question per exam 
def FitnesFunction(sample):
     val = (evaluateChaptersemetric(sample)+
     evaluateDificulty(sample)+evaluateSimplicity(sample)+
     evaluateUnderstanding(sample)+
     evaluateRemindering(sample)+
     evaluateCreativity(sample))

     return val




# number of questions per chapter in each sample, the optimal ratio is 
# OR = number of questions per chapter / total exam questions 
# total exam questions =  number of questions per chapter * number of chapters
# OR = 1 / number of chapters
def evaluateChaptersemetric(sample):
    optimalRation = 1 / context["numberOfChapters"]
    counter = {}
    for i in sample:
        chapter = getQuestion(i).chapter.id
        if chapter in counter:
            counter[chapter] +=1
        else:
            counter[chapter] = 1
    sum = 0
    for i in counter.keys():
        sum += optimalRation - counter[i] / len(sample)
    if sum < 0:
        sum *=-1
    return 1 - sum * optimalRation



def evaluateDificulty(sample):
    optimalRation = context["numberOfDefficulty"] / (context["numberOfChapters"] * context["sampleSize"])
    numberOflevelQuestions = 0
    for i in sample:
        question = getQuestion(i)
        if question.difficulty == "d" or question.difficulty == "D":
            numberOflevelQuestions +=1
    Rl = numberOflevelQuestions / len(sample)
    DltaRl = optimalRation - Rl
    if DltaRl < 0:
        DltaRl *=-1
    return 1 - DltaRl

def evaluateSimplicity(sample):
    optimalRation = context["numberOfSimplicity"] / (context["numberOfChapters"] * context["sampleSize"])
    numberOflevelQuestions = 0
    for i in sample:
        question = getQuestion(i)
        if question.difficulty == "s" or question.difficulty == "S":
            numberOflevelQuestions +=1
    Rl = numberOflevelQuestions / len(sample)
    DltaRl = optimalRation - Rl
    if DltaRl < 0:
        DltaRl *=-1
    return 1 - DltaRl
    

def evaluateUnderstanding(sample):
    optimalRation = context["numberOfUnderstanding"] / (context["numberOfChapters"] * context["sampleSize"])
    numberOflevelQuestions = 0
    for i in sample:
        question = getQuestion(i)
        if question.objective == "u" or question.objective == "U":
            numberOflevelQuestions +=1
    Rl = numberOflevelQuestions / len(sample)
    DltaRl = optimalRation - Rl
    if DltaRl < 0:
        DltaRl *=-1
    return 1 - DltaRl



def evaluateRemindering(sample):
    optimalRation = context["numberOfRemindering"] / (context["numberOfChapters"] * context["sampleSize"])
    numberOflevelQuestions = 0
    for i in sample:
        question = getQuestion(i)
        if question.objective == "r" or question.objective == "R":
            numberOflevelQuestions +=1
    Rl = numberOflevelQuestions / len(sample)
    DltaRl = optimalRation - Rl
    if DltaRl < 0:
        DltaRl *=-1    
    return 1 - DltaRl

def evaluateCreativity(sample):
    optimalRation = context["numberOfCreativity"] / (context["numberOfChapters"] * context["sampleSize"])
    numberOflevelQuestions = 0
    for i in sample:
        question = getQuestion(i)
        if question.objective == "c" or question.objective == "C":
            numberOflevelQuestions +=1
    Rl = numberOflevelQuestions / len(sample)
    DltaRl = optimalRation - Rl
    if DltaRl < 0:
        DltaRl *=-1
    return 1 - DltaRl

def getQuestion(id):
    for i in questionsPoll:
        if i.id == id:
            return i
