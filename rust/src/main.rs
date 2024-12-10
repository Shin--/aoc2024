mod day1;
mod day2;
mod day3;
mod day4;
mod utils;

use std::time::Instant;

fn main() {
    println!("Day 1");
    let start = Instant::now();
    day1::solve();
    let duration = start.elapsed();
    println!("Day 1 completed in {:?}", duration);

    println!("Day 2");
    let start = Instant::now();
    day2::solve();
    let duration = start.elapsed();
    println!("Day 2 completed in {:?}", duration);

    println!("Day 3");
    let start = Instant::now();
    day3::solve();
    let duration = start.elapsed();
    println!("Day 3 completed in {:?}", duration);

    println!("Day 4");
    let start = Instant::now();
    day4::solve();
    let duration = start.elapsed();
    println!("Day 4 completed in {:?}", duration);
}
