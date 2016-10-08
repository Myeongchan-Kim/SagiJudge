# SagiJudge
사기꾼판별기

# API LIST
## url -> ID call
```
/show/get_url/{{url}}  
res : {id: (id)}
```

## id -> rating call  
```
/show/get_rating/{{id}}  
result = {
      expert :{
        good : 123,
        bad : 55,
        avg : 123 / (123 + 55),
      }
      public_user :{
        good : 7244,
        bad : 1284,
        avg : 7244 / (7244 + 1284),
      }
      ai : {
        avg : 0.65,
      }
    }
```
