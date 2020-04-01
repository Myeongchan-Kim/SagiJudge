# SagiJudge
사기꾼판별기

# Requirement
Python
MySQL

## Python Packages
mysqlclient
flask

# Before to start
Make `database_info.py`

# Adress  
127.0.0.1

# API LIST
## url -> ID call
```
POST
/show/get_id/
body :{
url : {{url}}
}
```
```
res : {id: (id)}
```
## get_article
```
/40.74.136.158:3000/show/get_article/{{page_id}}
```
```
res :{
[
{"_id":5,
"url":"http%3A%2F%2Fdamoadamoa.tistory.com%2F123","title":"[무설탕]\"액상과당\"과 \"무설탕\"의 함정","content":"현대인의 비만은 사회적 문제가 될 만큼 심각하다.왜 갑자기 이런 비만이 폭발적으로 늘어나고 있을까? 그 답을 찾아본다...."}]
}
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
