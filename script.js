const ALLOWED_PANELS = ['apps', 'games'];

const panelData = {
  apps: {
    title: '📱 Apps',
    items: [
      { icon: '🗺️', label: 'Maps' },
      { icon: '📷', label: 'Camera' },
      { icon: '📅', label: 'Calendar' },
      { icon: '🎵', label: 'Music' },
      { icon: '📧', label: 'Mail' },
      { icon: '🌐', label: 'Browser' },
      { icon: '📝', label: 'Notes' },
      { icon: '⚙️', label: 'Settings' },
    ]
  },
  games: {
    title: '🎮 Games',
    items: [
      { icon: '🏎️', label: 'Racing' },
      { icon: '🧩', label: 'Puzzle' },
      { icon: '⚔️', label: 'Adventure' },
      { icon: '🏆', label: 'Sports' },
      { icon: '🔫', label: 'Action' },
      { icon: '🧠', label: 'Strategy' },
      { icon: '🃏', label: 'Card Games' },
      { icon: '🎲', label: 'Board Games' },
    ]
  }
};

function openPanel(type) {
  if (!ALLOWED_PANELS.includes(type)) return;
  const data = panelData[type];

  document.getElementById('panelTitle').textContent = data.title;

  const body = document.getElementById('panelBody');
  body.innerHTML = '';
  data.items.forEach(item => {
    const div = document.createElement('div');
    div.className = 'item';

    const icon = document.createElement('span');
    icon.style.fontSize = '1.5rem';
    icon.textContent = item.icon;

    const label = document.createTextNode(item.label);

    div.appendChild(icon);
    div.appendChild(label);
    body.appendChild(div);
  });

  document.getElementById('panel').classList.add('open');
  document.getElementById('overlay').classList.add('active');
}

function closePanel() {
  document.getElementById('panel').classList.remove('open');
  document.getElementById('overlay').classList.remove('active');
}

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('appsBtn').addEventListener('click', function () { openPanel('apps'); });
  document.getElementById('gamesBtn').addEventListener('click', function () { openPanel('games'); });
  document.getElementById('panelCloseBtn').addEventListener('click', closePanel);
  document.getElementById('overlay').addEventListener('click', closePanel);
});
