function playMatches(){
    matchesbtn = document.getElementsByClassName("matches");
    document.getElementById('btnExec').disabled = true;
    document.getElementById('rotateOnDiv').style.display = "block";
    document.getElementById('rotateOffDiv').style.display = "none";
    for (let i=0;i<matchesbtn.length;i++){
           matchesbtn.item(i).click();
    }
}