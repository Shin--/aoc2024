use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;


pub fn read_data(day: u32, production: bool) -> io::Result<Vec<String>> {
  let mut file_name = "dev.txt";
  if production {
    file_name = "production.txt"
  }
  let file_path = format!("C:/Users/Tim/Repos/aoc2024/data/day{}/{}", day, file_name);

  let path = Path::new(&file_path);
  let file = File::open(path)?;
  let reader = io::BufReader::new(file);

  let lines = reader.lines().collect::<Result<Vec<_>, _>>()?;
  Ok(lines)
}