# incognito
A tool for retrieving malware samples via TOR or proxy

* Can be run as a stand-alone application
* Can be imported as a module for extended functionality and tailored usage
* Simple API
* Generates random browser user agents for each request

The standalone application currently supports four options:
 
incognito.py --h<br>
usage: incognito.py [-h] [--proxy] [--noproxy] [--url | --file]<br>
optional arguments:<br>
  -h, --help  show this help message and exit<br>
  --proxy     use a proxy instead of TOR (single or list from file)<br>
  --noproxy   do not use TOR or any proxy (request sent from actual ipaddy)<br>
  --url       process single URL.<br>
  --file      process file of URLs.<br>
 
 <p>proxy = Use a specified proxy instead of TOR, for instance your provider/organization does not allow or condone the use of TOR (TOR is enabled by default for all requests).  </p>

<p>noproxy = Exposes your external IP, useful if TOR is block, not allowed, for example if you are automating downloads in a Sandbox or something similar and the remote server is expecting a specific IP address.</p>
 
url = Process a single URL.
 
file = Process a text file of URLs
 
### Data Output
 
Both URL and File options store results in the same format “md5sum_filename”. Each download will also create a similar named file with appended name "_headers.txt". This file is a hash map containing the original requested URL, resolved IP Address and any header information returned by the server. 
 
f28398bb0b8252f310ca548d068349a0_php06_headers.txt Output
 
{'content-length': '25709', 'url': 'hxxp://192.168.82.33/apache2-default/.a/hb/php06', 'ipaddress': '78.109.82.33', 'accept-ranges': 'bytes', 'server': 'Apache/2.2.3 (Debian) PHP/5.2.0-8+etch15 mod_ssl/2.2.3 OpenSSL/0.9.8c', 'last-modified': 'Fri, 24 Oct 2014 21:05:44 GMT', 'connection': 'close', 'etag': '"5baf9-646d-8b501a00"', 'date': 'Wed, 29 Oct 2014 13:55:51 GMT', 'content-type': 'text/plain; charset=UTF-8'}
 
Additionally both output the status of the download and or offline status of the site. The file option creates a directory based on the name of the input file. For example:
 
incognito.py --file<br>
FILE: guide.txt<br>
Results Directory: \_\_guide.txt\_\_<br>
2014-12-01 15:54:18 Processing: hxxp://192.168.144.163/guide/2004.py<br>
Saving File: 0b70ac27fef987cef59e96d59d1dea06_2004.py<br>
2014-12-01 15:54:19 Processing: hxxp://192.168.144.163/guide/20091<br>
Saving File: d3230b025cb346ec71f395d69f97d619_20091
2014-12-01 15:54:52 Processing: hxxp://192.168.144.163/guide/a.out<br>
Saving File: ff1e9d1fc459dd83333fd94dbe36229a_a.out<br>
2014-12-01 15:54:53 Processing: hxxp://192.168.144.163/guide/a.tgz<br>
Saving File: b46bb22b0f9d035169a9515fab10d1f3_a.tgz<br>
 
### Using the API
 
The API by design is meant to be simplistic, only two classes and two functions are available to the user, the core classes are transparent. The API offers more customization over standalone operation outside of the standard options. Users can change the save location and specify a custom or pre-fabricated user-agent from a few popular tools. (This may be needed in times when a remote server is expecting only downloads to occur from specific tools). For convenience the available parameters foreach method are provided, however this information is available from pythons internal help() system.
 
User-Agent keywords: curl, wget, lwp-download, or manually enter a custom agent.
 
The URL class has GetURL() for processing individual requests (url is the only required parameter).
GetURL(self, url, proxy=None, directory=None, noproxy=None, useragent=None)
 
The File class has GetFile() for processing lists of URLs (fileName is the only required parameter).
GetFile(self, fileName, proxy=None, directory=None, noproxy=None, useragent=None)
 
Incorporating Incognito into your own scripts
 
import incognito
nito = incognito.Incognito.URL() = Process URL
nito = incognito.Incognito.File() = Process File
 
nito.GetURL() = Downloads URL based on parameters
nito.GetFile() = Downloads URLs in specified file, based on parameters
 
### Example Usage
 
No proxy configuration (show your real IP Address) plus add custom user-agent
 
nito.GetURL(url,noproxy=1,useragent=”lwp-download”) – Use Perl LWP user-agent
nito.GetURL(url,noproxy=1,useragent=”b0tc4ll1n”) – Use custom botnet phone home user-agent
 
External Proxy
 
nito.GetURL(url,proxy=”192.168.49.76:8080”)
 
Write to Custom Directory (Uses TOR)
 
nito.GetFile(fileName,directory=”/opt/FileRepo”)

Requirements

TOR
Python 2.x
