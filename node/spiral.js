// HTML Canvas setup for rendering in the browser
let canvas = document.getElementById('spiralCanvas');
if (!canvas) {
  canvas = document.createElement('canvas');
  canvas.id = 'spiralCanvas';
  document.body.appendChild(canvas);
}
canvas.width = 800;
canvas.height = 800;
const ctx = canvas.getContext('2d');

const n = 99999;
const p = new Array(n).fill(0);
let t = 1;
const max_frames = 20000;
let metrics = [];

// Sieve of Eratosthenes to mark non-primes
for (let i = 2; i < n; i++) {
  if (p[i] === 0) {
    for (let j = i * 2; j < n; j += i) {
      p[j] = i;
    }
  }
}


let frameCount = 0;

function draw() {
  if (!ctx) {
    console.error('Canvas rendering context not found');
    return;
  }

  const startTime = performance.now(); // Start timing the frame

  // Clear the canvas
  ctx.fillStyle = 'black';
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = 'white';
  let pointsDrawn = 0;
  for (let i = 3; i < n; i++) {
    if (p[i] === 0) {
      // Calculate position using polar coordinates
      const x = Math.sin(i * t) * (i / 99) + canvas.width / 2;
      const y = Math.cos(i * t) * (i / 99) + canvas.height / 2;

      // Draw the point
      ctx.beginPath();
      ctx.arc(x, y, 2, 0, Math.PI * 2);
      ctx.fill();
      pointsDrawn++;
    }
  }

  t += 1e-7;

  // Calculate and log frame time
  const frameTime = performance.now() - startTime;
  const metricsEntry = `Frame Time: ${frameTime.toFixed(2)} ms, Points Drawn: ${pointsDrawn}`;
  console.log(metricsEntry);
  metrics.push(metricsEntry);

  frameCount++;

  if (frameCount >= max_frames) {
    downloadMetrics();
    return; // Stop the animation after downloading metrics
  }

 
  // Schedule the next frame
  requestAnimationFrame(draw);
}


function downloadMetrics() {
  const metricsText = metrics.join('\n');
  const blob = new Blob([metricsText], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);

  const downloadLink = document.createElement('a');
  downloadLink.href = url;
  downloadLink.download = 'metrics_node.txt';
  downloadLink.style.display = 'none';
  document.body.appendChild(downloadLink);

  downloadLink.click();

  // Clean up
  document.body.removeChild(downloadLink);
  URL.revokeObjectURL(url);
}



// Start the animation
draw();