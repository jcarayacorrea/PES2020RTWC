function playMatches(){
    matchesbtn = document.getElementsByClassName("matches");
    document.getElementById('btnExec').disabled = true;
    document.getElementById('rotateOnDiv').style.display = "block";
    document.getElementById('rotateOffDiv').style.display = "none";
    for (match of matchesbtn){
        match.click();
    }
}