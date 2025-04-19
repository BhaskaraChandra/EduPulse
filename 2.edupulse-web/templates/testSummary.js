// Hardcoded JSON data
let testResult = {
    "Qs": {
        "9": {"Choice": "A", "Review": false, "TimeSpent": 5, "TimeToSubmit": 4, "key": "A"},
        "16": {"Choice": "A", "Review": false, "TimeSpent": 4, "TimeToSubmit": 3, "key": "A"},
        "18": {"Choice": "A", "Review": false, "TimeSpent": 5, "TimeToSubmit": 3, "key": "C"},
        "151": {"Choice": "A", "Review": false, "TimeSpent": 3, "TimeToSubmit": 2, "key": "A"},
        "304": {"Choice": "A", "Review": false, "TimeSpent": 3, "TimeToSubmit": 1, "key": "A"},
        "468": {"Choice": "A", "Review": false, "TimeSpent": 3, "TimeToSubmit": 1, "key": "A"},
        "473": {"Choice": "A", "Review": false, "TimeSpent": 3, "TimeToSubmit": 1, "key": "2"},
        "526": {"Choice": "A", "Review": false, "TimeSpent": 2, "TimeToSubmit": 1, "key": "B"},
        "611": {"Choice": "-", "Review": true, "TimeSpent": 3, "TimeToSubmit": 0, "key": "A"},
        "775": {"Choice": "-", "Review": true, "TimeSpent": 544, "TimeToSubmit": 0, "key": "20"}
    },
    "startTime": "2025-04-05T10:25:11.833Z",
    "endTime": "2025-04-05T12:00:32.536Z",
    "userid": "orguser@org.com",
    "testduration": 0,
    "TestDuration": 575,
    "review": 2,
    "total": 10,
    "correct": 5,
    "wrong": 3,
    "unattempted": 2,
    "score": 5
};
//let testResult = testResultData;
// Display summary
//let summary = `Total Questions: ${testResult.total}\nCorrect: ${testResult.correct}\nScore: ${testResult.score}\nIncorrect: ${testResult.wrong}\nNot Attempted: ${testResult.unattempted}\nMarked for Review: ${testResult.review}\nTotal Time: ${testResult.TestDuration} seconds`;
//document.getElementById('summary').innerText = summary;

// Display questions
let accordion = document.getElementById('accordionExample');
let i = 0;
for (let q in testResult.Qs) {
    let card = document.createElement('div');
    card.classList.add('card');
    let cardHeader = document.createElement('div');
    cardHeader.classList.add('card-header');
    let reviewText = '';
    if (testResult.Qs[q].Review) {
        reviewText = ' (Marked for Review)';
    }
    cardHeader.innerHTML = `
        <h2 class="mb-0">
            <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse${i}" aria-expanded="true" aria-controls="collapse${i}">
                Question ${q}${reviewText}
            </button>
        </h2>
    `;
    cardHeader.innerHTML = `
    <h2 class="mb-0">
        <div class="btn btn-link" style="cursor: pointer;" data-toggle="collapse" data-target="#collapse${i}" aria-expanded="true" aria-controls="collapse${i}">
            Question ${q}${reviewText}
        </div>
    </h2>
    `;
    cardHeader.innerHTML = `
    <h2 class="mb-0">
        <button class="btn btn-block" type="button" data-toggle="collapse" data-target="#collapse${i}" aria-expanded="true" aria-controls="collapse${i}">
            Question ${q}${reviewText}
        </button>
    </h2>
    `;

    card.appendChild(cardHeader);
    let cardBody = document.createElement('div');
    cardBody.classList.add('collapse');
    cardBody.id = `collapse${i}`;
    /*if (testResult.Qs[q].Choice === testResult.Qs[q].key && testResult.Qs[q].Choice !== '-') {
        cardBody.classList.add('correct');
    } else if (testResult.Qs[q].Choice !== testResult.Qs[q].key && testResult.Qs[q].Choice !== '-') {
        cardBody.classList.add('incorrect');
    }*/
    if (testResult.Qs[q].Choice === testResult.Qs[q].key && testResult.Qs[q].Choice !== '-') {
        cardHeader.querySelector('button').classList.add('correct');
    } else if (testResult.Qs[q].Choice !== testResult.Qs[q].key && testResult.Qs[q].Choice !== '-') {
        cardHeader.querySelector('button').classList.add('incorrect');
    }
    
    cardBody.innerHTML = `
        <div class="card-body">
            Choice: ${testResult.Qs[q].Choice}<br>
            Key: ${testResult.Qs[q].key}<br>
            Time Spent: ${testResult.Qs[q].TimeSpent} seconds<br>
            Time to Submit: ${testResult.Qs[q].TimeToSubmit} seconds
        </div>
    `;
    if (testResult.Qs[q].Choice === testResult.Qs[q].key && testResult.Qs[q].Choice !== '-') {
        cardHeader.classList.add('correct');
    } else if (testResult.Qs[q].Choice !== testResult.Qs[q].key && testResult.Qs[q].Choice !== '-') {
        cardHeader.classList.add('incorrect');
    }
    card.appendChild(cardBody);
    accordion.appendChild(card);
    i++;
}
