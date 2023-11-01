function changeTeamStage(id,stage){
 //   console.log('Token --->' + getCookie('csrfToken'));
    const xhttp = new XMLHttpRequest();
   //  xhttp.setRequestHeader("X-CSRFToken",getCookie('csrfToken'));
     xhttp.open('POST','updateProgress/'+id+'/'+stage,true);
    xhttp.send();
}

function downloadDraw(html){
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST','/api/download_draw/', true);
    xhttp.send(html);
}


