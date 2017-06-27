var counter = 0

function addInput()
{
    var input=document.createElement('input');
    input.type = 'text';
    input.name = 'keyword' + counter;
    counter += 1;
    document.getElementById('add').appendChild(input);
    var input=document.createElement('Br');
    document.getElementById('add').appendChild(input);
}