let currentRoad = 1;
let score = 0;
let totalQuestions = 4;
let currentQuestion = 0;
let quizOver = false;
let questions = [];


fetch('static/questions.json')
  .then(res => res.json())
  .then(data => {
    questions = data;
    loadQuestion();
  });


function loadQuestion() {
  const q = questions[currentQuestion];
  document.getElementById('question-text').textContent = q.question;
  document.getElementById('question-image').src = q.image;

  const buttonsContainer = document.getElementById('answer-buttons');
  buttonsContainer.innerHTML = '';

  q.answers.forEach((answer, index) => {
    const btn = document.createElement('button');
    btn.textContent = answer;
    btn.onclick = () => submitAnswer(index);
    buttonsContainer.appendChild(btn);
  });
}


function loadRoad(roadNumber) {
  const progress = document.getElementById('progress');
  if (progress) {
    progress.textContent = `Kérdés: ${roadNumber}/${totalQuestions}`;
  }
}

function submitAnswer(option) {
  if (quizOver) return;

  console.log("User chose:", option);
  const isCorrect = (questions[currentQuestion].correct === option);

  if (isCorrect) {
    score++;
    console.log("Helyes válasz. Pont: ", score);
  } else {
    console.log("Helytelen válasz. Pont: ", score);
  }

  currentRoad++;
  currentQuestion++;

  if (currentQuestion >= questions.length) {
    quizOver = true;
    console.log("Kvíz vége. Elért pontszám: ", score);
    submitFinalScore();

    const allButtons = document.querySelectorAll('.option-button');
    allButtons.forEach(button => {
      button.disabled = true; 
    });
    return;
  }

  loadQuestion();
  loadRoad(currentRoad);
}

function submitFinalScore() {
    const roadContainer = document.getElementById('road-container');
    roadContainer.innerHTML = `
    <div style="text-align: center; padding: 20px; font-size: 24px;">
      <h2>Kvíz vége!</h2>
      <p>Elért pontszám: ${score}/${totalQuestions}</p>
      <p>A pontszám mentése folyamatban...</p>
    </div>
  `;
    fetch('/quiz/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
        body: JSON.stringify({
            adat: score
        })
    })
    .then(response => response.json())
    .then(data => {
    if (data.success) {
      roadContainer.innerHTML = `
        <div style="text-align: center; padding: 20px; font-size: 24px;">
          <h2>Kvíz vége!</h2>
          <p>Elért pontszám: ${score}/${totalQuestions}</p>
          <p>A pontszám sikeresen elmentve!</p>
          <a href="/" class="btn" style="display:inline-block; margin-top: 20px;">Vissza a főoldalra</a>
        </div>
      `;
    } else {
      roadContainer.innerHTML = `
        <div style="text-align: center; padding: 20px; font-size: 24px;">
          <h2>Kvíz vége!</h2>
          <p>Elért pontszám: ${score}/${totalQuestions}</p>
          <p>Hiba történt a pontszám mentése során!</p>
          <a href="/" style="display:inline-block; margin-top: 20px;">Vissza a főoldalra</a>
        </div>
      `;
    }
  });
}

window.onload = () => {
  loadRoad(currentRoad);
};
