function loading(){
    setTimeout(()=>{
       document.getElementById('section').style.visibility = 'hidden'
        document.getElementById('loading').style.visibility = 'visible'
    },4000);
    document.getElementById('section').style.visibility = 'visible'
        document.getElementById('loading').style.visibility = 'hidden'
    console.log('loading...')
}

