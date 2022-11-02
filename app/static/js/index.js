const fileText = document.querySelector('.file-custom')
const fileInput = document.querySelector('input[type="file"]')

fileInput.addEventListener('change', () => {
    if(fileInput.value.length > 0)
        fileText.innerText = fileInput.value.replace(/.*[\/\\]/, '')
    else fileText.innerText = 'None'
})
