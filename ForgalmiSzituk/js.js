let currentRoad = 1;
let currentQuestion = 0;
let questions = [];

fetch('questions.json')
  .then(res => res.json())
  .then(data => {
    questions = data;
    loadQuestion();
    loadRoad(currentRoad);
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

function submitAnswer(selectedIndex) {
  const correctIndex = questions[currentQuestion].correct;

  if (selectedIndex === correctIndex) {
    currentQuestion++;
    currentRoad++;
    if (currentQuestion < questions.length) {
      loadQuestion();
      loadRoad(currentRoad);
    } else {
      document.getElementById('question-text').textContent = '🎉 All situations completed!';
      document.getElementById('answer-buttons').innerHTML = '';
      document.getElementById('road-container').innerHTML = '';
    }
  } else {
    alert("Incorrect! Try again.");
  }
}
