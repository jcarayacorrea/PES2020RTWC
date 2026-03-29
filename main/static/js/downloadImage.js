/**
 * Capture a div and download it as an image
 * @param {string} divName - ID of the div to capture
 * @param {string} fileName - Name for the downloaded file (default: 'worldcup.jpg')
 */
const downloadImage = async (divName, fileName = 'worldcup.jpg') => {
    const div = document.getElementById(divName);
    if (!div) {
        console.error(`Element with ID ${divName} not found`);
        return;
    }

    try {
        const canvas = await html2canvas(div, {
            useCORS: true,
            allowTaint: true
        });

        const link = document.createElement("a");
        link.href = canvas.toDataURL("image/jpeg", 1.0);
        
        // Ensure fileName has .jpg extension
        const finalName = fileName.endsWith('.jpg') ? fileName : `${fileName}.jpg`;
        link.download = finalName;
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Error generating image:', error);
    }
};

// Event listener for download image buttons
document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-action="download-image"]');
    if (target) {
        const { targetDiv, fileName } = target.dataset;
        if (targetDiv) {
            downloadImage(targetDiv, fileName);
        }
    }
});



