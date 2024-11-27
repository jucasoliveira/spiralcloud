use ggez::{conf, event, graphics, mint::Point2, Context, ContextBuilder, GameResult};
use std::f32;
use std::fs::OpenOptions;
use std::io::Write;
use std::time::Instant;
const WIDTH: f32 = 800.0;
const HEIGHT: f32 = 800.0;
const N: usize = 99999;
const MAX_FRAMES: u32 = 20000;

struct MainState {
    t: f32,
    p: Vec<bool>,
    points: Vec<Point2<f32>>,
    frame_count: u32,
}

impl MainState {
    fn new() -> GameResult<MainState> {
        let mut p = vec![true; N];
        p[0] = false;
        p[1] = false;

        // Sieve of Eratosthenes to mark non-primes
        for i in 2..N {
            if p[i] {
                let mut j = i * 2;
                while j < N {
                    p[j] = false;
                    j += i;
                }
            }
        }

        let points = Vec::new();
        let s = MainState {
            t: 1.0,
            p,
            points,
            frame_count: 0,
        };
        Ok(s)
    }
}

impl event::EventHandler for MainState {
    fn update(&mut self, _ctx: &mut Context) -> GameResult {
        if self.frame_count >= MAX_FRAMES {
            return Ok(());
        }
        self.t += 0.0000001;

        // Update points based on current time `t`
        self.points.clear();
        for i in 3..N {
            if self.p[i] {
                let x = (f32::sin(i as f32 * self.t) * (i as f32 / 99.0)) + WIDTH / 2.0;
                let y = (f32::cos(i as f32 * self.t) * (i as f32 / 99.0)) + HEIGHT / 2.0;
                self.points.push(Point2 { x, y });
            }
        }
        Ok(())
    }

    fn draw(&mut self, ctx: &mut Context) -> GameResult {
        // Clear the screen
        if self.frame_count >= MAX_FRAMES {
            return Ok(()); // Stop drawing after reaching max frames
        }
        let start_time = Instant::now();
        let black = graphics::Color::from_rgb(0, 0, 0);
        graphics::clear(ctx, black);

        let white = graphics::Color::from_rgb(255, 255, 255);
        let mut mesh_builder = graphics::MeshBuilder::new();

        for point in &self.points {
            mesh_builder.circle(graphics::DrawMode::fill(), *point, 2.0, 0.1, white)?;
        }

        let mesh = mesh_builder.build(ctx)?;
        graphics::draw(ctx, &mesh, graphics::DrawParam::default())?;
        graphics::present(ctx)?;

        let frame_time = start_time.elapsed().as_millis();
        let mut file = OpenOptions::new()
            .create(true)
            .append(true)
            .open("metrics_rust.txt")?;
        writeln!(
            file,
            "Frame Time: {} ms, Points Drawn: {}",
            frame_time,
            self.points.len()
        )
        .unwrap();
        self.frame_count += 1;
        Ok(())
    }
}

fn main() -> GameResult {
    let (ctx, event_loop) = ContextBuilder::new("prime_spiral_visualization", "ggez")
        .window_setup(conf::WindowSetup::default().title("Prime Spiral Visualization"))
        .window_mode(conf::WindowMode::default().dimensions(WIDTH, HEIGHT))
        .build()?;

    let state = MainState::new()?;
    event::run(ctx, event_loop, state)
}
