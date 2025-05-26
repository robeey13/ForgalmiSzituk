let currentRoad = 1;

function loadRoad(roadNumber) {
  const roadContainer = document.getElementById('road-container');

  // Clear current
  roadContainer.innerHTML = '';

  // Load CSS
  const oldLink = document.getElementById('dynamic-style');
  if (oldLink) oldLink.remove();

  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = `roadStyles/road${roadNumber}.css`;
  link.id = 'dynamic-style';
  document.head.appendChild(link);

  // Load HTML
  fetch(`roadLayouts/road${roadNumber}.html`)
    .then(response => response.text())
    .then(html => {
      roadContainer.innerHTML = html;
    });
}

function submitAnswer(option) {
  console.log("User chose:", option);
  currentRoad++;
  loadRoad(currentRoad); // Load next situation
}

window.onload = () => {
  loadRoad(currentRoad); // Load first road on start
};
