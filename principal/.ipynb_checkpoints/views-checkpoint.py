from django.shortcuts import render
#from django.http import HttpResponse
import ast
import os
from collections import defaultdict
from deep_translator import GoogleTranslator
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
from collections import defaultdict
# Create your views here.

def about(request):
    return render(request,'about.html')

def home(request):
    return render(request,'home.html')


def busqueda(request):
    # reading the data from the file
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'raiz_ind_inv.txt')
    with open(file_path) as f:
        data = f.read()  
    print("Data type before reconstruction : ", type(data))  
    # reconstructing the data as a dictionary
    dicts = ast.literal_eval(data) 
    print("Data type after reconstruction : ", type(dicts))
    index = defaultdict(list)
    for key, val in dicts.items():
        for subkey, subval in val.items():
            index[subkey].append((key, subval))
    try:
        res = request.GET.get('busqueda')
        indice = GoogleTranslator(source='auto', target='english').translate(res)
        sentencias = indice.split()
        values = ''
        for i in range(len(sentencias)):
            try:
                valuefind=stemmer.stem(sentencias[i])
                print(valuefind)
                aux1 = list(index.keys()).index(valuefind)
                print("aux1")
                print(aux1)
                key = list(index)[aux1]
                print(key)
                
                value = list(index.values())[aux1]
                print(value) 
                longitud = len(list(index.values())[aux1])
                array = []
                arrayurls = []
                for i in range(longitud):
                    array.append(int(list(index.values())[aux1][i][1]))
                    arrayurls.append(list(index.values())[aux1][i][0])
                for i in range(len(array)):
                    for j in range(0, len(array) - i - 1):
                        if array[j] < array[j + 1]:
                            temp = array[j]
                            temp2 = arrayurls[j]
                            array[j] = array[j+1]
                            arrayurls[j] = arrayurls[j+1]
                            array[j+1] = temp
                            arrayurls[j+1] = temp2
                #print(array) 
        
                #print(array)
                #print(arrayurls)
                for i in range(longitud):
                    values += str(arrayurls[i])
                    values += "\n "
                    values += str(valuefind)
                    values += '\n frecuencia solo para fines de ver '
                    values += str(array[i])
                    values += ' \t\n\n'
                #values = arrayurls[0]
            except:
                values="No encontre nada"

        
        
        
    except:
        values="No encontre nada"
        
    
    #list2 = ['cat', 'bat', 'mat', 'cat', 'pet'] 
    #if(request.GET.get('uppercase')):
        #indice = 'pet'
    #int(request.GET.get('busqueda'))
    #indice = list('adc')
    #indice.extend(list('defghi'))
    
    #bat=list2.index(indice)
    return render(request,'busqueda.html',{'busqueda':values})