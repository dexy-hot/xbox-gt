import requests
import sys
import os
from halo import Halo
import re
import warnings
import base64
import zlib	
import random
import codecs
import json
import time
import threading
import urllib
import queue as Queue
from multiprocessing.dummy import Pool as ThreadPool
warnings.filterwarnings("ignore") #disable warnings 



headers = {
'User-agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.48 Safari/537.36',
'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Language' : 'en-US,en;q=0.9'
}


codec = 0
errr = 0
fini = False
false = False
true = True
spinner = Halo(text="Request sent",spinner="dots")

q = Queue.Queue()
bob = True


##Small & Simple Multi threading class by Dexy
class MultiThread:
	def __init__(self, function, args):
		self.target = function
		self.threads = []
		self.args = args
	
	def create(self,n):
		for i in range(0,n):
			t = threading.Thread(target=self.target,args=self.args)
			self.threads.append(t)
		return self.threads
	
	def start(self):
		spinner.start("Starting " + str(len(self.threads)) + " threads")
		for thread in self.threads:
			time.sleep(1)
			thread.start()
		spinner.stop()
	def join(self):
		#This will make current window unactive
		for thread in self.threads:
			time.sleep(2)
			thread.join()
		spinner.stop()		

def db64(data, altchars=b'+/'):
    missing_padding = len(data) % 4
    if missing_padding and "=" not in data:
        data += '='* (4 - missing_padding)
    return base64.b64decode(data, altchars)
	
def keyExist(key,value):
	try:
		value = key[value]
		return True 
	except:
		return False

def createThreads(n):
	threads = []
	for i in range(0,n):
		threads.append(i)
	return threads
	
def Login(theprint = True):
	global fini
	if(theprint):
		spinner.start("Logging into account\n")
	global session	
	session = requests.Session()
	if not "false" in proxies:
		proxy = random.choice(proxies)
		session.proxies.update({'https':'https://' + proxy})
		#print(proxy)
	try:
		first = session.get("https://login.live.com/login.srf?",headers=headers,verify=False);
	except:
		fini = True
		print("\n[-] Bad proxy.")
		sys.exit(0)
	flowToken = re.search(r'(?<=value=\")([^\"]*)',first.text)[0]
	uaid = session.cookies['uaid']
	
	
	checkJson = {"username":email,"uaid":uaid,"isOtherIdpSupported":False,"checkPhones":False,"isRemoteNGCSupported":True,"isCookieBannerShown":False,"isFidoSupported":True,"forceotclogin":False,"otclogindisallowed":True,"isExternalFederationDisallowed":False,"isRemoteConnectSupported":False,"federationFlags":3,"flowToken":flowToken}
	
	checkemail = session.post("https://login.live.com/GetCredentialType.srf",json=checkJson,verify=False,headers=headers)
	
	dataPost = {"i13" : "0", "login" : email, "loginfmt" : email, "type" : "11", "LoginOptions" : "3", "lrt" : "", "lrtPartition" : "", "hisRegion" : "", "hisScaleUnit" : "", "passwd" : password, "ps" : "2", "psRNGCDefaultType" : "", "psRNGCEntropy" : "", "psRNGCSLK" : "", "canary" : "", "ctx" : "", "hpgrequestid" : "", "PPFT" : flowToken, "PPSX" : "Passpor", "NewUser" : "1", "FoundMSAs" : "", "fspost" : "0", "i21" : "0", "CookieDisclosure" : "0", "IsFidoSupported" : "1", "i2" : "1", "i17" : "0", "i18" : "", "i19" : "1668743"}
	
	checklogin = session.post("https://login.live.com/ppsecure/post.srf",data=dataPost,headers=headers,verify=False,allow_redirects=False)
	
	if not keyExist(session.cookies,'PPAuth'):
		sys.exit("Couldn't log in")
	b = session.get("https://sisu.xboxlive.com/connect/XboxLive?state=crime&ru=https://social.xbox.com/en-us/changegamertag",headers=headers,allow_redirects=True,verify=False)
	bc = json.loads(db64(re.search(r'(?<=accessToken\=)(.*?)$',b.url)[0].strip()))
	o = bc[0]['Item2']['DisplayClaims']['xui'][0]['uhs']
	global od
	od = bc[0]['Item2']['DisplayClaims']['xui'][0]['xid']
	i = bc[0]['Item2']['Token']
	authorize = "XBL3.0 x=" + o + ";" + i
	headers["x-xbl-contract-version"] = '1'
	headers["authorization"] = authorize
	if(theprint):
		spinner.stop()
	if(theprint):
		print("[+] Logged in")

