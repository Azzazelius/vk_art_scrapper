// const jsonContent = document.getElementsByClassName('json_link')[0]; // Обращаемся к первому элементу из коллекции
// console.log('test');

// function run() {
//     console.log(jsonContent);
//     jsonContent.innerHTML = 'Нет элементов';
// }

// run();


// document.getElementById('runButton').addEventListener('click', async function() {
//     // Загрузка содержимого файла scrapper.py
//     const response = await fetch('py/scrapper.py'); 
//     const code = await response.text();

//     // Выполнение кода из файла
//     try {
//         const result = await runPythonCode(code);
//         document.getElementById('output').innerText = 'Scrapper executed successfully:\n' + result;
//     } catch (error) {
//         document.getElementById('output').innerText = 'Error executing scrapper:\n' + error;
//     }
// });

// async function runPythonCode(code) {
//     const response = await fetch('/api/run_python_code', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({ code })
//     });

//     if (!response.ok) {
//         throw new Error('Failed to execute python code');
//     }

//     return await response.text();
// }

/* 
Вопросы для прояснения
        
async function()
    fetch

    html
        <pre 
*/




// ----------------------------------------------

// ----------------------------------------------

console.log('Script activated');


document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('downloadBtn');
    const statusMessage = document.getElementById('statusMessage');

    downloadBtn.addEventListener('click', async function() {
        console.log('Sent request to the server');
        try {
            const response = await fetch('/download_images', {
                method: 'POST'
            });

            if (response.ok) {
                statusMessage.textContent = 'Images downloaded successfully!';
            } else {
                statusMessage.textContent = 'Error downloading images.';
            }
        } catch (error) {
            console.error('An error occurred:', error);
            statusMessage.textContent = 'Error downloading images.';
        }
    });
});
