let currentRoad = 1;
let score = 0;
let totalQuestions = 4;

const correctAnswers = {
  1: 'A',
  2: 'B',
  3: 'C',
  4: 'D',
};


function loadRoad(roadNumber) {
  const roadContainer = document.getElementById('road-container');

  // Clear current
  roadContainer.innerHTML = '';

  if (roadNumber > totalQuestions) {
  submitFinalScore();
  return;
  }   

  // Load CSS
  const oldLink = document.getElementById('dynamic-style');
  if (oldLink) oldLink.remove();

  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = `static/roadStyles/road${roadNumber}.css`;
  link.id = 'dynamic-style';
  document.head.appendChild(link);

  // Load HTML
  fetch(`static/roadLayouts/road${roadNumber}.html`)
    .then(response => response.text())
    .then(html => {
      roadContainer.innerHTML = html;
    });
}

function submitAnswer(option) {
    console.log("User chose:", option);
    const isCorrect = (correctAnswers[currentRoad] === option)

    if (isCorrect) {
        score++;
        console.log("Helyes válasz. Pont: ", score);
    } else {
        console.log("Helytelen válasz. Pont: ", score);
    }

    currentRoad++;
    loadRoad(currentRoad); // Load next situation
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
          <a href="/" style="display:inline-block; margin-top: 20px;">Vissza a főoldalra</a>
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
  loadRoad(currentRoad); // Load first road on start
};
