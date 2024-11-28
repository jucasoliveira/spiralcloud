#include <SDL.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define WIDTH 800
#define HEIGHT 800
#define N 99999
#define MAX_FRAMES 20000
int main(int argc, char *argv[])
{
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0)
    {
        printf("SDL_Init Error: %s\n", SDL_GetError());
        return 1;
    }

    // Create window
    SDL_Window *win = SDL_CreateWindow("Prime Spiral Visualization", 100, 100, WIDTH, HEIGHT, SDL_WINDOW_SHOWN);
    if (win == NULL)
    {
        printf("SDL_CreateWindow Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Create renderer
    SDL_Renderer *ren = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (ren == NULL)
    {
        SDL_DestroyWindow(win);
        printf("SDL_CreateRenderer Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Sieve of Eratosthenes to mark non-primes
    bool *p = (bool *)malloc(N * sizeof(bool));
    if (p == NULL)
    {
        printf("Memory allocation failed\n");
        SDL_DestroyRenderer(ren);
        SDL_DestroyWindow(win);
        SDL_Quit();
        return 1;
    }

    for (int i = 0; i < N; i++)
    {
        p[i] = true;
    }
    p[0] = p[1] = false;

    for (int i = 2; i < N; i++)
    {
        if (p[i])
        {
            for (int j = i * 2; j < N; j += i)
            {
                p[j] = false;
            }
        }
    }

    float t = 1.0f;
    bool running = true;
    SDL_Event e;
    int frame_count = 0;
    // Open file to write metrics
    FILE *metrics_file = fopen("metrics_c.txt", "w");
    if (!metrics_file)
    {
        printf("Failed to open metrics file\n");
        free(p);
        SDL_DestroyRenderer(ren);
        SDL_DestroyWindow(win);
        SDL_Quit();
        return 1;
    }

    while (running)
    {
        if (frame_count >= MAX_FRAMES)
        {
            break;
        }
        clock_t start_time = clock(); // Start timing the frame

        // Handle events
        while (SDL_PollEvent(&e))
        {
            if (e.type == SDL_QUIT)
            {
                running = false;
            }
        }

        // Clear the screen
        SDL_SetRenderDrawColor(ren, 0, 0, 0, 255);
        SDL_RenderClear(ren);

        // Draw points for primes
        SDL_SetRenderDrawColor(ren, 255, 255, 255, 255);
        SDL_Point points[N];
        int points_drawn = 0;
        for (int i = 3; i < N; i++)
        {
            if (p[i])
            {
                int x = (int)(sin(i * t) * (i / 99.0f) + WIDTH / 2);
                int y = (int)(cos(i * t) * (i / 99.0f) + HEIGHT / 2);
                if (x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT)
                {
                    points[points_drawn++] = (SDL_Point){x, y};
                }
            }
        }

        SDL_RenderDrawPoints(ren, points, points_drawn);
        // Update the screen
        SDL_RenderPresent(ren);

        // Calculate and log frame time
        clock_t end_time = clock();
        double frame_time = (double)(end_time - start_time) / CLOCKS_PER_SEC * 1000.0; // in milliseconds
        fprintf(metrics_file, "Frame Time: %.2f ms, Points Drawn: %d\n", frame_time, points_drawn);

        // Increment t for animation
        frame_count++;

        t += 0.0000001f;
    }

    // Cleanup
    fclose(metrics_file);
    free(p);
    SDL_DestroyRenderer(ren);
    SDL_DestroyWindow(win);
    SDL_Quit();

    return 0;
}