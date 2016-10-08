# SagiJudge
사기꾼판별기

# API LIST
## url -> ID call
```
/show/get_url/{{url}}  
```
```
res : {id: (id)}
```

## id -> rating call  
```
/show/get_rating/{{id}}  
```
```
res :{
  "expert":{
    "good":123,
    "bad":55,
    "avg":0.6910112359550562
   },
   "public_user":{
     "good":7244,
     "bad":1284,
     "avg":0.849437148217636
    },
   "ai":{"avg":0.65}
}
```
