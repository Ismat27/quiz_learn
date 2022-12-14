# Endpoints

Unless otherwise stated all endpoints will have same base url given below:

```sh
BASE_URL = 'http://127.0.0.1:8000'
```

## Sign up new user: /signup/

The following fields are required:

- username
- first_name
- last_name
- email
- password

Sample request

``` js
axios.post(`${BASE_URL}/signup/`, {
    username: 'username',
    first_name: 'first_name',
    last_name: 'lastt_name',
    email: 'email',
    password: 'password',
})
.then((response) => {
    console.log(response.data)
})
.catch(error => {
    // handle error as appropriate
})
```

Sample success response

```js
{
    success: true,
    user: {…} // user details
}
```

## Login user: /login/

**Method : Post**
Required fields:

- username
- password

Sample request

```js
axios.post(`${BASE_URL}/login/`, {
    username: 'username',
    password: 'password'
})
.then((response) => {
    const {data} = response
    console.log(data)
})
.catch(error => {
    // handle error
})
```

Sample success response

```js
{
    success: true;
    token: ''; // to be sent along all requests require quthorization
    user: {...} // user details
}
```

## GET USER DETAIL: /users/user_id/

Method: **GET**

NB: **user_id** is a unique identifier for the user which is gotten after a user has logged in

```js
axios.get(`${BASE_URL}/users/${user_id}/`, {
    headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
    const {data} = response
    console.log(data)
    })
    .catch(error => {
    console.log(error);
})
```

## GET QUIZ QUESTIONS: /quiz-question/

Method: **GET**

This endpoint requires authorization token

Sample Request

```js
axios.GET(`${BASE_URL}/quiz-question/`, {
    headers: {Authorization: `Token ${token}`} // token is obtained upon logging in
})
.then(response => {
    const {data} = response
    console.log(data)
})
.catch(error => {
    // handle error
})
```

Sample success response:

```js
{
    quiz_id: '' // string, to be sent along for grading the user after completing the quiz
    questions: [] // list of questions 
}
```

## GRADE QUIZ: /mark-quiz/

Method: **POST**

Required fields:

- quiz_id: This is given along with quiz questions
- answers: list of user answers to each question. Each answer will be object as given below

```js
{
    question_id: 'string' // unique question id,
    user_answer: 'user answer to the question'
}
```

This endpoint requires authorization

Sample Request

```js
axios.post(`${BASE_URL}/mark-quiz/`, {quiz_id: '', answers: [{...},]}, {
    headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` }
})
.then(response => {
    const {data} = response
    console.log(data)
})
.catch(error => {
    // handle error
})
```

Sample success response

```js
{challenge_points: 120, course_access_points: 90, score: 6}
```

## Dashboard Details: /dashboard/

Method: **GET**

This endpoint requires authorization

Response:

- List of user referrals
- User Course access points
- User challenge points

Sample Request

```js
axios.get(`${BASE_URL}/dashboard/`, {
    headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
    const {data} = response
    console.log(data)
    })
    .catch(error => {
    console.log(error);
})
```

## Leaderboard Details: /leaderboard/

Method: **GET**

Response:

- List of leaderboard data

Sample Request

```js
axios.get(`${BASE_URL}/leaderboard/`, {
    headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
    const {data} = response
    console.log(data)
    })
    .catch(error => {
    console.log(error);
})
```

## Set a New Question: /questions/

Method: **POST**

This endpoint requires that the user is authorized to set a new question

Required fields (data):

- text: question text
- option_a: first question option
- option_b: second question option
- option_c: third question option
- option_d: fourth question option
- answer: correct answer to the question
- cp_wrong: a number that indicates the challenge points to be awarded a user that got the question wrong
- cp_right: a number that indicates the challenge points to be awarded a user that got the question right
- cap_wrong: a number that indicates the course access points to be awarded a user that got the question wrong
- cap_right: a number that indicates the course access points to be awarded a user that got the question right

Sample Request

```js
axios.post(`${BASE_URL}/questions/`, data, {
    // data is an object containing values for the required fields
    headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
    const {data} = response
    console.log(data)
    })
    .catch(error => {
    console.log(error);
})
```

## Read, Delete a Question: /questions/question_id/

Method: **GET** to read

Method: **DELLETE** to delete

This endpoint requires that the user is authorized to read or delete a question as per the request method

The **question_id** is a unique identifier for each question

## Update a Question: /questions/question_id/

Method: **PUT**

This endpoint requires that the user is authorized to delete question

Required fields (data):

- text: question text
- option_a: first question option
- option_b: second question option
- option_c: third question option
- option_d: fourth question option
- answer: correct answer to the question
- cp_wrong: a number that indicates the challenge points to be awarded a user that got the question wrong
- cp_right: a number that indicates the challenge points to be awarded a user that got the question right
- cap_wrong: a number that indicates the course access points to be awarded a user that got the question wrong
- cap_right: a number that indicates the course access points to be awarded a user that got the question right

## Submit spin result: /spins/

Method: **POST**

This endpoint is to be called after spinning to record the points or items won by user as the case may be.

Required fields (data):

- username: The username of the user as recorded in the database.
- point: Points obtained by user after spinning. This to be an integer.

Sample Request

```js
const data = {
    username: 'username', // corresponding username to be included
    point: 5 // asssuming the user obtained 5 points after spinning
}
axios.post(`${BASE_URL}/spins/`, data, {
    // data is an object containing values for the required fields
    headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
    }
    })
    .then(response => {
    const {data} = response
    console.log(data)
    })
    .catch(error => {
    console.log(error);
})
```
