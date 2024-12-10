// 167650499
// 95846796

use regex::Regex;
use crate::utils::read_data;


fn part_1(instructions: &[String]) -> i32 {
  let pattern = r"mul\((\d+),(\d+)\)";
  let regex = Regex::new(pattern).unwrap();

  return instructions.iter()
    .flat_map(|row| regex.captures_iter(row))
    .filter_map(|captures| {
      let v1 = captures.get(1)?.as_str().parse::<i32>().ok()?;
      let v2 = captures.get(2)?.as_str().parse::<i32>().ok()?;
      Some(v1 * v2)
    })
    .sum();
}


fn part_2(instructions: &[String]) -> i32 {
  let regex = Regex::new(r"mul\((\d+),(\d+)\)|don't\(\)|do\(\)").unwrap();
  let mut total_value = 0;
  let mut do_active = true;

  for row in instructions {
      for captures in regex.captures_iter(&row) {
          match captures.get(0).map(|m| m.as_str()) {
              Some("do()") => do_active = true,
              Some("don't()") => do_active = false,
              Some(matched) if do_active && matched.starts_with("mul") => {
                  if let (Some(v1), Some(v2)) = (captures.get(1), captures.get(2)) {
                    let v1 = v1.as_str().parse::<i32>().unwrap();
                    let v2 = v2.as_str().parse::<i32>().unwrap();
                    total_value += v1 * v2;
                  }
              }
              _ => {}
          }
      }
  }

  total_value
}


pub fn solve() {
  let instructions: Vec<String> = match read_data(3, true) {
    Ok(data) => data.into_iter().collect(),
    Err(err) => {
      eprintln!("Error reading data {}", err);
      return;
    }
  };
  println!("Part 1: {}", part_1(&instructions));
  println!("Part 2: {}", part_2(&instructions));
}