def intro():
	exec(base64.b64decode("cHJpbnQoIiBfX19fX19fX19fX19fX19fX19fX19fX19fX19fXyAgIikgCnByaW50KCIvICAgICAgICBfX19fX19fX19fX19fICAgICAgICBcICIpIApwcmludCgifCA9PSAuICB8ICAgICAgICAgICAgIHwgICAgIG8gfCAiKSAKcHJpbnQoInwgICBfICAgfCAgICAgICAgICAgICB8ICAgIEIgIHwgIikgCnByaW50KCJ8ICAvIFwgIHwgIFhCT1ggVFVSQk8gfCBBICAgTyB8ICIpIApwcmludCgifCB8IE8gfCB8ICAgICB2MS4zICAgIHwgIE8gICAgfCAiKSAKcHJpbnQoInwgIFxfLyAgfCAgICAgICAgICAgICB8ICAgICAgIHwgIikgCnByaW50KCJ8ICAgICAgIHwgIENvbnRhY3Q6ICAgfCAuIC4gLiB8ICIpIApwcmludCgifCAgOjo6ICB8ICBkZXh5Izc3NDIgIHwgLiAuIC4gfCAiKSAKcHJpbnQoInwgIDo6OiAgfF9fX19fX19fX19fX198IC4gLiAuIHwgIikgCnByaW50KCJ8ICAgICAgICAgICBEIEUgWCBZICAgICAgICAgICB8ICIpIApwcmludCgiXF9fX19fX19fX19fX19fX19fX19fX19fX19fX19fLyAiKQpwcmludCgiICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiKQ=="))




############# This functions is called peridocally to check username.
### At Reserve url
def CheckUsername(name,q):
	change = {"gamertag":name,"reservationId":"" + od + "","targetGamertagFields":"gamertag"}
	d = session.post("https://gamertag.xboxlive.com/gamertags/reserve", json=change,headers=headers,verify=False)  ### THIS HERE CHECKS THE USERNAME 

	global codec
	global errr
	global fini
	codec = d.status_code
	q.put(1)
	checkd = json.loads(d.text)
	

	###If Username is available ChangeUsername is called

	if keyExist(checkd,"composedGamertag") and checkd["composedGamertag"] == name:
		headers["MS-CV"] = d.headers["MS-CV"]
		headers["Referer"] = "https://social.xbox.com/en-us/changegamertag"
		headers["Accept"] = "application/json, text/plain, */*"
		fini = True
		print("\n[+] Username Available!")
		ChangeUsername(name); ##ChangeUsername
		return True
	if d.status_code == 400:
		fini = True
		print("\nGamertag is not accepted");
		sys.exit(0);
	if d.status_code == 429 and "false" in proxies:
		fini = True
		print("\nRate limited")
		sys.exit(0);	
	if not d.status_code == 200:
		errr +=1
		if(errr > 2):
			fini = True
			print("\n[-] Error, bad proxies probably")
			sys.exit(0)
		Login(False)
	if fini == False:
		CheckUsername(name,q)

### This Here Changes the username
def ChangeUsername(name):
	headers["x-xbl-contract-version"] = '6'
	chdata = {"reservationId":od,"gamertag":{"gamertag":name,"gamertagSuffix":"","classicGamertag":name},"preview":False,"useLegacyEntitlement":False}
	
	change = session.post("https://accounts.xboxlive.com/users/current/profile/gamertag",json=chdata,headers=headers,verify=False)
	
	print("[+] Claim made | Response:" + change.text)
	sys.exit(0)
	
intro()

try:
	with open('settings.json') as f:
		settings = json.load(f)
	print("[*] Settings loaded. (" + settings["email"] + ")\n")
	email = settings["email"]
	password = settings["password"]
	proxies = settings["proxy"]
	if not "false" in proxies:
		with open(proxies) as f:
			proxies = f.read().splitlines()
except:
	sys.exit("Can't load settings.")
	
Login()
name = input("Name to Turbo: ")

#####Multiple Threads Here if you have proxies set up
if len(proxies) > 5:
	try:
		nthreads = int(input("How many threads? "))
	except:
		nthreads = 5
else:
	nthreads = 1
threads = MultiThread(CheckUsername,[name,q])
threads.create(nthreads)
threads.start()

	
try:
	while True:
		time.sleep(1)
		spinner.start('Requests: ' + str(q.qsize()) + ' | Status code: ' + str(codec) )
		if fini == True:
			break
except KeyboardInterrupt:
		pass
		fini = True
		spinner.stop()



