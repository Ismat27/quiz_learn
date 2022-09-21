# Get a new quiz question

``` js
const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                'prev_id': [] // the list should contain previous quiz id that the user has answered
            })
        };
fetch('http://127.0.0.1:8000/quiz-question/', requestOptions)
    .then(response => response.json())
    .then(data => {
            console.log(data);
        else {
            // do what you like by checking the error
            console.log('failed');
        }
    })
    .catch(error => {
        // catch error here
        console.log(error);
    });
```
