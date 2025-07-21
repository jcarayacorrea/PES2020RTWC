function changeTeamStage(code,stage){
 //   console.log('Token --->' + getCookie('csrfToken'));
    const xhttp = new XMLHttpRequest();
   //  xhttp.setRequestHeader("X-CSRFToken",getCookie('csrfToken'));
     xhttp.open('POST','updateProgress/'+code+'/'+stage,true);
    xhttp.send();
}



