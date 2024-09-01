const playMatches = async () => {

    document.getElementById('btnExec').disabled = true;
    document.getElementById('rotateOnDiv').style.display = "block";
    document.getElementById('rotateOffDiv').style.display = "none";

   $('#fixtures button').map((index,element)=>{
      element.click();
   })



}

