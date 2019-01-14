import re
from bs4 import BeautifulSoup
import requests
import mysql.connector

r = requests.get('https://bama.ir/car')

soup = BeautifulSoup(r.text, 'html.parser')

name = soup.find_all('select', attrs={'name':'selectedTopBrand'})

res = re.findall(r'<option value="(.+),(.+)">(.+)</option>', str(name[0]))#اولی:کد. دومی:اسم لاتین ماشین. سومی:اسم فارسی ماشین

l = []
a = dict()
b = dict()
for i in range (0, len(res)):
    a[int(res[i][0])] = str(res[i][1]) #دیکشنری اسم فارسی
    b[int(res[i][0])] = str(res[i][2]) #دیکشنری اسم لاتین
for i in range (0, len(res)):
    print ('%s : %i' %(res[i][2], int(res[i][0])))

x = int(input('lotfan kode brande morede nazar ra vared befarmaeed: '))

m0 = requests.get('https://bama.ir/car/%s' %(a[x]))#جهت گرفتن مدلها
soup0 = BeautifulSoup(m0.text, 'html.parser')

model1 = soup0.find_all('li')
res1 = re.findall(r'<li class=.+id="model.+">\s+<a href="/car/.+/(.+)">\s+<span class="navigation-name">(.+)</span>', str(model1))
j = 'no'
if res1 != []:#اگر res1 یک لیست خالی باشد به این معناست که برند مورد نظر فقط یک مدل دارد بنابراین میتوان در همان صفحه ی برند جستجو کرد
    for i in range (0, len(res1)):
        print('%i : %s'%(i, res1[i][1]))
    j = 'yes'
    y = int(input('lotfan kode modele morede nazar ra vared befarmaeed: '))


if j == 'yes':
    m1 = requests.get('https://bama.ir/car/%s/%s' %(a[x], res1[y][0]))#صفحه ی اول 
    m2 = requests.get('https://bama.ir/car/%s/%s?page=2' %(a[x], res1[y][0]))#صفحه ی دوم
    soup1 = BeautifulSoup(m1.text, 'html.parser')#صفحه ی اول
    soup2 = BeautifulSoup(m2.text, 'html.parser')#صفحه ی دوم
if j == 'no':
    res1 = re.findall(r'<li class="" id="model-0">\s+<span class="single-data-rightnavigation">\s+<span class="navigation-name">همه (.+)</span>', str(model1))
    m1 = requests.get('https://bama.ir/car/%s' %(a[x]))#صفحه ی اول 
    m2 = requests.get('https://bama.ir/car/%s?page=2' %(a[x]))#صفحه ی دوم
    soup1 = BeautifulSoup(m1.text, 'html.parser')#صفحه ی اول 
    soup2 = BeautifulSoup(m2.text, 'html.parser')#صفحه ی دوم
    print ('faghat yek model darad : %s'%(res1[0]))

karkard1 = soup1.find_all('p', attrs={'class':'price hidden-xs'})#صفحه ی اول 
karkard2 = soup2.find_all('p', attrs={'class':'price hidden-xs'})#صفحه ی دوم

gheymat1 = soup1.find_all('p', attrs={'class':'cost'})#صفحه ی اول 
gheymat2 = soup2.find_all('p', attrs={'class':'cost'})#صفحه ی دوم


l1 = []
c = 0
for i in karkard1:
    res2 = re.findall(r'کارکرد (.+) کیلومتر', i.text)
    if res2 == ['صفر']:
        l1.append('0')
        c += 1
    elif res2 == []:
        res3 = re.findall(r'<p class="price hidden-xs">(.+)</p>',str(i))
        if res3 == ['کارتکس']:            
            l1.append('kartex')
            c += 1
        if res3 == ['حواله']:            
            l1.append('havaleh')
            c += 1
        if res3 == ['-']:            
            l1.append('-')
            c += 1
    elif res2 != []:        
        l1.append(res2[0])
        c += 1
    if c == 12:
        break
    

l2 = []
if c == 12:
    for i in karkard2:
        res2 = re.findall(r'کارکرد (.+) کیلومتر', i.text)
        if res2 == ['صفر']:
            l2.append('0')
            c += 1
        elif res2 == []:
            res3 = re.findall(r'<p class="price hidden-xs">(.+)</p>',str(i))
            if res3 == ['کارتکس']:            
                l2.append('kartex')
                c += 1
            if res3 == ['حواله']:            
                l2.append('havaleh')
                c += 1
            if res3 == ['-']:            
                l2.append('-')
                c += 1
        elif res2 != []:  
            l2.append(res2[0])
            c += 1
        
        if c == 20:
            break
c = 0
g1 = []
for i in gheymat1:
    res2 = re.findall(r'(.+) تومان', i.text)
    if res2 == []:
        pish = re.findall(r'(.+) پیش', i.text)
        if pish == []:
            g1.append('invalid')
            c += 1
        else:
            g1.append(pish[0])
            c += 1
    else:
        g1.append(res2[0])
        c += 1
    if c == 12:
        break
    

g2 = []
if c == 12:
    for i in gheymat2:
        res2 = re.findall(r'(.+) تومان', i.text)
        if res2 == []:
            pish = re.findall(r'(.+) پیش', i.text)
            if pish == []:
                g2.append('invalid')
                c += 1
            else:
                g2.append(pish[0])
                c += 1
        else:
            g2.append(res2[0])
            c += 1
        
        if c == 20 :
            break

cnx = mysql.connector.connect(user='root', password='201747mat', host='127.0.0.1', database='test')
cursor = cnx.cursor()

if c <= 12:
    if j == 'yes':
        for i in range (0, c):
            cursor.execute('INSERT INTO machin VALUES(\'%s %s\', \'%s\', \'%s\')' %(b[x], res1[y][1], l1[i], g1[i]))
            cnx.commit()

    if j == 'no':
        for i in range (0, c):
            cursor.execute('INSERT INTO machin VALUES(\'%s %s\', \'%s\', \'%s\')' %(b[x], res1[0], l1[i], g1[i]))
            cnx.commit()

if c > 12:
    f = c-12
    if j == 'yes':
        for i in range (0, 12):
            cursor.execute('INSERT INTO machin VALUES(\'%s %s\', \'%s\', \'%s\')' %(b[x], res1[y][1], l1[i], g1[i]))
            cnx.commit()

        for i in range(0, f):
            cursor.execute('INSERT INTO machin VALUES(\'%s %s\', \'%s\', \'%s\')' %(b[x], res1[y][1], l2[i], g2[i]))
            cnx.commit()

    if j == 'no':
        for i in range (0, 12):
            cursor.execute('INSERT INTO machin VALUES(\'%s %s\', \'%s\', \'%s\')' %(b[x], res1[0], l1[i], g1[i]))
            cnx.commit()

        for i in range(0, f):
            cursor.execute('INSERT INTO machin VALUES(\'%s %s\', \'%s\', \'%s\')' %(b[x], res1[0], l2[i], g2[i]))
            cnx.commit()

cnx.close()






