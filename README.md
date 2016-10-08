# SagiJudge
사기꾼판별기

# Adress  
40.74.136.158  

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
/show/get_comments/doctor/{{page_id}}
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

## Add User
```
POST
/add/user
body :{
 user_email : (text)
 user_password : (text)
 user_type : (int) // 0:alphGo, 1:user , 2:doctor
}
```

## Post comment
```
POST
/add/comment
body :{
 page_id : {{page_id}},
 user_id : {{user_id}},
 user_comment : {{user_comment}},
 user_rating : {{user_rating}},
}
```


## wait 4
```
/show/hot/{{user_id}}
```
```
res : {
}
```

## hot 4
```
/show/hot/{{user_id}}
```

## wrong 4
```
/show/hot/{{user_id}}
```
