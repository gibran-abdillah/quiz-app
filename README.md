# quiz-app
Quiz Web Application made with flask and mongodb as the Databases

### Before you run this application, change the inside MONGODB_URI ( in config.py ) to your cluster database. <a href='https://docs.atlas.mongodb.com/connect-to-cluster/'>( Read More ) </a>
Example for MONGODB_URI :
```python
MONGODB_URI = 'mongodb+srv://username:password@learnmongo.scjon.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
```

## Features 
- CRUD with ajax
- Rest API
- Add Quiz
- Add Quz From CSV
- Edit QUiz
- Quiz author can see score that if quiz were done by other users ( only for logged in users ) 
- We can see the quiz scores that have been done
- Register 
- Login 
- Change Password

## Screenshots 
### Dashboard Scores 
![Screenshots](https://github.com/gibran-abdillah/quiz-app/raw/main/screenshots/dashboard_scores.png)

### Questions
![Questions](https://github.com/gibran-abdillah/quiz-app/raw/main/screenshots/questions.png)
