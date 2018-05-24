from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .GeneticAlgorithms import startGeneration
import  math 

mulist = [
        {"name":"Course 1","id":1,"numberOfchapters":3},
        {"name":"Course 2","id":2,"numberOfchapters":4},
        {"name":"Course 3","id":3,"numberOfchapters":3},
        {"name":"Course 4","id":4,"numberOfchapters":5},
        {"name":"Course 5","id":5,"numberOfchapters":2},
        {"name":"Course 6","id":6,"numberOfchapters":4},
]

objectives = ["Reminding", "Understanding", "Creativity"] 

difficulty = ["Difficult","Simple"]
categories = []


'''
Route Function to show list of Courses Avilable
@Output render list of current avilable courses
'''
def index(request):
    #return list of Courses
    courses = Course.objects.all()
    context= {"courses":courses}
    return render(request,"Courses/index.html",context)



'''
Route Function to add new post

it will accept the request if it was from Post 
and will redirect to list of courses if GET 

@Input data from add course Form 
@Output call specifyCourse() method that will add course sequience 
'''
def add(request):
    if(request.POST):    
        c= Course(name = request.POST["name"],
            number_of_chapters = request.POST["numberOfchapters"]
        )
        c.save()
        c.generateChapters()
        return redirect("Courses:index")
    else:
        return redirect("Courses:index")




'''
Route Function to show details of Courses
@Input courseId 

@Output render view of current courses data
'''
def detail(request,course_id):
    course= get_object_or_404(Course,pk=course_id)

    print(course.chapter_set.all()[0].question_set.all())
    context={
        "course":course,
    }
    return render(request,"Courses/details.html",context)


'''
Route Function to display form to enter chapter questions
'''
def chapterQuestions(request,course_id,chapter_id):
    list(map( lambda x: categories.extend(x*2) ,[[o+" "+d for d in difficulty] for o in objectives]))
    course= get_object_or_404(Course,pk=course_id)
    chapter= get_object_or_404(Chapter,pk=chapter_id)
    context={
        "course":course,
        "chapter":chapter,
        "categories":categories
    }
    if not chapter.question_set.all():
        return render(request,"Courses/chapter.html",context)

    context = {
        
            "course":course,
            "chapter":chapter
           
    }
    return render(request,"Courses/displayChapter.html",context)


'''
Route Function to handle data submited form chapter questions
form
'''
#TODO validate Repited questions 
def chapterAdd(request,chapter_id):
    if(request.POST):
        chapter = get_object_or_404(Chapter,pk=chapter_id)
        for i in range(12):
            x=str(i+1)
            q = Question()    
            q.question=request.POST["question"+x]
            q.choice1 = request.POST["q"+x+"a1"]
            q.choice2 = request.POST["q"+x+"a2"]
            q.choice3 = request.POST["q"+x+"a3"]
            q.answer = request.POST["Answer"+x]
            q.setLevels(categories[i])
            q.chapter=chapter
            q.save()
        return redirect("Courses:detail" , chapter.course.id)
    else:
        return redirect("Courses:index")



'''
Route Function to diplay customize exam form
'''
def generateExam(request,course_id):
    course= get_object_or_404(Course,pk=course_id)
    context={
        "course":course
    }
    return render(request,"Courses/designExam.html",context)


def generation(request,course_id):
    if(request.POST):
        course = get_object_or_404(Course,pk=course_id)
        poll = Question.objects.filter(chapter__in=course.chapter_set.all())
        
        valid= validateExam(request.POST,len(course.chapter_set.all()) , len(poll))
        
        print("valid",valid)
        
        if not valid[0]:
            print("ssss")
            context ={
                "message": valid[1],
                "course":course,
                "numberOfquestionPerChapter":request.POST["numberOfquestionPerChapter"],
                "Difficult":request.POST["Difficult"],
                "Simple":request.POST["Simple"],
                "Creativity":request.POST["Creativity"],
                "Reminding":request.POST["Reminding"],
                "Understanding":request.POST["Understanding"]
            }
            return render(request,"Courses/designExam.html",context)    
        
        context={
            "questionsPoll":poll,
            "sampleSize":int(request.POST["numberOfquestionPerChapter"]), #question per chapter
            "numberOfChapters":course.number_of_chapters,
            "NumberOfGenerations":100,
            "numberOfDefficulty":int(request.POST["Difficult"]),
            "numberOfSimplicity":int(request.POST["Simple"]),
            "numberOfUnderstanding":int(request.POST["Understanding"]),
            "numberOfRemindering":int(request.POST["Reminding"]),
            "numberOfCreativity":int(request.POST["Creativity"])
        }    

        optimalExam = startGeneration(context)
        exam = Question.objects.filter(id__in=optimalExam[1])
        accuracy =(optimalExam[0] / (6 * context["sampleSize"])) * 100
        print(round(accuracy))
        context = {
            "course":course,
            "questions":exam,
            "accuracy" : accuracy
        }
        return render(request,"Courses/displayExam.html",context)
    else:
        return redirect("Courses:index")


def validateExam(request , chapters,totalquestionsperexam):
    if int(request["Difficult"])+int(request["Simple"])+int(request["Creativity"])+int(request["Reminding"])+int(request["Understanding"]) != int(request["numberOfquestionPerChapter"]) * int(chapters):
        return (0,"total number of question of each levels must equal " + str((int(request["numberOfquestionPerChapter"]) * int(chapters))))
    elif totalquestionsperexam < 12 * chapters:
        return(0,"no enugh questions for each chapter, chaeck that you have entered 12 question per each chapter")
    return (1,"")

