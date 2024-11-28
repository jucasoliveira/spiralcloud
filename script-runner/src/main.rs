use anyhow::{Context, Result};
use lazy_static::lazy_static;
use std::{collections::HashMap, env, fs, path::Path, process::Command};

lazy_static! {
    static ref LANGUAGE_CONFIG: HashMap<&'static str, LanguageConfig> = {
        let mut m = HashMap::new();
        m.insert(
            "python",
            LanguageConfig {
                extensions: vec![".py"],
                command: "python",
                package_file: "requirements.txt",
                directory: "python",
                main_file: "spiral.py",
            },
        );
        m.insert(
            "node",
            LanguageConfig {
                extensions: vec![".js", ".ts"],
                command: "node",
                package_file: "package.json",
                directory: "node",
                main_file: "index.js",
            },
        );
        m.insert(
            "go",
            LanguageConfig {
                extensions: vec![".go"],
                command: "go run",
                package_file: "go.mod",
                directory: "go",
                main_file: "main.go",
            },
        );
        m.insert(
            "rust",
            LanguageConfig {
                extensions: vec![".rs"],
                command: "cargo run",
                package_file: "Cargo.toml",
                directory: "rust",
                main_file: "src/main.rs",
            },
        );
        m.insert(
            "c",
            LanguageConfig {
                extensions: vec![".c"],
                command: "gcc",
                package_file: "spiral.c",
                directory: "c",
                main_file: "spiral_sdl2.c",
            },
        );
        m
    };
}

#[derive(Debug)]
struct LanguageConfig {
    extensions: Vec<&'static str>,
    command: &'static str,
    package_file: &'static str,
    directory: &'static str,
    main_file: &'static str,
}

fn run_language(language: &str) -> Result<()> {
    let config = LANGUAGE_CONFIG
        .get(language)
        .with_context(|| format!("Language not supported: {}", language))?;

    let dir_path = Path::new(config.directory);
    if !dir_path.exists() {
        anyhow::bail!("Directory not found: {}", config.directory);
    }

    let main_file_path = dir_path.join(config.main_file);
    if !main_file_path.exists() {
        anyhow::bail!("Main file not found: {}", main_file_path.display());
    }

    println!("Running {} project in {}", language, config.directory);

    // Check for package file and install dependencies if needed
    let package_file_path = dir_path.join(config.package_file);
    if package_file_path.exists() {
        match language {
            "python" => {
                println!("Installing Python dependencies...");
                Command::new("pip")
                    .args(["install", "-r"])
                    .arg(&package_file_path)
                    .status()
                    .context("Failed to install Python dependencies")?;
            }
            // Add other package managers as needed
            _ => {}
        }
    }

    // Change to the project directory
    env::set_current_dir(dir_path).context("Failed to change to project directory")?;

    let mut command_parts = config.command.split_whitespace();
    let command = command_parts.next().unwrap();

    let status = Command::new(command)
        .args(command_parts)
        .arg(&config.main_file)
        .status()
        .with_context(|| format!("Failed to execute {} command", command))?;

    if !status.success() {
        anyhow::bail!("Script execution failed with status: {}", status);
    }

    Ok(())
}

fn main() -> Result<()> {
    let args: Vec<String> = env::args().collect();

    if args.len() != 2 {
        println!("Usage: {} <language>", args[0]);
        println!("Supported languages: python, node, go, rust, c");
        std::process::exit(1);
    }

    let language = args[1].to_lowercase();
    run_language(&language)?;
    Ok(())
}
