import fs from 'fs'

fs.readFile('input.txt', 'utf8', (_, data) => {
  const newLocal = data.split('\n').filter(a => a);
  const { lItems, rItems } = newLocal.reduce(({ lItems, rItems }, val) => {
    const [l, r] = val.split("   ").map(a => Number.parseInt(a));
    lItems.push(l);
    rItems.push(r);
    return { lItems, rItems };
  }
    , { lItems: [], rItems: [] })

  rItems.sort()
  const partA = lItems.toSorted().reduce((state, curr, i) => state + Math.abs(curr - rItems[i]), 0)
  const { sum: partB, cache } = lItems.toSorted().reduce((state, curr) => {
    const cachedFrequency = state.cache[curr];
    if (cachedFrequency) {
      return { ...state, sum: state.sum + cachedFrequency * curr }
    }
    const frequency = rItems.filter(i => i === curr).length;

    state.cache[curr] = frequency
    return { ...state, sum: state.sum + frequency * curr }
  }, { cache: {}, sum: 0 })
  console.log(cache)
  console.log(partA);
  console.log(partB);

})

