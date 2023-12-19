const user_name = document.getElementById('user_name');
const collection_id = document.getElementById('collection_id');
const token = document.getElementById('token');
const websocket_url = document.getElementById('websocket_url');
const ws = new WebSocket(websocket_url.value);
ws.onmessage = function (event) {
  try {
    const todo = JSON.parse(event.data);
    processTodo(todo);
    console.log("Received: '" + event.data + "'");
  } catch (e) {
    console.log(event.data);
  }
};

function processTodo(todo) {
  let todos = document.getElementById('todos');
  let todoItem = document.createElement('article');
  todoItem.className = 'item';
  let todoTitle = document.createElement('h3');
  let todoDescription = document.createElement('p');
  todoTitle.textContent = todo.title;
  todoDescription.textContent = todo.description;
  todoItem.appendChild(todoTitle);
  todoItem.appendChild(todoDescription);
  todos.appendChild(todoItem);
}
function sendMessage(event) {
  let todoTitle = document.getElementById('todoTitle');
  let todoDescription = document.getElementById('todoDescription');
  // To jsson
  let todo = {
    title: todoTitle.value,
    description: todoDescription.value,
  };
  // To string
  let todoString = JSON.stringify(todo);
  ws.send(todoString);
  todoTitle.value = '';
  todoDescription.value = '';
  event.preventDefault();
}
async function addToCollection(event) {
  event.preventDefault();
  // Send to server put with fetch
  let user_name_to_add = document.getElementById('user_name_to_add');
  let user_name_to_add_value = user_name_to_add.value;
  let url = '/api/v1/member/create';
  let data = {
    user_name: user_name_to_add_value,
    collection_id: collection_id.value,
  };
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (response.redirected) {
        alert('User already in collection');
      } else {
        return response;
      }
    })
    .catch((error) => {
      console.log(error);
    });

  const content = await response.json();
  console.log(content);
  user_name_to_add.value = '';
}
