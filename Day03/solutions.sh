#!/bin/bash
wdir=$(dirname -- "${BASH_SOURCE[0]}")
echo -n "Part a :"
(grep -oP 'mul\(\d{1,3},\d{1,3}\)' | sed 's/mul(\(.*\),\(.*\))/\1 \2/' | awk 'BEGIN{sum = 0}{sum += ($1 * $2)}END{print sum}') <"${wdir}/input.txt"
echo -n "Part b :"
(grep -oP "mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)" |
  sed 's/mul(\(.*\),\(.*\))/\1 \2/' | sed "s/don't()/stop/" | sed 's/do()/start/' |
  awk -f "${wdir}/part_b.awk") <"${wdir}/input.txt"
