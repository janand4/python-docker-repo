import requests
import math
from bs4 import BeautifulSoup
import codecs
from selenium import webdriver 
import collections
import json
import copy

def alltrails_spider():
##        
     with open('./AllTrailsNYUrls.out') as f:
      content = f.read().splitlines()
      staterank = 1 
      
     for u in content:
         
      try:
          #url ="https://www.alltrails.com/trail/us/new-york/mount-beacon-trail"
          #url = "http://www.alltrails.com/trail/us/florida/wekiwa-springs-loop-trail"
          details = collections.OrderedDict()
          index = collections.OrderedDict()          
          
          url = u
          #source_code = requests.get(url, allow_redirects=False, proxies={'http':'','https':''})   
          source_code = requests.get(url)         
          plain_text = source_code.text
          soup = BeautifulSoup(plain_text, "html.parser")
          
          try:
           details['trailurl'] = soup.find("meta",attrs={'property':'og:url'})["content"]
          except:
           details['trailurl'] = ''

          index['_id']=hash(url) % 1000000000000
          details['id']=hash(url) % 1000000000000
           
          try:
           details['trailname'] = soup.find("meta",attrs={'property':'og:title'})["content"]
          except:
           details['trailname']= ''  
            
          try:
           details['distance'] = float(soup.find("span", class_="distance-icon").get_text().split(' ')[0])
          except:
           details['distance']= '' 
            
            
          try:
           details['difficulty'] = soup.find("span",class_='diff').get_text()
          except:
           details['difficulty']= '' 
           
          try:
           details['routetype'] = soup.find("span",class_="route-icon").get_text()
          except:
           details['routetype']= '' 
            
          try:
           lat = soup.find("meta",attrs={'property':'place:location:latitude'})["content"]
           lon = soup.find("meta",attrs={'property':'place:location:longitude'})["content"]
           details['location'] = {'lat':lat, 'lon':lon}
          except:
           details['location']= '' 
                       
          try:
             elevationgain = float(soup.find("span", class_="elevation-icon").get_text().split(' ')[0])
             if elevationgain:
               details['elevationgain'] = elevationgain
             else:
               details['elevationgain'] = '' 
               pass
          except: 
             details['elevationgain'] = ''  
            
          try:    
           details['area'] = soup.find("span",itemprop='name').get_text()
          except:
           details['area'] =''         

                 
          text= str(soup.find("section",id= "aside-ad").find("script").get_text())
          #print text
          index1 = 0
          index2 = 0
          while index1 < len(text):
            index1 = text.find('googletag.pubads().setTargeting', index1)
            index2 = text.find(';',index2)
            if index1 == -1:
                break
            #print('Index 1 found at', index1)
            #print('Index 2 found at', index2)
            
            extract =  text[index1+31:index2]
            
            
            if 'city' in extract:
                try:
                 details['city'] =  extract.split('[')[1].split(']')[0].replace('_',' ').strip('"')
                except:
                 details['city'] = ''
                
            if 'state' in extract and '_states' not in extract:
                try:
                 details['state'] =  extract.split('[')[1].split(']')[0].replace('_',' ').strip('"')
                except:
                 details['state'] = ''
                 
            
            try:
            
             if 'activity' in extract:
                    
                    allact=[]
                    #allact =  extract.split('[')[1].split(']')[0].split(',')
                    allact =  extract.split('[')[1].split(']')[0]
                    allact = allact.replace('_',' ')
                    allact = '['+ allact + ']'
                    allact = eval (allact)
                    
                    details['activities'] =  allact
            except:
                     details['activities'] =  ''


            try:
            
              if 'feature' in extract:
                    
                    feature=[]
                    
                    feature =  extract.split('[')[1].split(']')[0]
                    feature = feature.replace('_',' ')
                    feature = '['+ feature + ']'
                    feature = eval (feature)
                    
                    details['features'] =  feature
            except:
                     details['features'] =  ''                   
                
            #if 'feature' in extract:
            #    print "feature:" + extract.split('[')[1].split(']')[0] 
                
                                                                                   
            index1 += 31 # +2 because len('ll') == 2
            index2 +=1
            
            
        
          try:
           allactivities= soup.findAll("span",class_="big rounded active")
           activitycount = len(allactivities)
           activities = []
           a = 0
           while a < activitycount:
             activity =  allactivities[a].get_text()
             activities.append(activity)
             a = a+1 
           details['allactivities'] =  activities
          except:
           details['allactivities'] = ''
          
          
                     
          try:
            details['description'] = soup.find("meta",attrs={'property':'og:description'})["content"].strip('\'')
          except:
            details['description']= '' 

          try:
            details['arearank'] = int(soup.find("div",class_="trail-rank").get_text().split('#')[1].strip('\r\t\n').split(' ')[0].strip('\r\t\n'))
          except:
            details['arearank']=''
            
          try:
            details['maxarearank'] = int(soup.find("div",class_="trail-rank").get_text().split('of')[1].strip('\r\t\n').split('trails')[0].strip('\r\t\n'))
          except:
            details['maxarearank']=''
            
          details ['staterank'] = staterank  
          
            
          try:
            details['averagerating'] = float(soup.find("meta",attrs={'itemprop':'ratingValue'})["content"])
          except:
            details['averagerating']= ''          

          try:    
           reviewcount = int(soup.find("span",attrs={'itemprop':'reviewCount'}).get_text())
           details['reviewcount'] = reviewcount
          except:
           details['reviewcount']=''   
       
          if (float(reviewcount) == 0):
              pass
          else:
            counter = math.ceil(float(reviewcount)/20)
           # driver= webdriver.PhantomJS()
            driver = webdriver.PhantomJS(executable_path='/Users/janisha/Desktop/HikingProject/trailrunning/node_modules/phantomjs/lib/phantom/bin/phantomjs')
            if driver:
             driver.get(url)
            else:
                pass
            
          
            i =1 
            try:
             while i <=counter:
              eleml= driver.find_element_by_link_text("Load More")
              eleml.click()
              i=i+1
            except :
             pass 

            html_source = driver.page_source
            rsoup = BeautifulSoup(html_source, "html.parser")
            
            reviewers = rsoup.find_all("div", class_="feed-user-content")
            reviewercount = len(reviewers)
            j = 0
            
            ratings_dict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0}
            #print ratings_dict  
            while j < reviewercount:
                try:
                    reviewerrating = reviewers[j].find("meta",attrs={'itemprop':'ratingValue'})["content"]
                    ratings_dict[int(reviewerrating)] = ratings_dict.get(int(reviewerrating)) + 1
                except:
                    pass
                j = j+1
            
            #details['ratings'] = ratings_dict
            details['ratings'] = [ratings_dict[0],ratings_dict[1],ratings_dict[2],ratings_dict[3],ratings_dict[4]]
            
            
            #elem2 = driver.find_elements_by_xpath('//div[@class="pull-left "]')
            #elem2[1].click()
            elem2 = driver.find_element_by_name('Photos')
            
            elem2.click()

            #html_source2 = driver.page_source
            #psoup = BeautifulSoup(html_source2, "html.parser")
            
            #photocount = psoup.find('div',class_="tab-container").findAll('div',class_="photo-item")
            #print photocount   
            
          #redirectedtext= soup.find("a").get_text()
          try: 
            photo_elem = driver.find_elements_by_xpath('//a[@class="gallery cboxElement"]')
            photos = [] 
            for elem in photo_elem:
                photo = elem.get_attribute('href')
                photos.append(photo)
            details['photos'] = photos
                 
                
          except:
            details['photos'] = ''
              
          print '{"index":' + json.dumps(index) + '}'
          print json.dumps(details)    

          
        
          driver.close()        
          staterank = staterank + 1          
      except:
                      
                staterank = staterank + 1  
                pass 
                raise 
           
                
alltrails_spider()            
























