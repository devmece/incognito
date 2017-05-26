#!/usr/bin/python

"""
    Name:   Incognito
    Author: Ramece Cave
    Email:  rrcave@n00dle.org

    License: BSD

    Copyright (c) 2012,2014 Ramece Cave
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted     
    provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions
    and the following disclaimer. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the documentation and/or other
    materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
    IMPLIED WARRANTIES,INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
    FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
    DAMAGE.
"""

#__version__ = 2.1

from random import choice
import urllib2,sys,os,hashlib,time,socket,re,argparse

class Incognito:
    class URL:
        def __init__(self):
            self.otherAgents = {
                            "wget" : "Wget/1.13.4 (linux-gnu)",
                            "curl" : "curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3",
                            "lwp-download" : "lwp-download/6.00 libwww-perl/6.03"
                          }
            self.dat = lambda: time.strftime("%Y-%m-%d %H:%M:%S")
            self.otype = lambda x: str(type(x)).split("'")[1]
            self.currentWorkingDirectory = os.getcwd()

        def GetURL(self,url,proxy=None,directory=None,noproxy=None,useragent=None):
            """
            Grabs URL and server headers. Information is saved as md5sum_pagename
            and md5sum_pagename_headers.txt in current working directory.

            User-Agent keywords: curl, wget, lwp-download, or manually enter a custom agent.
            """

            url = url.rstrip()
            timestamp = self.dat()
            print timestamp,"Processing:",url

            if proxy and not useragent: #proxy option
                fileName,data,headers = Incognito._GetContent(url,proxy)
            elif proxy and useragent: #proxy option w/useragent
                if otherAgents.has_key(useragent):
                    fileName,data,headers = Incognito._GetContent(url,proxy,useragent=self.otherAgents.get(useragent))
                else:
                    fileName,data,headers = Incognito._GetContent(url,proxy,useragent=useragent)
            elif noproxy and not useragent: #noproxy option
                fileName,data,headers = Incognito._GetContent(url,noproxy=1)
            elif noproxy and useragent: #noproxy option w/useragent
                if self.otherAgents.has_key(useragent):
                    fileName,data,headers = Incognito._GetContent(url,noproxy=1,useragent=self.otherAgents.get(useragent))
                else:
                    fileName,data,headers = Incognito._GetContent(url,noproxy=1,useragent=useragent)
            else:
                if useragent:
                    fileName,data,headers = Incognito._GetContent(url,useragent=useragent)
                else:
                    fileName,data,headers = Incognito._GetContent(url)

            if fileName and data: #data is returned from site (content was available)
                fileName = Incognito._GetFileName(fileName,data)
                print "Saving File:",fileName

                if directory: #Write to specific location
                    Incognito._SaveFile(headers,fileName,data,directory=directory)
                else:
                    Incognito._SaveFile(headers,fileName,data)
            else:
                if proxy:
                    print "Site Unavailable -- Check Proxy"
                else:
                    print "Site Unavailable"

            return

    class File:
        def __init__(self):
            self.otherAgents = {
                            "wget" : "Wget/1.13.4 (linux-gnu)",
                            "curl" : "curl/7.22.0 (x86_64-pc-linux-gnu) libcurl/7.22.0 OpenSSL/1.0.1 zlib/1.2.3.4 libidn/1.23 librtmp/2.3",
                            "lwp-download" : "lwp-download/6.00 libwww-perl/6.03"
                          }
            self.dat = lambda: time.strftime("%Y-%m-%d %H:%M:%S")
            self.otype = lambda x: str(type(x)).split("'")[1]
            self.currentWorkingDirectory = os.getcwd()

        def GetFile(self,fileName,proxy=None,directory=None,noproxy=None,useragent=None):
            """
            Grabs URL and server headers, for each URL listed in the file Information is
            saved as md5sum_pagename and md5sum_pagename_headers.txt in current working
            directory.

            User-Agent keywords: curl, wget, lwp-download, or manually enter a custom agent.
            """

            urlProcessor = Incognito.URL()
            counter = 0 #Track processed URL count

            if directory: #directory option
                saveDir = directory
            else:
                saveDir = "%s/__%s__" % (self.currentWorkingDirectory,fileName.split("/")[-1])

            try:
                fileContents = open(fileName).read().strip().split("\n")
            except:
                print "Error: Unable to read or locate file"
                sys.exit()

            try:
                os.mkdir(saveDir)
                print "Results Directory:",saveDir
            except:
                print "Error: Directory already exists"
                sys.exit()

            for url in fileContents:
                #All options are passed to GetURL() for individual processing.
                try:
                    urlProcessor.GetURL(directory=saveDir,url=url,proxy=proxy,noproxy=noproxy,useragent=useragent)

                    trackLog = "/tmp/%s.incognito" % fileName.split("/")[-1]
                    output = open(trackLog,"w")
                    output.write(str(counter))
                    output.flush() ; output.close()
                    counter += 1
                except:
                    trackLog = "/tmp/%s.incognito" % fileName.split("/")[-1]
                    output = open(trackLog,"w")
                    output.write(str(counter))
                    output.flush() ; output.close()
                    counter += 1
            return

    @staticmethod
    def _ProxySelect(proxy):
        proxyType = self.otype(proxy)

        if proxyType == "list": #Select random proxy from list
            proxyList = proxy
            selectedProxy = choice(proxyList)
            return selectedProxy
        else:
            proxyUrl = proxy
            return proxyUrl
    @staticmethod
    def _ProxyConfig(url,server=None,selection=None):
        if selection == "user":
            proxyServer = Incognito.__ProxySelect(server)
            if url.startswith("https"):
                externalProxy = urllib2.ProxyHandler({"https" : proxyServer})
            else:
                externalProxy = urllib2.ProxyHandler({"http" : proxyServer})
        else:
            #Use local TOR proxy server
            if url.startswith("https"):   
                externalProxy = urllib2.ProxyHandler({"https" : "127.0.0.1:8123"})
            else:
                externalProxy = urllib2.ProxyHandler({"http" : "127.0.0.1:8123"})

        return externalProxy

    @staticmethod
    def _GetContent(url,proxy=None,noproxy=None,useragent=None):
        """
        Connects to Tor and selects a random User Agent.
        Returns fileName and data.
        """
        userAgents = [
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8",
        "Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3",
        "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.5",
        "Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2",
        "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.1.8) Gecko/20100202 Firefox/3.5.8",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; )",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; GTB6.4; SLCC2; .NET CLR 2.0.50727; .NET CLR",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; sk; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)"
        ]

        if (not url.startswith("http://")) and (not url.startswith("https://")):
            url = "http://" + url.replace("%2f","/")
        else:
            url = url.replace("%2f","/")

        fileName = url.split("/")[-1]
        if len(fileName) == 0:
            fileName = "index"

        if proxy:# Use an alternate proxy server, if provided.
            externalProxy = Incognito._ProxyConfig(url,server=proxy,selection="user")
        elif noproxy:
            pass
        else: #Use TOR
            externalProxy = Incognito._ProxyConfig(url,selection="tor")

        if noproxy and not useragent: #Do not use any proxies
            request = urllib2.Request(url)
            request.add_header('User-Agent',choice(userAgents))
        elif noproxy and useragent: #Apply alternate useragent
            request = urllib2.Request(url)
            request.add_header('User-Agent',useragent)
        else:
            if not useragent:
                urlHandler = urllib2.build_opener(externalProxy)
                urllib2.install_opener(urlHandler)
                request = urllib2.Request(url)
                request.add_header('User-Agent',choice(userAgents))
            if useragent:
                urlHandler = urllib2.build_opener(externalProxy)
                urllib2.install_opener(urlHandler)
                request = urllib2.Request(url)
                request.add_header('User-Agent',useragent)
        try:
            data = urllib2.urlopen(request,timeout=5)
        except:
            return 0,0,0

        fileContent = data.read()
        headerInfo = data.info()
        headerKeys = headerInfo.keys()
        headerValues = headerInfo.values()
        headers = dict(zip(headerKeys,headerValues)) #Remove dictionary from object.
        headers['ipaddress'] = Incognito._nslookup(url)
        headers['url'] = url

        return fileName,fileContent,headers

    @staticmethod
    def _GetFileName(oldFileName,data):
        md5sum = hashlib.md5(data).hexdigest()
        newFileName = "%s_%s" % (md5sum,oldFileName) #md5sum,oldFileName

        return newFileName

    @staticmethod
    def _SaveFile(headers,fileName,data,directory=None):
        if directory:
            if not os.path.exists(directory):
                os.mkdir(directory)
            fileName = "%s/%s" % (directory,fileName)

        headersFileName = "%s_headers.txt" % fileName
        headersText = str(headers)
        saveHeaders = open(headersFileName,'w')
        saveHeaders.write(headersText+'\n')
        saveHeaders.flush()
        saveHeaders.close()

        saveData = open(fileName,"wb")
        saveData.write(data)
        saveData.flush()
        saveData.close()

        return

    @staticmethod
    def _nslookup(url):
        ipRegex = "^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"

        if url.startswith("http://"):
            lookup = url.split("/")[2]
        else:
            lookup = url

        try:
            if re.search(ipRegex,lookup):
                #nsResults = socket.gethostbyaddr(lookup)[0]
                nsResults = lookup
            elif not re.search(ipRegex,lookup):
                nsResults = socket.gethostbyname(lookup)
        except:
            nsResults = 0

        return nsResults

    @staticmethod
    def _main():
        """
        CLI: presents and executes options.
        """
        parser = argparse.ArgumentParser()

        #Misc options
        parser.add_argument("--proxy",help="use a proxy instead of TOR (single or list from file)",required=False,action="store_true")
        parser.add_argument("--noproxy",help="do not use TOR or any proxy (request sent from actual ipaddy)",required=False,action="store_true")

        #Options that cannot be used together
        group = parser.add_mutually_exclusive_group()
        group.add_argument("--url",help="process single URL.",action="store_true")
        group.add_argument("--file",help="process file of URLs.") #,action="store_true")

        args = parser.parse_args()

        if args.url: #SINGLE URL Processing
            url = raw_input("URL: ")
            if len(url) == 0:
                print "Error: No URL specified"
                sys.exit()
            else:
                if args.proxy: #PROXY OPTION
                    userProxy = raw_input("PROXY: ")
                    if len(userProxy) == 0:
                        print "Error: No proxy specified"
                        sys.exit()
                    else:
                        urlProcessor = Incognito.URL()
                        urlProcessor.GetURL(url,userProxy)
                        sys.exit()
                elif args.noproxy: #NOPROXY OPTION
                    urlProcessor = Incognito.URL()
                    urlProcessor.GetURL(url,noproxy=1)
                    sys.exit()
                else:
                    #proxy = Incognito.ProxyCheck(args)
                    urlProcessor = Incognito.URL()
                    urlProcessor.GetURL(url)
                    sys.exit()
        elif args.file: #FILE Processing
            # fileName = raw_input("FILE: ")
            fileName = args.file

            # if len(fileName) == 0:
            #     print "Error: No file specified"
            #     sys.exit()
            if args.noproxy:
                urlFileProcessor = Incognito.File()
                urlFileProcessor.GetFile(fileName,noproxy=1)
                sys.exit()
            elif args.proxy: #PROXY OPTION
                userProxy = raw_input("PROXY: ")
                if len(userProxy) == 0:
                    print "Error: No proxy specified"
                    sys.exit()
                else:
                    urlProcessor = Incognito.File()
                    urlProcessor.GetFile(url,userProxy)
                    sys.exit()
            else:
                urlFileProcessor = Incognito.File()
                urlFileProcessor.GetFile(fileName)
                sys.exit()

if __name__=='__main__':
    Incognito._main()
#END

