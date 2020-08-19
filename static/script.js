function sayHello() {
    alert('Hello!');
    console.log('Hello');
}

function fetchHelloText() {
    fetch('/hello')
        .then(function (response) {
            return response.text();
        }).then(function (text) {
            console.log('GET response text:');
            console.log(text); // Print the greeting as text
        });
}

function fetchHelloJSON() {
    fetch('/hello')
        .then(function (response) {
            console.log(response);
            return response.json(); // But parse it as JSON this time
        })
        .then(function (json) {
            console.log('GET response as JSON:');
            console.log(json); // Here's our JSON object
        });
}

// POST to python file
function postMessage() {
    fetch ('/hello', {
        method: 'POST',

        // JSON payload
        body: JSON.stringify({
            "greeting": "Hello from the browser!"
        })
    }).then(function (response) {
        return response.text();
    }).then(function (text) {

        console.log('POST response: ');

        // Should be 'OK'
        console.log(text);
    });
}

/* Gets data from Spreadsheet and displays it */
function getData() {
    fetch('/data')
        .then(function(response) {
            console.log(response);
            return response.json();
        }).then(function(results) {
            dataDiv = document.getElementById('data');
            dataDiv.innerHTML = '';
            for (x in results) {
                categoryDiv = document.createElement('div');
                categoryDiv.id = x;
                categoryList = makeList(results[x]);
                categoryDiv.innerHTML = '<p>'+x+'</p>';
                categoryDiv.appendChild(categoryList);
                dataDiv.appendChild(categoryDiv);
            }
        });
}

/* Creates a list element given an array */
function makeList(array) {
    unorderedListElement = document.createElement('ul');
    for (var i = 0; i < array.length; i++) {
        listElement = document.createElement('li');
        linkElement = document.createElement('a');
        linkElement.href = array[i];
        linkElement.innerText = array[i];
        //listElement.innerHTML = '<a href="'+array[i]+'">'+array[i]+'</a>';
        listElement.append(linkElement);
        unorderedListElement.appendChild(listElement);
    }
    return unorderedListElement;
}
