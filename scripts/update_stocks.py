import json, datetime, requests
from zoneinfo import ZoneInfo
SYMS=[("NCLH","Norwegian Cruise Line"),("LYFT","Lyft"),("CRWV","CoreWeave"),("SPY","S&P 500 (SPY)"),("QQQ","Nasdaq (QQQ)"),("CL=F","WTI Oil"),("BTC-USD","Bitcoin")]
H={"User-Agent":"Mozilla/5.0"}
d=json.load(open("data.json")); out=[]
for s,n in SYMS:
    try:
        r=requests.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{s}",params={"range":"5d","interval":"1d"},headers=H,timeout=20).json()
        m=r["chart"]["result"][0]["meta"]; p=m["regularMarketPrice"]
        closes=[c for c in r["chart"]["result"][0]["indicators"]["quote"][0]["close"] if c]
        prev=closes[-2] if len(closes)>1 else m.get("chartPreviousClose")
        out.append({"symbol":s,"name":n,"price":round(p,2),"change_pct":round((p-prev)/prev*100,2)})
    except Exception as e:
        old=next((x for x in d.get("stocks",[]) if x["symbol"]==s),None)
        out.append(old or {"symbol":s,"name":n,"price":None,"change_pct":None}); print(s,e)
d["stocks"]=out; d["updated"]=datetime.datetime.now(ZoneInfo("America/New_York")).strftime("%b %d, %Y %I:%M %p ET")
json.dump(d,open("data.json","w"),indent=2)
