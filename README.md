# quiz-app
Quiz Web Application made with flask and mongodb as the Databases

### Before you run the application, set your mongodb uri to environ. <a href='https://docs.atlas.mongodb.com/connect-to-cluster/'>( Read More )</a> how to get your cluster database
Example for MONGODB_URI :
```sh
export "MONGODB_URI = mongodb+srv://username:password@learnmongo.scjon.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
```

## Features 
- CRUD with ajax
- Rest API
- Add Quiz
- Add Quiz From CSV
- Edit Quiz
- Delete QUiz 
- Quiz author can see score that if quiz were done by other users ( only for logged in users ) 
- We can see the quiz scores that we have been done
- Bulk delete for users ( admin level ) 
- Bulk promote users to admin
- Bulk unpromote users from admin role 
- Register 
- Login 
- Change Password

## Demo 
<a href='http://another-myapp.herokuapp.com/'>http://another-myapp.herokuapp.com</a>
- username  : admin
- password : admin1

## Screenshots 
### Dashboard Scores 
![Screenshots](https://github.com/gibran-abdillah/quiz-app/raw/main/screenshots/dashboard_scores.png)

### Questions
![Questions](https://github.com/gibran-abdillah/quiz-app/raw/main/screenshots/questions.png)
