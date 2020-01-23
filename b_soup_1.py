
from urllib.request import urlopen  # b_soup_1.py
from bs4 import BeautifulSoup

html = urlopen('https://www.treasury.gov/resource-center/'
               'data-chart-center/interest-rates/Pages/'
               'TextView.aspx?data=yieldYear&year=2019')

bsyc = BeautifulSoup(html.read(), "lxml")

fout = open('bsyc_temp.txt', 'wt',
		encoding='utf-8')

fout.write(str(bsyc))

fout.close()

# print the first table
print(str(bsyc.table))
# ... not the one we want

# so get a list of all table tags
table_list = bsyc.findAll('table')

# how many are there?
print('there are', len(table_list), 'table tags')

# look at the first 50 chars of each table
for t in table_list:
    print(str(t)[:50])

# only one class="t-chart" table, so add that
# to findAll as a dictionary attribute
tc_table_list = bsyc.findAll('table',
                      { "class" : "t-chart" } )

# how many are there?
print(len(tc_table_list), 't-chart tables')

# only 1 t-chart table, so grab it
tc_table = tc_table_list[0]

# what are this table's components/children? >> the rows
for c in tc_table.children:
    print(str(c)[:50])

# tag tr means table row, containing table data
# what are the children of those rows? >> they are the cells in each of the rows
for c in tc_table.children:
    for r in c.children:
        print(str(r)[:50])

# we have found the table data!
# just get the contents of each cell
for c in tc_table.children:
    for r in c.children:
        print(r.contents) 


