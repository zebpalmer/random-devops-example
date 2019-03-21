# Approach

As you'll notice, I chose to use kubernetes as the orchestration layer. I made a few small changes to the apps. 
- Added health endpoints
- Using gunicorn 
- swapped to mongodb

I could have thrown the sqlite db on a volume and mounted it to each instance, but I chose to swap it out for a 
distributed database. Though, admittedly, I deployed this project to a single node mongo instance rather than 
a replica set. And I chose mongo vs mysql/pgsql because I already had I already had a few instances deployed to this 
cluster.  

#### Notes:
- You will also see that I temporarily deployed an ingress mounting App B at `/auth-svc` on the App A ingress for 
initial deploy testing. I left that file in the repo, commenting it out rather than deleting for easier inspection. 

- I chose not to squash any commits or didn't use any branches per the readme's note about progress.
Many of these commits would have been appropriate for sqashing or condensing through branches/PRs. 

### Proof
You can access the service at https://app-a.halo.sh, as there is no root view in the flask app, I'd suggest hitting 
`/hello`, `/healthz` or running your suggested test(s). This is deployed to a small kubernetes 


## Autoscaling

I'm using the horizontal auto scaling resource in kubernetes to scale both apps. You'll notice app A and B 
are configured slightly different in this respect. App B is using a CPU target percentage which is one of the
two default pod resource metrics, this works in any recent kubernetes cluster without a custom metrics API. 
App A is configured for using the custom metrics API to look at requests per second across the ingress as well as 
a target CPU usage.

Here you can see app-a scaling up during an `ab` run. 

```bash
kubectl get deployment app-a --watch

NAME    READY   UP-TO-DATE   AVAILABLE   AGE
app-a   1/1     1            1           8h
app-a   1/3     1            1           8h
app-a   1/3     1            1           8h
app-a   1/3     1            1           8h
app-a   1/3     2            1           8h
app-a   1/3     3            1           8h
app-a   2/3     3            2           8h
app-a   3/3     3            3           8h
```


# CI/CD

Given the allotted time, I did not setup CI/CD for the project, but it'd be straight forward to throw in 
your CI/CD tool(s) of choice. I also didn't version the apps or their docker images as I didn't want to 
juggle tags without a ci/cd pipeline, that's a recipe for frustration. Yep, for the sake of time I'm using 
'latest' image tags and making rapid iteration to my 'production' environment. 
Don't use 'latest' in prod. Also, version your stuff. 

To deploy a new version, your deploy tool would need to get the images to your docker repo 
(which hopefully your build/test pipline has already done) and then the manifest needs 
to have the tag bumped. Kubernetes will do a rolling deploy as soon as it receives a new desired state. 
You'll notice I added and am using a health endpoint in both apps to help facilitate zero downtime state 
changes. 

My manual pipeline consisted of running `buildall.sh` (included in the repo) which built each app's image and pushed 
them to my personal docker repo (which is also running in kubernetes, in the same cluster this project was deployed to). 
 


## Testing...

Single request

```bash
→ curl -X POST -H 'Authorization: mytoken' https://app-a.halo.sh/jobs
Jobs:
Title: Devops
Description: Awesome
```

Running apache bench against the service.

*Ignore the high-ish latency, this cluster is on the other side of the country from me and 
its not the fastest hw*

```bash
→ ab -m POST -H "Authorization: mytoken" -n 500 -c 4 https://app-a.halo.sh/jobs
This is ApacheBench, Version 2.3 <$Revision: 1807734 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking app-a.halo.sh (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Finished 500 requests


Server Software:        nginx/1.13.12
Server Hostname:        app-a.halo.sh
Server Port:            443
SSL/TLS Protocol:       TLSv1.2,ECDHE-RSA-AES256-GCM-SHA384,2048,256
TLS Server Name:        app-a.halo.sh

Document Path:          /jobs
Document Length:        41 bytes

Concurrency Level:      4
Time taken for tests:   33.138 seconds
Complete requests:      500
Failed requests:        0
Total transferred:      131500 bytes
HTML transferred:       20500 bytes
Requests per second:    15.09 [#/sec] (mean)
Time per request:       265.103 [ms] (mean)
Time per request:       66.276 [ms] (mean, across all concurrent requests)
Transfer rate:          3.88 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:      179  184   4.6    182     229
Processing:    68   80  10.9     77     157
Waiting:       68   80  10.7     77     150
Total:        250  264  12.1    261     338

Percentage of the requests served within a certain time (ms)
  50%    261
  66%    265
  75%    268
  80%    270
  90%    277
  95%    289
  98%    306
  99%    316
 100%    338 (longest request)

```
