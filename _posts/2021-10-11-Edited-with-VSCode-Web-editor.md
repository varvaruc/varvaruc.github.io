
This is a test and was edited and commited with VS code web editor

Here's some code

```
// Promisifying setTimeout
const wait = function (seconds) {
  return new Promise(function (resolve) {
    setTimeout(resolve, seconds * 1000);
  });
};

// callback hell avoided
wait(2)
  .then(() => {
    console.log("I waited for 2 seconds");
    return wait(1);
  })
  .then(() => {
    console.log("I waited for 1 seconds");
    return wait(0.5);
  })
  .then(() => {
    console.log("I waited for 0.5 seconds");
  });
```
