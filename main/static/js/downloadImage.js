function downloadImage(divName) {
    const div = document.getElementById(divName);
   let imageUrl =  html2canvas(div).then((canvas)=>{
       let link = document.createElement("a");
       link.href=  canvas.toDataURL("image/jpeg",1);
       link.download = "worldcup.jpg";
       link.click();
    });

}



