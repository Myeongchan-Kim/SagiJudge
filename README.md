# SagiJudge
사기꾼판별기

# API LIST
## url -> ID call
```
/show/get_id/{{url}}  
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

## 5 users comments.
```
/show/get_comments/user/{{page_id}}
```
```
res : [
    {
      id: "mc1004",
      comment: "개사기 꺼져.",
      rating: 0,
    },
    {
      id: "tawoo",
      comment: "정말 좋아요~!! ^^.",
      rating: 1,
    },
    {
      id: "hahahah1925",
      comment: "아무래도 구라 같은데...",
      rating: 0,
    },
    {
      id: "Minytong",
      comment: "아무래도 구라구라왕구라",
      rating: 0,
    },
    {
      id: "asdf11111",
      comment: "좋은 정보 감사합니다~!!",
      rating: 1,
    },
  ];
```
