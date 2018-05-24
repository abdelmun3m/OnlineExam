from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200,unique = True)
    number_of_chapters = models.IntegerField(default=0)

    def generateChapters(self):
        for i in range(int(self.number_of_chapters)):
            name = "Chapter "+str(i+1)
            self.chapter_set.create(name=name)

class Chapter(models.Model):
    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
    verbose_name="chapter's course")

    def __str__(self):
        return self.name
DIFFICULTY_LEVELS = (
        ('d', 'Difficult'),
        ('s', 'Simple'),
    )
OBJECTIVE_LEVEL = (
        ('r','Reminding'),
        ('u','Understanding'),
        ('c','Creativity')
    )
class Question(models.Model):
    
    question = models.CharField(max_length=200)
    choice1 = models.CharField(max_length=200 , default="")
    choice2 = models.CharField(max_length=200,default="")
    choice3 = models.CharField(max_length=200,default="")
    answer = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_LEVELS)
    objective = models.CharField(max_length=1, choices=OBJECTIVE_LEVEL)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,
    verbose_name="Question's Chapter")

    def setLevels(self,category):
        levels = category.split(" ")
        for i in  DIFFICULTY_LEVELS:
            if(i[1] == levels[1]):
                self.difficulty = i[0]

        for i in OBJECTIVE_LEVEL:
            if(i[1] == levels[0]):
                self.objective = i[0]


class Exam(models.Model):
    grade = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,
    verbose_name="This exam for Course ")
    questions = models.ManyToManyField(
        Question,
    verbose_name="Exam Questions ")

