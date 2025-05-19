import matplotlib.pyplot as plt
import os
import pandas as pd

def postPerYear(cur):
    '''
    Graph overall posts per year
    '''
    years = []
    counts = []
    countPerYear = cur.execute("select year, sum(nameCount) from names group by year order by year asc")
    
    for rec in countPerYear.fetchall():
        years.append(rec[0]) 
        counts.append(rec[1]) 

    bar = plt.bar(years, counts)
    ylabel = plt.ylabel("Biere")
    title = plt.title("Bierstatistik")  
    
    return bar, ylabel, title

def beerWinner(cur, year):
    '''
    Graph per drinker and post last year
    '''
    names = []
    counts = []
    
    countList = cur.execute(
        "select name, sum(nameCount) from names where year = ? and nameCount != 0 group by name order by sum(nameCount) desc",(year,))
    for rec in countList.fetchall():
        names.append(rec[0])
        counts.append(rec[1])

    # Write Text file 
    header = ["Name","Letztes Jahr"]
    list = zip(names, counts)
    fileName = "beerWinner.xlsx"
    message = writeFile(list, fileName, header)
  
    # Top 10
    length = names.__len__() * (-1) + 10
    del names[length:]
    del counts[length:]
      
    bar = plt.bar(names, counts)
    sticky = plt.xticks(names, rotation=90)
    ylabel =plt.ylabel("Biere")
    title = plt.title('Bierposts von ' + str(year))

    return bar, sticky, ylabel, title, message

def beerWinnerTotal(cur, year):
    '''
    Graph overall per drinker
    '''
    names = []
    counts = []
    countsLastYear = []
    
    nameList = cur.execute(
        "SELECT DISTINCT name, SUM(nameCount) OVER (PARTITION BY name) AS total, FIRST_VALUE(nameCount) OVER (PARTITION BY name ORDER BY year DESC) AS last_value FROM names order by total desc")
    for rec in nameList.fetchall():
        names.append(rec[0])
        counts.append(rec[1])
        countsLastYear.append(rec[2])    
    
    # Write Text file
    header = ["Name","Total",year]
    list = zip(names, counts,  countsLastYear)
    fileName = "beerWinnerTotal.xlsx"
    message = writeFile(list, fileName, header)

    # Top 10
    length = names.__len__() * (-1) + 10
    del names[length:]
    del counts[length:]

    bar = plt.bar(names, counts)
    sticky = plt.xticks(names, rotation=90)
    ylabel = plt.ylabel("Biere")
    title = plt.title('Bierposts Total ')

    return bar, sticky, ylabel, title, message

def beerPosterAllYear(cur, year):
    '''
    Generates an excel file with all posts of the drinkers
    '''
    cur.execute("SELECT DISTINCT year FROM names ORDER BY year")
    years = cur.fetchall()

    # Generate the pivot columns as years
    columns = []
    for year in years:
        columns.append(f"MAX(CASE WHEN year = {year[0]} THEN nameCount END) AS '{year[0]}'")

    columns_str = ", ".join(columns)

    sql = f"""
    SELECT name, {columns_str}, 
       {"+".join([f"COALESCE(MAX(CASE WHEN year = {year[0]} THEN nameCount END), 0)" for year in years])} AS total
    FROM names
    GROUP BY name
    ORDER BY name;
    """

    cur.execute(sql)
    result = cur.fetchall()

    fileName = "beerPostsAllYears.xlsx"
    message = writeFile(result, fileName, header=['Name'] + [str(year[0]) for year in years] + ['Total'])
    return message
    
def brandsLastYear(cur, year):
    '''
    Graph about brands last year
    ''' 
    brands = []
    counts = []
    
    nameList = cur.execute(
        "select brand, beerCount from beers where year = ? and beerCount != 0 order by beerCount desc",(year,)) 
    for rec in nameList.fetchall():
        brands.append(rec[0])
        counts.append(rec[1])

    # write Text file
    header = ["Marke","Letztes Jahr"]
    list = zip(brands, counts)
    fileName = "brandsLastYear.xlsx"
    message = writeFile(list, fileName, header)

    #Top 10
    length = brands.__len__() * (-1) + 10
    del brands[length:]
    del counts[length:]

    bar = plt.bar(brands, counts)
    sticky = plt.xticks(brands, rotation = 90)
    ylabel = plt.ylabel("Posts")
    title = plt.title("Top 10 Biermarken " + str(year))  
    
    return bar, sticky, ylabel, title, message

def brandsTotal(cur):
    '''
    Graph about brands all years
    '''    
    brands = []
    counts = []
    countsLastYear = []
    count = 0
    nameList = cur.execute(
        "SELECT DISTINCT brand, SUM(beerCount) OVER (PARTITION BY brand) AS total, FIRST_VALUE(beerCount) OVER (PARTITION BY brand ORDER BY year DESC) AS last_value FROM beers order by total desc")
    for rec in nameList.fetchall():
        brands.append(rec[0])
        counts.append(rec[1])
        countsLastYear.append(rec[2])
        count += 1

    # write Text file
    header = ["Marke","Total","Last year"]
    list = zip(brands, counts, countsLastYear)
    fileName = "brandsTotal.xlsx"
    message = writeFile(list,fileName, header)
   
    #Top 10
    length = brands.__len__() * (-1) + 10
    del brands[length:]
    del counts[length:]

    bar = plt.bar(brands, counts)
    sticky = plt.xticks(brands, rotation = 90)
    ylabel = plt.ylabel("Posts")
    title = plt.title("Top 10 Biermarken Total")  
    
    return bar, sticky, ylabel, title, message
    
def oneBrandTotal(cur, brand):
    '''
    Graph about one brand all years
    '''
    years = []
    counts = []
    
    nameList = cur.execute("select * from beers where brand = ? ",(brand,))

    for rec in nameList.fetchall():
        years.append(rec[1])
        counts.append(rec[2])

    if years == []:
        title = plt.title("Biermarke nicht gefunden")
    else:     
        title = plt.title(brand)   

    bar = plt.bar(years, counts)
    sticky = plt.xticks(years, rotation = 90)
    ylabel = plt.ylabel("Posts") 

    return bar, sticky, ylabel, title

def writeFile(list, fileName, header):
    '''
    Writes a XLSX File and saves it on the desktop
    '''
    desktopPath = os.path.join(os.path.expanduser("~"),"Desktop")
    filePath = os.path.join(desktopPath, fileName)
    pd.DataFrame(list).to_excel(filePath, header = header, index=False)

    message = "File saved to: " + filePath

    return message