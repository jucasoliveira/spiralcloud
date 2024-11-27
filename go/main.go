package main

import (
	"fmt"
	"image/color"
	"math"
	"os"
	"time"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

const (
	width      = 800
	height     = 800
	n          = 99999
	max_frames = 20000
)

type Game struct {
	t           float64
	p           []int
	file        *os.File
	frame_count int
}

func (g *Game) Update() error {
	g.t += 1e-7
	return nil
}

func (g *Game) Draw(screen *ebiten.Image) {
	if g.frame_count >= max_frames {
		return
	}
	start := time.Now()

	screen.Fill(color.Black)

	pointsDrawn := 0
	for i := 3; i < n; i++ {
		if g.p[i] == 0 {
			x := int(math.Sin(float64(i)*g.t)*(float64(i)/99) + float64(width)/2)
			y := int(math.Cos(float64(i)*g.t)*(float64(i)/99) + float64(height)/2)
			if x >= 0 && x < width && y >= 0 && y < height {
				ebitenutil.DrawRect(screen, float64(x), float64(y), 2, 2, color.White)
				pointsDrawn++
			}
		}
	}

	g.frame_count += 1

	fmt.Fprintf(g.file, "Frame Time: %d ms, Points Drawn: %d\n", time.Since(start).Milliseconds(), pointsDrawn)
}

func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return width, height
}

func main() {
	// Initialize sieve of Eratosthenes
	file, err := os.OpenFile("metrics_go.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	if err != nil {
		panic(err)
	}

	// Clean the metrics file
	file.Truncate(0)
	file.Seek(0, 0)

	p := make([]int, n)
	for i := 2; i < n; i++ {
		if p[i] == 0 {
			for j := i * 2; j < n; j += i {
				p[j] = i
			}
		}
	}

	game := &Game{
		t:           1,
		p:           p,
		file:        file,
		frame_count: 0,
	}

	ebiten.SetWindowSize(width, height)
	ebiten.SetWindowTitle("Prime Spiral Visualization")
	if err := ebiten.RunGame(game); err != nil {
		panic(err)
	}
}
