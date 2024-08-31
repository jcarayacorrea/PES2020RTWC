async function playMatches() {
    let promisesArray = arrayToPromise(document.getElementsByClassName("matches"));
    document.getElementById('btnExec').disabled = true;
    document.getElementById('rotateOnDiv').style.display = "block";
    document.getElementById('rotateOffDiv').style.display = "none";
    for (let i = 0; i < promisesArray.length; i++) {
        await execPromises(promisesArray[i]);
    }
}

function arrayToPromise(matches) {
    let promiseArray = []
    for (let i = 0; i < matches.length; i += 2) {
        promiseArray.push([createPromise(matches.item(i).click(),(i === 0) ? 0 : 20000), createPromise(matches.item(i + 1).click(),(i === 0) ? 0 : 20000)])
    }
    return promiseArray;
}

function createPromise(execLine, waitTime) {
    return new Promise((resolve) => {
        setTimeout(()=>{
           resolve(execLine)
        },waitTime)

    });
}

async function execPromises(promArray, ) {
     return await Promise.all(promArray).then(()=>{console.log('Ejecutando matches....')});

}