use crate::utils::read_data;


fn search_word_part_1(grid: &[char], width: usize, height: usize, search: &str) -> usize {
  let directions = [
      (1, 0),   // Horizontal right
      (0, 1),   // Vertical down
      (1, 1),   // Diagonal down-right
      (1, -1),  // Diagonal up-right
  ];
  let search_rev: String = search.chars().rev().collect();
  let search_len = search.len();
  let mut count = 0;
  let start_char = search.chars().next().unwrap();
  let reverse_start_char = search_rev.chars().next().unwrap();

  for y in 0..height {
    for x in 0..width {
      let current_char = grid[y * width + x];
      if current_char != start_char && current_char != reverse_start_char {
        continue;
      }
      for &(dx, dy) in &directions {
        let mut matches = true;
        let mut matches_rev = true;

        for i in 0..search_len {
          let nx = x as isize + i as isize * dx;
          let ny = y as isize + i as isize * dy;
          if nx < 0 || nx >= width as isize || ny < 0 || ny >= height as isize {
            matches = false;
            matches_rev = false;
            break;
          }
          let idx = ny as usize * width + nx as usize;
          if grid[idx] != search.chars().nth(i).unwrap() {
            matches = false;
          }
          if grid[idx] != search_rev.chars().nth(i).unwrap() {
              matches_rev = false;
          }
        }

        if matches || matches_rev {
          count += 1;
        }
      }
    }
  }

  return count;
}


fn build_string(grid: &[char], directions: &[(isize, isize)], width: usize, height: usize, x: usize, y: usize) -> Option<String> {
  let mut val = String::new();
  for &(dx, dy) in directions {
    let nx = x as isize + dx;
    let ny = y as isize + dy;

    if nx < 0 || nx >= width as isize || ny < 0 || ny >= height as isize {
      break;
    }

    let idx = ny as usize * width + nx as usize;
    val.push(grid[idx]);
  }
  return Some(val);
}
 

fn search_word_part_2(grid: &[char], width: usize, height: usize, search: &str) -> usize {
  let directions_up_right = [
      (-1, 1),  // down-left
      (0, 0),
      (1, -1),  // up-right
  ];
  let directions_down_right = [
      (-1, -1), // up-left
      (0, 0),
      (1, 1),   // down-right
  ];
  let search_rev: String = search.chars().rev().collect();
  let mut count = 0;

  for y in 0..height {
    for x in 0..width {
      let current_char = grid[y * width + x];
      if current_char != 'A' {
        continue;
      }

      if let Some(string_up_right) = build_string(grid, &directions_up_right, width, height, x, y) {
        if string_up_right == search || string_up_right == search_rev {
          if let Some(string_down_right) = build_string(grid, &directions_down_right, width, height, x, y) {
            if string_down_right == search || string_down_right == search_rev {
              count += 1;
            }
          }
        }
      }
    }
  }

  return count;
}


pub fn solve() {
  let data: Vec<String> = match read_data(4, true) {
    Ok(data) => data.into_iter().collect(),
    Err(err) => {
      eprintln!("Error reading data {}", err);
      return;
    }
  };
  let width = data[0].len();
  let height = data.len();
  let search = "XMAS";
  let single_line: Vec<char> = data.concat().chars().collect();
  let found_words = search_word_part_1(&single_line, width, height, search);
  println!("Part 1: {}", found_words);
  let found_crosses = search_word_part_2(&single_line, width, height, "MAS");
  println!("Part 2: {}", found_crosses);
}