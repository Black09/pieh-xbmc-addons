import xbmcaddon
import simplejson as json
from Utils import log, GetStringFromUrl
import urllib

bandsintown_apikey = 'xbmc_test'

def HandleResult(results):
    events = []
    
    for event in results:
        date = event['datetime']
        venue = event['venue']
        city = venue['city']
        name = venue['name']
        region = venue['region']
        country = venue['country']
        
        artists = event['artists']
        my_arts = []
        for art in artists:
            art_tmp = {}
            art_tmp['name'] = art['name']
            art_tmp['mbid'] = art['mbid']
            my_arts.append(art_tmp)
        
        event = {'date': date, 'city': city, 'name':name, 'region':region, 'country':country, 'artists':my_arts  }
        events.append(event)
        
    return events
    

def GetEvents(id):
    url = 'http://api.bandsintown.com/artists/mbid_%s/events?format=json&app_id=%s' % (id, bandsintown_apikey)
    response = GetStringFromUrl(url)
    results = json.loads(response)
    
    return HandleResult(results)

def GetNearEvents():
    settings = xbmcaddon.Addon(id='script.ExtraMusicInfo')
    country = 'Poland' #settings.getSetting('country')
    city = 'Wroclaw' #settings.getSetting('city')
    url = 'http://api.bandsintown.com/events/search?format=json&location=use_geoip&app_id=%s' % (bandsintown_apikey)
    
    log('request: %s' % url)
    
    response = GetStringFromUrl(url)
    results = json.loads(response)
    
    return HandleResult(results)

def GetNearEvents(Artists):
    settings = xbmcaddon.Addon(id='script.ExtraMusicInfo')
    
    ArtistStr = ''
    for art in Artists:
        if len(ArtistStr) > 0:
             ArtistStr = ArtistStr + '&'
        
        ArtistStr = ArtistStr + 'artists[]=' + urllib.quote(art['name'])     
        
    Artists
    
    url = 'http://api.bandsintown.com/events/search?%sformat=json&location=use_geoip&app_id=%s' % (ArtistStr, bandsintown_apikey)
    
    log('request: %s' % url)
    
    response = GetStringFromUrl(url)
    results = json.loads(response)
    
    return HandleResult(results)
