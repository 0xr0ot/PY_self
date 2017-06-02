#soup
soup = BeautifulSoup(html, 'lxml')
print(type(soup))


#lxml
from lxml import etree
tree = etree.HTML(html)
print(type(tree))

t1 = time.time()
for i in range(10000):
    td1 = tree.cssselect('#places_continent__row > td.w2p_fw > a')
t2 = time.time()
for j in range(10000):                    
    td2 = tree.xpath('//*[@id="places_continent__row"]/td[2]/a')[0]
t3 = time.time()
#print(td2.text,'\n',type(td2.attrib))
print('cssselect_time: {0}; xpath_time: {1}'.format(t2-t1,t3-t2))

#output: 4.3s,1.9s
