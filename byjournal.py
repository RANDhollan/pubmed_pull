from Bio import Entrez

def search(query):
    Entrez.email = 'simon_hollands@hotmail.com'
    handle = Entrez.esearch(db='pubmed', 
                            sort='relevance', 
                            retmax='20000',
                            retmode='xml', 
                            term=query)
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'simon_hollands@hotmail.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


if __name__ == '__main__':
   
    #Not (Comment[Publication Type] OR Letter[Publication Type])
    type="Med_California" #For output naming
    Country="California[ad] AND"
    #Country=""
    #pub_type=" AND Clinical Trial[Publication Type] NOT (Comment[Publication Type] OR Letter[Publication Type] OR Book Reviews[Publication Type])" 
    pub_type=" NOT (Comment[Publication Type] OR Letter[Publication Type] OR Letter[Publication Type])" 
    #NIH = "AND (NIH [gr] OR Research Support, N.I.H., Extramural [pt] OR Research Support, N.I.H., Intramural [pt])"
    NIH = ""
    Term =""
    #Term ="Humans[MeSH Terms] AND"
  
    results={}
    #journals = ['"N Engl J Med"[Journal]','"Lancet"[Journal]','"JAMA"[Journal]','"BMJ"[Journal]','"Ann Intern Med"[Journal]', '"Science"[Journal]', '"Nature"[Journal]', '"Cell"[Journal]']
    #journals = ['"Epidemiology"[Journal]','"Am J Epidemiol"[Journal]','"J Clin Epidemiol"[Journal]','"Am J Public Health"[Journal]','"Int J Epidemiol"[Journal]']
    journals = ['"N Engl J Med"[Journal]','"Lancet"[Journal]','"JAMA"[Journal]','"BMJ"[Journal]','"Ann Intern Med"[Journal]']
  
    names = ['NEJM','Lancet','JAMA','BMJ','Annals']
   # names = ['Epi','AmjEpi','Jclin','AmjPubh','IntJE']
      
    count=0
    j1=-1 # this is to count the number of journal loops which will start at 0. Needed to name files by journal

    for Journal in journals:
     j1=j1+1 
     count=0
     jname=names[j1]
     for year in range(1996,2009):
      for i in range(1,13):
       count=count+1
       j=i+1
       year2=year+1
       if i<12:
        search_item = Term +' ("'+str(year)+'/'+str(i)+'/01"[Date - Publication] : "'+str(year)+'/'+str(j)+'/01"[Date - Publication]) AND '+Country+ Journal + NIH + pub_type
        print search_item
        results[count]=search(search_item)
       else:
        search_item = Term+' AND ("'+str(year)+'/'+str(i)+'/01"[Date - Publication] : "'+str(year2)+'/01/01"[Date - Publication]) AND '+Country+ Journal + NIH + pub_type
        results[count]=search(search_item)

     print count
     dick = {}
     for x in range(1,count+1):
      dick[x] = results[x] ['IdList'] 
  
     outdick={}
     for i in range(1,count+1):
      outdick[i]=len(dick[i])
      print outdick[i]


     import csv

     with open('Trends_'+jname+type+'.csv', 'wb') as f:  # Just use 'w' mode in 3.x
      w = csv.DictWriter(f, outdick.keys())
      w.writeheader()
      w.writerow(outdick)
