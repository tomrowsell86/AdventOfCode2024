import fs from 'fs'

fs.readFile("input.txt", "ascii", (_, data) => {
  day2(data, true)
})
function day2(data, partB) {
  const safeLevels = data.split('\n').filter(a => a).map(l => l.split(' ').map(a => Number.parseInt(a)))
    .reduce((count, curr) => {
      let prev = curr[0]
      let safe = true
      let badLevelRemoved = false
      let direction


      for (const a of curr.slice(1)) {
        const diff = a - prev
        if (diff === 0 || Math.abs(diff) > 3 || Math.abs(diff) < 1) {
          if (partB && !badLevelRemoved) {
            badLevelRemoved = true
            continue
          } else {
            safe = false
            break
          }
        }
        if (!direction) {
          direction = diff > 0 ? "ASC" : "DESC"
        }
        safe = (direction === "ASC" ? diff > 0 : diff < 0)
        if (!safe)
          if (partB && !badLevelRemoved) {
            badLevelRemoved = true
            safe = true
            continue
          }
          else {
            break
          }
        prev = a
      }
      if (safe === true) {
        if (badLevelRemoved) {
          console.log('safe bad level - ' + curr)
        }
        count++
      }
      else {
        console.log('unsafe - ' + curr)
      }
      return count
    }, 0)
  console.log(safeLevels)
}
