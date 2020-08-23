function sayHello() {
    alert('Hello!');
}

/* Gets data from Spreadsheet and displays it */
function getData(category) {
    fetch('/data?category='+category)
        .then(function(response) {
            return response.json();
        }).then(function(results) {
            dataDiv = document.getElementById('data-'+category);
            dataDiv.innerHTML = category;
            categoryList = makeList(results);
            dataDiv.appendChild(categoryList);
        });
}

/* Creates a list element given an array */
function makeList(array) {
    unorderedListElement = document.createElement('ul');
    for (var i = 0; i < array.length; i++) {
        listElement = document.createElement('li');
        linkElement = document.createElement('a');
        linkElement.href = array[i][1];
        linkElement.innerText = array[i][0];
        listElement.append(linkElement);
        unorderedListElement.appendChild(listElement);
    }
    return unorderedListElement;
}
