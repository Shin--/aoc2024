use crate::utils::read_data;


fn check_report(report_values: &Vec<i32>) -> bool {
  let mut last_value: i32 = report_values[0];
  let is_increasing: bool = last_value < report_values[1];
  for report_value in &report_values[1..] {
    if (report_value - last_value).abs() > 3 || (is_increasing != (last_value < *report_value)) || last_value == *report_value {
      return false
    }
    last_value = *report_value
  }
  return true
}

fn part_1(reports: &Vec<Vec<i32>>) {
  let mut unsafe_reports: i32 = 0;
  let total_reports = reports.len() as i32;
  for report in reports {
    if !check_report(&report) {
      unsafe_reports += 1;
    }
  }
  println!("Part 1 - Valid reports: {}", total_reports - unsafe_reports)
}

fn part_2(reports: &Vec<Vec<i32>>) {
  let mut unsafe_reports: i32 = 0;
  let total_reports = reports.len() as i32;
  for report in reports {
    if !check_report(&report) {
      let mut dampened_reports: Vec<Vec<i32>> = Vec::new();
      for i in 0..report.len() {
        let mut dampened_report = report.clone();
        dampened_report.remove(i); // Remove the element at index `i`
        dampened_reports.push(dampened_report);
      }
      if !dampened_reports.iter().any(|dampened_report| check_report(dampened_report)) {
        unsafe_reports += 1;
      }
    }
  }
  println!("Part 2 - Valid reports: {}", total_reports - unsafe_reports)
}

pub fn solve() {
  let mut reports: Vec<Vec<i32>> = Vec::new();
  match read_data(2, true) {
    Ok(data) => {
      for line in data {
        if line.len() > 0 {
          reports.push(line.split_whitespace().filter_map(|x| x.parse::<i32>().ok()).collect())
        }
      }
    }
    Err(err) => {
      eprintln!("Error reading data {}", err)
    }
  }
  part_1(&reports);
  part_2(&reports);
}
