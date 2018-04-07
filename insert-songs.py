import time
import struct
import urllib.parse, urllib.request
import csv

def construct_request_body(timestamp, itunes_identifier):
    hex = "61 6a 43 41 00 00 00 45 6d 73 74 63 00 00 00 04 55 94 17 a3 6d 6c 69 64 00 00 00 04 00 00 00 00 6d 75 73 72 00 00 00 04 00 00 00 81 6d 69 6b 64 00 00 00 01 02 6d 69 64 61 00 00 00 10 61 65 41 69 00 00 00 08 00 00 00 00 11 8c d9 2c 00" 

    body = bytearray.fromhex(hex);
    body[16:20] = struct.pack('>I', timestamp)
    body[-5:] = struct.pack('>I', itunes_identifier)
    return body


def add_song(itunes_identifier):
    data = construct_request_body(int(time.time()), itunes_identifier)

    headers = {
        "X-Apple-Store-Front" : "143441-1,32",
        "Client-iTunes-Sharing-Version" : "3.14",
        "Accept-Language" : "te-US;q=1.0, en-US;q=0.9",
        "Client-Cloud-DAAP-Version" : "1.3/iTunes-12.7.4.76",
        "Accept-Encoding" : "gzip",
        "X-Apple-itre" : "0",
        "Client-DAAP-Version" : "3.13",
        "User-Agent" : "iTunes/12.7.4 (Macintosh; OS X 10.13.3) AppleWebKit/604.5.6 (dt:1)",
        "Connection" : "keep-alive",
        "Content-Type" : "application/x-dmap-tagged",
        # Replace the values of the next three headers with the values you intercepted
        "X-Dsid" : "226247711",
        "Cookie" : "ns-mzf-inst=35-149-443-110-126-8277-182303-18-nk11; mzf_in=182303; amp=5cdoJEH1btlzyWTWCUq4yZDwrjBFcGHTc0pJk+1f7zVs/nRZwH46cmN2l5thVXzYWgQzHbLmmxW9sdYR598e+nLvraUbjJQmY3smp9PZ05NCbXVF2T3lUGYTW8vFF4xEt1T2+ShWpqwjOewENdsCutb2OItW5sotSUdCXVrpF2ySCAA18D1De4U94FsPF3e6; amia-226247711=eUGm6flrmPa13Gp6uNG0DVeZv38sG6jFSAmFO3FNe4BsBBuX5wt+ehi/iMJWq6BZYxcA6E4kdC9hSGawbos9Tw==; itspod=18; TrPod=2; mz_at_ssl-226247711=AwUAAAEBAAHXgAAAAABax9NpUUUR3P09mk6uNl1cCV/FnJ7gg0I=; xp_ab=1#isj11bm+2847+PcSvtDe0; xp_abc=PcSvtDe0; xp_ci=3zvqNhRz3h5z510zAYZzWH1t2But; vrep=CJ-I8WsSBAgHEAASBAgIEAASBAgDEAASBAgEEAASBAgGEAASBAgBEAASBAgFEAASBAgCEAA; mt-asn-226247711=5; X-Dsid=226247711; mz_at0-226247711=AwQAAAEBAAHXfwAAAABalHGv1j1aSFK+FkravwTl4RB073tX5t8=; pldfltcid=21d8972053ae43f8b26d4a44b927da74018; mt-tkn-226247711=Al7AnuHe0nmWfB1xvQkhMLF1/prxXQPcTQRXEWMi4wOOIWlFnHQ+LzHl6vd/R72HrTln0pZc7mNLRT/zk5qEN+KULlYbjoBoKA+u2EnncHVplSEsXWuFj58loJW6TeayPErOxcTPzEs+8Pt2zXCk63z0SOyuAOR8eaUmrI8ZnrjSYVXKZxaD/Hqmnc831rj7IK7OZKE=; groupingPillToken=2_allPodcasts", 
        "X-Guid" : "ACBC32947F83",
        "Content-Length" : "77"
    }

    request = urllib.request.Request("https://ld-4.itunes.apple.com/WebObjects/MZDaap.woa/daap/databases/1/cloud-add", data, headers)
    urllib.request.urlopen(request)

# Identified songs failed to put
failed_songs = []

with open('itunes.csv') as itunes_identifiers_file:
    for line in itunes_identifiers_file:
        itunes_identifier = int(line)
        
        try:
            add_song(itunes_identifier)
            print("Successfuly inserted a song!")
            # Try playing with the interval here to circumvent the API rate limit
            time.sleep(5)
        except Exception as e:
            failed_songs.append(str(itunes_identifier))
            print("Something went wrong while inserting " + str(itunes_identifier) + " : " + str(e))

outfile = open("failed_songs.csv", "w")
writer = csv.writer(outfile)
for row in l:
    writer.writerow(row)
outfile.close()
