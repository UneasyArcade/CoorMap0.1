import pickle
import random
import math
from statistics import mean
from django.shortcuts import render

filename = 'linear_model.sav'
LrReg = pickle.load(open(filename, 'rb'))
#filename = 'Forest_model.sav'
#forest = pickle.load(open(filename, 'rb'))
#filename = 'knn_model.sav'
#knn = pickle.load(open(filename, 'rb'))
 
Ppd=25#Мощность передатчика дБм
Gpd=10#Усиление передатчика дБи
Gpr=10#Усиление приемника дБи
Lv=0.125#Длина волны в метрах
Centr_Circle=[[0,0],[1000,0],[800,400]]#координаты точек доступа
#Функция перевода из дБм в Вт
def СonverdBm(a):
        return math.pow(10,(a/10))/1000
#Функция перевода из дБи в разы
def СonverdBi(a):
        return math.pow(10,(a/10))
#Функция расчета дистанции от приемника до передатчика в свободном пространстве
def Dist(Ppd,Gpd,Gpr,Lv,Ppr):
        Ppd= СonverdBm(Ppd)
        Ppr=СonverdBm(Ppr)
        Gpd=СonverdBi(Gpd)
        Gpr=СonverdBi(Gpr)
        return math.sqrt((Ppd*Gpd*Gpr*math.pow(Lv,2))/(math.pow(4*math.pi,2)*Ppr))

def RSA(num1,num2,num3):
    RSSi=[num1,num2,num3]
    dist=[]
    for obj in RSSi:
        dist.append(Dist(Ppd,Gpd,Gpr,Lv,obj))
    left   = min(Centr_Circle[0][0] - dist[0], Centr_Circle[1][0] - dist[1], Centr_Circle[2][0] - dist[2])
    # крайняя правая точка
    right  = max(Centr_Circle[0][0] + dist[0], Centr_Circle[1][0] + dist[1], Centr_Circle[2][0] + dist[2])
    # крайняя верхняя точка
    top    = min(Centr_Circle[0][1] - dist[0], Centr_Circle[1][1] - dist[1], Centr_Circle[2][1] - dist[2])
    # крайняя нижняя точка
    bottom = max(Centr_Circle[0][1] + dist[0], Centr_Circle[1][1] + dist[1], Centr_Circle[1][1] + dist[2])
    iterations = 10000#число итераций
    # списки для хранения координат x и y
    ListX=[]
    ListY=[]
    # цикл генерации случайно точки и проверки на вписаность в окружности
    for j in range(iterations):
        # случайные координаты в диапозоне ограничивающего прямоугольника
        x =random.uniform(left, right)
        y =random.uniform(top, bottom)
        # про верка на вписаность точки во все 3 окружности
        if ((math.sqrt(((x - Centr_Circle[0][0])**2)+((y -Centr_Circle[0][1])**2))<= dist[0] )and
         (math.sqrt(((x - Centr_Circle[1][0])**2)+((y - Centr_Circle[1][1])**2))<= dist[1] )and
          (math.sqrt(((x - Centr_Circle[2][0])**2)+((y - Centr_Circle[2][1])**2))<= dist[2] )):
            #запись координат
            ListX.append(x)
            ListY.append(y)
    if not ListX:
         return 'Не удалось определить точку пересечения'
    return [mean(ListX), mean(ListY)]
 
def home(request):
    if request.method == 'POST':
        num1 = eval(request.POST['num1'])
        num2 = eval(request.POST['num2'])
        num3 = eval(request.POST['num3'])
        result=[]
        mode= request.POST.get('mode')
        if '1' in mode:
            result=LrReg.predict([[num1,num2,-num3]])
            data={"result_X": round(result[0][0],2), "result_Y": round(result[0][1],2)}
            return render(request,'home.html',data)
        elif '4' in mode:
            result=RSA(num1,num2,num3)
            if 'Не удалось определить точку пересечения' in result:
                return render(request,'home.html', {"Error": result}) 
            data={"result_X": round(result[0],2), "result_Y": round(result[1],2)}
            return render(request,'home.html',data)
    '''
        elif '2' in mode:
            result=forest.predict([[num1,num2,-num3]])
            data={"result_X": round(result[0][0],2), "result_Y": round(result[0][1],2)}
            return render(request,'home.html',data)
 
        elif '3' in mode:
            result=knn.predict([[num1,num2,-num3]])
            data={"result_X": round(result[0][0],2), "result_Y": round(result[0][1],2)}
            return render(request,'home.html',data)
    '''
        
    return render(request,'home.html')

'''
 python manage.py runserver
 pip install scikit-learn==1.2.2
    def post(self,request):
        result_X='555'
        result_Y='1111'
        mode=''
        print(result_X)
        try:
                n1=eval(request.POST.get('num1'))
                n2=eval(request.POST.get('num2'))
                n3=eval(request.POST.get('num3'))
                mode=eval(request.POST.get('mode'))
                if mode==1:
                    result_X=n1+n2+n3
                    result_Y=n1+n2+n3
                elif mode==2:
                    result_X=n1-n2-n3
                    result_Y=n1+n2+n3
                elif mode==3:
                    result_X=n1*n2*n3
                    result_Y=n1+n2+n3
                elif mode==4:
                    result_X=n1/n2/n3
                    result_Y=n1+n2+n3
        except:
            result_X="mode"
        data={"result_X": result_X, "result_Y": result_Y}
        print(mode)
        return render(request, self.template_name, data)   

        env\Scripts\activate.ps1
'''
