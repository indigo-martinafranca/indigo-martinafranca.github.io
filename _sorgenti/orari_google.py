"""Legge gli orari dai profili Google dei negozi (Places API New) e scrive hours.json per l'app.
Gira in automatico con GitHub Actions. Chiave in GitHub Secret GOOGLE_PLACES_KEY (mai nel codice)."""
import json, os, sys, urllib.request, datetime
KEY=os.environ.get("GOOGLE_PLACES_KEY")
if not KEY: print("Chiave non impostata: niente da fare"); sys.exit(0)
STORES=json.load(open(os.path.join(os.path.dirname(__file__),"negozi_google.json")))
def req(url,body=None,mask="*"):
  h={"X-Goog-Api-Key":KEY,"X-Goog-FieldMask":mask,"Content-Type":"application/json"}
  r=urllib.request.Request(url,data=json.dumps(body).encode() if body else None,headers=h,method="POST" if body else "GET")
  return json.load(urllib.request.urlopen(r,timeout=30))
hm=lambda p:f'{p.get("hour",0):02d}:{p.get("minute",0):02d}'
def slots_by_day(periods,key):
  out={}
  for p in periods or []:
    o,c=p.get("open"),p.get("close")
    if not o: continue
    k=key(o); close="24:00" if not c else hm(c)
    if c and c.get("day")!=o.get("day") and close=="00:00": close="24:00"
    out.setdefault(k,[]).append([hm(o),close])
  for v in out.values(): v.sort()
  return out
res={"updated":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),"stores":{}}
for s in STORES:
  pid=s.get("placeId")
  if not pid:
    j=req("https://places.googleapis.com/v1/places:searchText",{"textQuery":s["query"],"languageCode":"it"},"places.id,places.displayName,places.formattedAddress")
    if not j.get("places"): print("NON TROVATO:",s["id"]); continue
    p=j["places"][0]; pid=p["id"]; print(f'{s["id"]}: trovato {p["displayName"]["text"]} - {p.get("formattedAddress")} -> {pid}')
  d=req(f"https://places.googleapis.com/v1/places/{pid}?languageCode=it","","id,displayName,regularOpeningHours,currentOpeningHours")
  reg=d.get("regularOpeningHours") or {}
  week=slots_by_day(reg.get("periods"),lambda o:str(o["day"]))
  if not reg.get("periods"): print("Senza orari:",s["id"]); continue
  week={str(i):week.get(str(i),[]) for i in range(7)}
  cur=d.get("currentOpeningHours") or {}
  bydate=slots_by_day(cur.get("periods"),lambda o:"%04d-%02d-%02d"%(o["date"]["year"],o["date"]["month"],o["date"]["day"]) if o.get("date") else None)
  special={}
  for sd in cur.get("specialDays") or []:
    dt=sd.get("date"); 
    if not dt: continue
    k="%04d-%02d-%02d"%(dt["year"],dt["month"],dt["day"]); special[k]=bydate.get(k,[])
  res["stores"][s["id"]]={"name":d.get("displayName",{}).get("text"),"placeId":pid,"week":week,"special":special}
  print(s["id"],"ok",week,special)
out=os.path.join(os.path.dirname(__file__),"..","hours.json")
old=None
try: old=json.load(open(out))
except Exception: pass
if old and {k:v for k,v in old.items() if k!="updated"}=={k:v for k,v in res.items() if k!="updated"}: print("Nessuna modifica"); sys.exit(0)
if res["stores"]: json.dump(res,open(out,"w"),ensure_ascii=False,indent=1)
