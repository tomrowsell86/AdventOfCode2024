
BEGIN {
  summing = 1;
  sum = 0;
}
{
  if ($1 == "stop") {
    summing=0;
  }
  else if ($1 == "start") {
    summing=1;
  }
  else if(summing == 1) {
    sum += ($1 * $2);
  }
}
END { print sum }
